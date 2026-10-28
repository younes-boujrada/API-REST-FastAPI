# Compte rendu : TP API LogiAI

**Noms :** ............................  **Groupe :** ........

## 1. Environnement et premiers tests
- Sortie de `python -m pytest` au départ (collez-la) :
```
collected 13 items

tests\test_api.py ..FFFF......F                                                                                  [100%]

====================================================== FAILURES ======================================================= 
FAILED tests/test_api.py::test_predict_valide_renvoie_200 - assert 422 == 200
FAILED tests/test_api.py::test_predict_forme_de_la_reponse - AssertionError: assert {'detail'} == {'alerte', 'model_version', 'probabilite_retard', 'seuil'}
FAILED tests/test_api.py::test_predict_probabilite_entre_0_et_1 - KeyError: 'probabilite_retard'
FAILED tests/test_api.py::test_predict_trajet_risque_plus_eleve_que_trajet_facile - KeyError: 'probabilite_retard'
FAILED tests/test_api.py::test_modele_absent_renvoie_503 - assert 422 == 503
======================================= 5 failed, 8 passed, 1 warning in 3.48s ========================================
```
- Performances initiales (`python -m logiai.train`) :
  - **Baseline accuracy** : 72.6 % (prédire toujours « à l'heure »)
  - **Accuracy du modèle** : 77.4 %
  - **Rappel du modèle** : 46.4 % (sur 100 livraisons réellement en retard, environ 46 sont détectées)
- Pourquoi certains tests qui attendent un 422 passent-ils déjà, alors que rien n'est écrit ?
  Le schéma `Livraison` contenait la configuration `model_config = ConfigDict(extra="forbid")` et aucun champ n'était encore déclaré (hormis `distance_km`). Par conséquent, tout champ envoyé dans la requête était considéré comme inconnu et rejeté automatiquement par Pydantic avec un statut **422 Unprocessable Entity**. Les tests attendant 422 passaient donc par "faux positif" car tout était refusé, même les requêtes valides.

## 2. Mon schéma
- Mes bornes et leur justification physique (une ligne par variable) :

| Variable | Min | Max | Pourquoi |
|---|---|---|---|
| distance_km | 1 | 1000 | Trajet d'au moins 1 km en ville jusqu'à 1000 km pour une liaison routière nationale. |
| poids_kg | 0.1 | 30000 | D'un petit colis léger en deux-roues (100 g) jusqu'à la charge utile maximale d'un camion 38-44 tonnes. |
| heure_depart | 0 | 23 | Heure de la journée sur une plage de 24 heures (0h00 à 23h59). |
| pluie_mm | 0 | 300 | Temps sec (0 mm) jusqu'à des conditions d'orages tropicaux / pluies torrentielles extrêmes (300 mm). |
| trafic_index | 0 | 10 | Échelle d'indice normalisée définie dans le contrat LogiAI (0 = circulation fluide, 10 = réseau saturé). |
| nb_arrets | 0 | 50 | Trajet direct sans escale (0) jusqu'à une tournée de distribution urbaine intensive (50 arrêts). |

## 3. Ma fonction predict()
```python
@app.post("/v1/predict", response_model=PredictionOut)
def predict(livraison: Livraison):
    predictor = state.get("predictor")
    if predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Modèle indisponible. Veuillez entraîner ou charger le modèle.",
        )
    return PredictionOut(**predictor.predict(livraison.model_dump()))
```

## 4. Quatre requêtes
| Requête | Code obtenu | Pourquoi |
|---|---|---|
| livraison normale | 200 | Données conformes au contrat de l'API et modèle chargé en mémoire. |
| distance_km = -5 | 422 | Distance négative invalide violant la règle de validation `ge=1` du schéma Pydantic. |
| type_vehicule = "avion" | 422 | Valeur hors du `Literal["moto", "fourgon", "camion"]` défini dans le schéma. |
| modèle absent (supprimez models/ et relancez) | 503 | `state.get("predictor")` renvoie `None` ; l'API lève une `HTTPException(status_code=503)`. |

## 5. Questions de compréhension
1. **Pourquoi charge-t-on le modèle au démarrage et pas à chaque requête ?**
   Charger un modèle sérialisé (`joblib`) depuis le disque implique des accès disques (I/O) et une désérialisation lourde. Le charger une seule fois au démarrage (via le cycle de vie `lifespan`) et le conserver en RAM permet à l'API de répondre à chaque requête en quelques millisecondes sans saturer les ressources.
2. **Qui écrit le contrôle « pluie <= 100 », et où est-il écrit ?**
   C'est le développeur qui l'écrit dans le schéma Pydantic (`logiai/api/schemas.py`) dans l'argument `le=...` de `Field(...)`. FastAPI et Pydantic se chargent ensuite de l'exécuter automatiquement à chaque requête.
3. **Différence entre 422 et 503 ?**
   - **422 (Unprocessable Entity)** : Erreur côté **client** (requête syntaxiquement correcte mais données non conformes aux contraintes du schéma).
   - **503 (Service Unavailable)** : Erreur côté **serveur** (le service de prédiction est temporairement indisponible car le modèle de machine learning n'est pas chargé).
4. **Pourquoi une route `/v1/predict` plutôt que `/predict` ?**
   Le versionnement dans l'URL (`/v1`) permet de faire évoluer l'API dans le futur (ex: changer le contrat pour une `/v2`) sans casser les applications clientes existantes qui continuent d'utiliser la v1.
5. **Que se passerait-il si la distance était déclarée `int` ?**
   Une distance avec des décimales (par exemple `12.5` km) provoquerait une erreur 422 ou une troncature indésirable lors de la conversion, interdisant aux utilisateurs de transmettre des distances précises.

## 6. Décision : modèle absent
**Répondre 503 ou refuser de démarrer ? Qu'est-ce que chaque option fait perdre ?**
- **Option A (Répondre 503) :** L'API reste en ligne, la route de supervision `/health` fonctionne (`"model_loaded": false`) et la documentation `/docs` reste accessible. On peut diagnostiquer précisément la panne. En revanche, les requêtes d'inférence échouent (503), ce qui peut dérouter un client s'il ne vérifie pas `/health`.
- **Option B (Refuser de démarrer / Crash au démarrage) :** Approche *fail-fast* : les orchestrateurs (Kubernetes, Docker) détectent immédiatement le crash et évitent de router du trafic vers une instance non fonctionnelle. En contrepartie, on perd l'accès à la documentation et aux endpoints d'observabilité (`/health`), et l'instance entre dans une boucle de redémarrage (CrashLoopBackOff).

## 7. Lien de la pull request
*(À coller ici après la création de la Pull Request sur GitHub, ex: https://github.com/votre-compte/API-REST-FastAPI/pull/1)*

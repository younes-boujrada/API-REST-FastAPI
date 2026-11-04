# Compte rendu : tester, sécuriser et appeler l'API LogiAI

**Noms :** ............................  **Groupe :** ........

## 1. Casser son API (activité 1)
| Cas | Requête (corps ou URL) | Prévu | Obtenu |
|---|---|---|---|
| champ manquant | | | |
| valeur absurde | | | |
| texte au lieu d'un nombre | | | |
| champ en trop | | | |
| mauvaise route | | | |

- Une requête acceptée alors qu'elle devait être refusée ? Laquelle ?

## 2. Les 2 bugs (activité 2)
| Bug | Test qui l'a révélé | Comportement avant | Correction |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

- Sortie de `python -m pytest` à la fin de l'activité 2 :

## 3. La clé API (sprint 1)
- Ma fonction `verify_api_key()` (collez le code) :

| Requête | Code obtenu |
|---|---|
| `/v1/predict` sans clé | |
| `/v1/predict` fausse clé | |
| `/v1/predict` clé utilisateur | |
| `/v1/model-info` clé utilisateur | |
| `/v1/model-info` clé administrateur | |
| `/health` sans clé | |

- Preuve que `.env` n'est pas dans Git (sortie de `git status`) :

## 4. Le client web (sprint 2)
- Mon `fetch` (collez le code) :
- Ce qui s'affiche : livraison normale / pluie de 500 mm / fausse clé :
- Expérience CORS (page servie sur le port 5501) : que disent la page et la console (F12) ? Pourquoi `curl` marche-t-il quand même ?
- Où voyez-vous la clé dans F12 ?

## 5. Questions de compréhension
1. Quelle différence entre 401, 403 et 422 ?
2. Pourquoi la clé n'est-elle ni dans le code ni dans Git ?
3. Pourquoi comparer avec `compare_digest` plutôt qu'avec `==` ?
4. Pourquoi `curl` fonctionne-t-il alors que la page du port 5501 est bloquée ?
5. Pourquoi la validation faite par le navigateur ne remplace-t-elle pas celle de l'API ?

## 6. Lien de la pull request

# Étude de conception — LogiAI

## 1. Besoin
*À rédiger lors d'une prochaine itération.*

## 2. Données
*À rédiger lors d'une prochaine itération.*

## 3. Modèle et métriques
*À rédiger lors d'une prochaine itération.*

## 4. Critères d'acceptation
*À rédiger lors d'une prochaine itération.*

## 5. Cycle de vie
*À rédiger lors d'une prochaine itération.*

## 6. Architecture

L'application **LogiAI** repose sur un cœur métier empaqueté (`logiai` installé dans `site-packages`) consommé à la fois par une interface en ligne de commande locale (`logiai-predict`) et par une architecture web conteneurisée (Docker Compose avec Nginx en point d'entrée unique et FastAPI en backend). Les données et le modèle entraîné restent découplés du code dans `data/` et `models/`, localisés par la variable `LOGIAI_HOME`.

```text
+-----------------------------------------------------------------------------------+
|                                MACHINE HÔTE (Windows)                             |
|                                                                                   |
|  +---------------------------+        +----------------------------------------+  |
|  | Terminal / CLI            |        | Navigateur Web                         |  |
|  | $ logiai-predict          |        | http://localhost:8080                  |  |
|  |   livraison.json          |        +-------------------+--------------------+  |
|  +-------------+-------------+                            |                       |
|                | lit LOGIAI_HOME                          | HTTP (:8080)          |
|                v                                          v                       |
|  +---------------------------+        +----------------------------------------+  |
|  | Dossiers locaux           |        | Conteneur : logiai-web (nginx:alpine)  |  |
|  | - data/livraisons.csv     |        | - Sert / (page web HTML/JS)            |  |
|  | - models/model.joblib     |        | - Reverse proxy /api/ -> api:8000      |  |
|  | - models/model_info.json  |        +-------------------+--------------------+  |
|  +-------------+-------------+                            |                       |
|                |                                          | Réseau Docker interne |
|                | volumes Docker                           | http://api:8000/      |
|                | (./data, ./models)                       v                       |
|                |                      +----------------------------------------+  |
|                |                      | Conteneur : logiai-api (python:3.11)   |  |
|                |                      | - /app : data/, models/ (LOGIAI_HOME)  |  |
|                +--------------------->| - site-packages : package logiai 0.1.0 |  |
|                                       | - Uvicorn / FastAPI (:8000)            |  |
|                                       |   POST /v1/predict, GET /health        |  |
|                                       +----------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

### Flux principaux
1. **Entraînement hors-ligne :** `python -m logiai.dataset` génère `data/livraisons.csv`, puis `python -m logiai.train` entraîne le pipeline `scikit-learn` et écrit `models/model.joblib` et `models/model_info.json`.
2. **Utilisation CLI :** la commande `logiai-predict` (point d'entrée `logiai.cli:main`) charge le modèle depuis `$LOGIAI_HOME/models/model.joblib` et affiche la probabilité de retard dans le terminal.
3. **Utilisation Web & API (Docker Compose) :** l'utilisateur accède à la page web sur `http://localhost:8080` servie par `logiai-web` (Nginx). Les requêtes vers `/api/*` sont relayées sur le réseau Docker interne vers `logiai-api` (FastAPI), qui importe `logiai` depuis `site-packages` et lit le modèle monté dans `/app/models`.

## 7. Choix technologiques
*À rédiger lors d'une prochaine itération.*

## 8. Risques et éthique
*À rédiger lors d'une prochaine itération.*

## 9. Limites
*À rédiger lors d'une prochaine itération.*


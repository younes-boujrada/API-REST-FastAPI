# ADR 004 : conteneurisation et déploiement de LogiAI avec Docker

## Décision 1 : le modèle est-il copié dans l'image (`COPY`) ou monté en volume ?

- **Votre choix :** combinaison des deux — le modèle (`models/`) et les données (`data/`) sont copiés dans l'image via `COPY` dans le `Dockerfile` pour rendre l'image autonome et transportable, et montés en volume (`./models:/app/models` et `./data:/app/data`) dans `docker-compose.yml` lors de l'exécution locale.
- **Ce que l'autre option ferait perdre :**
  - **Avec uniquement `COPY` (sans volume) :** le fichier `model.joblib` est figé dans une couche en lecture seule au moment du `docker build`. À chaque ré-entraînement (`python -m logiai.train` sur la machine hôte), le conteneur continuerait d'utiliser l'ancien modèle tant qu'on ne reconstruit pas l'image complète (`docker compose up -d --build`).
  - **Avec uniquement un volume (sans `COPY` dans le `Dockerfile`) :** l'image `logiai:1.0` ne serait plus autonome. Si on distribue l'image seule ou si on la lance avec `docker run` sur une autre machine sans dossier `./models` local, l'API démarrerait sans modèle (`model_loaded: false`, erreurs `503`).
  - **Compromis retenu :** `COPY` garantit qu'une image prête à l'emploi contient toujours un modèle valide par défaut, tandis que le bind mount dans Compose masque le dossier de l'image à l'exécution pour refléter immédiatement un nouveau `model.joblib` ré-entraîné (après simple redémarrage du service `api`, sans rebuild).

## Décision 2 : quels ports sont publiés : 8080 seulement, ou aussi 8001 ?

- **Votre choix :** dans le cadre de cet atelier de développement et de test, les deux ports sont publiés (`8080:80` pour Nginx et `8001:8000` pour FastAPI) ; en revanche, pour une cible de production, seul le port `8080` (ou `443` en HTTPS) de Nginx devrait être publié.
- **Ce que l'autre option ferait perdre :**
  - **Ne publier que `8080` (sans `8001`) en développement :** on perd l'accès direct depuis l'hôte Windows à la documentation interactive Swagger (`http://localhost:8001/docs`), au schéma OpenAPI (`/openapi.json`) et au débogage direct de FastAPI sans passer par le reverse proxy Nginx (puisque Nginx ne relaie ici que le préfixe `/api/`).
  - **Publier aussi `8001` en production :** un visiteur ou un attaquant peut contourner le point d'entrée unique Nginx en interrogeant directement le port `8001` de l'hôte. Il accède alors directement à Uvicorn/FastAPI (notamment à `/docs`, `/openapi.json`, `/health`, `/v1/...`), ce qui élargit la surface d'attaque et court-circuite tout filtrage, limitation de débit (rate limiting), journalisation centralisée ou terminaison TLS configurés sur Nginx.


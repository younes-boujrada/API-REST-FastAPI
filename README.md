# LogiAI : conteneuriser et déployer avec Docker, Nginx et Compose

Suite de l'Atelier 4 : l'API FastAPI LogiAI et sa page web sont conteneurisées et orchestrées avec **Docker Compose**. Nginx sert la page statique sur `http://localhost:8080` et relaie les appels `/api/` vers l'API FastAPI (`http://api:8000/`).

- Compte rendu complet : [COMPTE_RENDU.md](COMPTE_RENDU.md)
- Décisions d'architecture : [docs/adr/003-securite.md](docs/adr/003-securite.md) et [docs/adr/004-docker.md](docs/adr/004-docker.md)

## Vos clés (fichier `.env`, jamais dans Git ni dans l'image)

    copy .env.example .env            # macOS / Linux : cp .env.example .env
    # puis ouvrez .env et choisissez deux clés différentes (LOGIAI_API_KEY et LOGIAI_ADMIN_KEY)

Le fichier `.env` est ignoré par Git (`.gitignore`) et par le contexte de build Docker (`.dockerignore`). Il est injecté à l'exécution via `env_file` dans `docker-compose.yml`.

## Démarrer avec Docker Compose (une seule commande)

    docker compose config
    docker compose up -d --build
    docker compose ps

- **Page web (Nginx) :** `http://localhost:8080` (appelle `/api/v1/predict` sur la même origine, relayé vers `http://api:8000/v1/predict`)
- **API directe (FastAPI) :** `http://localhost:8001/health` et Swagger sur `http://localhost:8001/docs`
- **Arrêter / relancer / nettoyer :**
  - `docker compose stop` / `docker compose start`
  - `docker compose down`

## Exécution locale hors Docker (Atelier 4)

    python -m venv .venv
    .venv\Scripts\activate.bat        # PowerShell : .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python -m logiai.dataset
    python -m logiai.train
    python -m uvicorn logiai.api.main:app --reload

## Tester et vérifier la qualité

    python -m pytest
    ruff check .
    ruff format --check .

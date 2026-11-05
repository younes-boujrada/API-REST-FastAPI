# LogiAI : tester, sécuriser et appeler l'API

Suite du TP précédent : l'API LogiAI est testée pour être cassée, protégée par une clé API, puis appelée par une page web. Le compte rendu complet est dans [COMPTE_RENDU.md](COMPTE_RENDU.md) et la décision de sécurité dans [docs/adr/003-securite.md](docs/adr/003-securite.md).

## Installation (une fois)

    python -m venv .venv
    .venv\Scripts\activate.bat        # Windows cmd  (PowerShell : .venv\Scripts\Activate.ps1)
    source .venv/bin/activate         # macOS / Linux
    pip install -r requirements.txt
    python -m logiai.dataset
    python -m logiai.train

## Vos clés (fichier .env, jamais dans Git)

    copy .env.example .env            # macOS / Linux : cp .env.example .env
    # puis ouvrez .env et choisissez deux clés différentes

Le fichier `.env` est ignoré par Git. `.env.example` est versionné avec des valeurs factices.

## Lancer

    python -m uvicorn logiai.api.main:app --reload          # l'API, port 8000
    python -m http.server 5500 --directory web              # la page web, dans un 2e terminal
    # ouvrez http://localhost:5500

- `GET /health` est public.
- `POST /v1/predict` exige une clé utilisateur ou administrateur dans `X-API-Key`.
- `GET /v1/model-info` est réservé à l'administrateur (403 avec une clé utilisateur).
- CORS autorise uniquement `http://localhost:5500` et `http://127.0.0.1:5500`.

## Tester

    python -m pytest
    ruff check .
    ruff format --check .

Les tests couvrent le cas nominal, les cinq requêtes refusées, les bornes de chaque champ, l'authentification (401), l'autorisation (403) et l'absence de configuration (échec sûr). Le projet ne contient plus les deux bugs de bornes : `heure_depart` est limité à 23 et `nb_arrets` refuse les valeurs négatives.

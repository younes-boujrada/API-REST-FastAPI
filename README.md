# API-REST-FastAPI — LogiAI

Projet d'API REST avec **FastAPI** pour la prédiction des retards de livraison logistique, intégrant la validation de données par **Pydantic**, une suite de tests unitaires avec **Pytest**, et une interface utilisateur interactive avec **Streamlit**.

## 📑 Compte Rendu du TP
Le rapport complet de l'atelier est disponible dans :
- [COMPTE_RENDU.md](COMPTE_RENDU.md) (Markdown)
- [Compte_Rendu_Atelier3_BOUJRADA_Younes.pdf](Compte_Rendu_Atelier3_BOUJRADA_Younes.pdf) (Document PDF)

## 🚀 Démarrage rapide

### 1. Installation
```bash
python -m venv .venv
# Sous Windows PowerShell :
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Données et Entraînement du modèle
```bash
python -m logiai.dataset
python -m logiai.train
```

### 3. Lancer l'API FastAPI
```bash
python -m uvicorn logiai.api.main:app --reload
```
- Documentation Swagger interactive : [http://localhost:8000/docs](http://localhost:8000/docs)
- Endpoint Healthcheck : [http://localhost:8000/health](http://localhost:8000/health)

### 4. Lancer le client Streamlit
```bash
streamlit run streamlit_app.py
```

### 5. Exécuter les tests unitaires
```bash
python -m pytest
```

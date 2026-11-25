# ADR 005 : Empaquetage Python de LogiAI

## 1. Pourquoi `>=` dans `pyproject.toml` et `==` dans `requirements.txt` ?
- **Choix retenu :** `pyproject.toml` déclare des bornes minimales (`>=`, ex. `pandas>=2.0`, `scikit-learn>=1.3`) pour la compatibilité du package réutilisable, tandis que `requirements.txt` fige les versions exactes (`==`) pour le déploiement reproductible (notamment dans l'image Docker).
- **Ce que l'autre choix ferait perdre :** figer avec `==` dans `pyproject.toml` provoquerait des conflits de dépendances dès qu'un collègue ou un autre projet installe `logiai` aux côtés d'autres bibliothèques ; à l'inverse, n'utiliser que `>=` en production (`requirements.txt`) ferait perdre la reproductibilité des builds (risque de régression silencieuse ou d'`InconsistentVersionWarning` lors du chargement de `model.joblib` par `scikit-learn`).

## 2. Le modèle fait-il partie du package, ou reste-t-il à côté (`models/`) ?
- **Choix retenu :** le modèle (`models/model.joblib` et `models/model_info.json`) reste en dehors du package Python (dans `models/`, localisé via `LOGIAI_HOME`).
- **Ce que l'autre choix ferait perdre :** inclure le modèle dans le wheel alourdirait l'archive distribuée, couplerait le cycle de vie du code à celui des données et obligerait à recompiler et rediffuser une nouvelle version du package à chaque ré-entraînement (`python -m logiai.train`), tout en empêchant la mise à jour à chaud via un volume Docker (`./models:/app/models`). En contrepartie, l'utilisateur final doit disposer du dossier `models/` et définir `LOGIAI_HOME`.


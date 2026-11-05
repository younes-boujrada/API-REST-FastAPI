# ADR 003 : sécurité de l'API LogiAI

## Décision 1 : où transmettre la clé (en-tête, URL ou corps) ?

- **Votre choix :** la clé est transmise dans l'en-tête HTTP `X-API-Key`.
- **Ce que l'autre option ferait perdre :**
  - Dans l'URL, la clé serait enregistrée dans les journaux du serveur, l'historique du navigateur, les proxies et l'en-tête `Referer`. Une simple capture d'écran ou un partage de lien suffirait à la divulguer.
  - Dans le corps, la clé serait mélangée aux données métier, recopiée dans les journaux applicatifs et les traces de débogage. Elle serait aussi plus difficile à retirer des exemples de requêtes.
  - L'en-tête sépare clairement le secret des données et permet au serveur de le vérifier avant même de lire le corps de la requête.

## Décision 2 : quelles origines autoriser (CORS) ? Une liste précise ou « * » ?

- **Votre choix :** une liste précise, `http://localhost:5500` et `http://127.0.0.1:5500`, avec les méthodes `GET`, `POST`, `OPTIONS` et les en-têtes `Content-Type`, `X-API-Key`.
- **Ce que l'autre option ferait perdre :**
  - Avec `*`, n'importe quel site pourrait faire lire à un navigateur les réponses de l'API. La clé resterait nécessaire, mais une page malveillante pourrait utiliser une clé volée ou inciter l'utilisateur à appeler l'API.
  - `*` interdit aussi l'envoi de cookies d'authentification (`allow_credentials`) et ne permet pas de restreindre les méthodes et les en-têtes réellement utiles.
  - Une liste précise applique le moindre privilège : seule l'origine du client web prévu peut lire les réponses. Le coût est qu'il faut modifier la configuration et redémarrer l'API pour ajouter une nouvelle origine.

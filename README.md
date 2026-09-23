# Masomo Plus — API Accounts

API Django REST pour la gestion des comptes utilisateurs. L’authentification repose sur des jetons DRF : les mots de passe ne sont jamais renvoyés par l’API.

## Démarrage

```bash
python manage.py migrate
python manage.py runserver
```

En développement, l’API est disponible à l’adresse `http://127.0.0.1:8000`.

## Authentification

Après une inscription ou une connexion réussie, l’API renvoie un jeton :

```json
{
  "token": "5a0…",
  "user": {
    "id": 1,
    "email": "amina@example.com",
    "first_name": "Amina"
  }
}
```

Pour toutes les routes protégées, ajouter cet en-tête :

```http
Authorization: Token 5a0…
```

> Le jeton est propre à un utilisateur. La déconnexion le supprime ; il faut ensuite se reconnecter pour en obtenir un nouveau.

## Endpoints

Base URL : `/user/`

| Méthode | Route | Authentification | Description |
| --- | --- | --- | --- |
| `POST` | `/user/auth/register/` | Non | Crée un compte et retourne un jeton. |
| `POST` | `/user/auth/login/` | Non | Connecte un utilisateur et retourne son jeton. |
| `POST` | `/user/auth/logout/` | Token | Révoque le jeton de l’utilisateur connecté. |
| `GET` | `/user/profile/` | Token | Retourne le profil de l’utilisateur connecté. |
| `PATCH` | `/user/profile/` | Token | Met à jour partiellement le profil connecté. |
| `GET` | `/user/users/` | Admin | Liste les utilisateurs. |
| `GET` | `/user/users/{id}/` | Admin | Consulte un utilisateur. |

Les routes de l’annuaire `/user/users/` sont volontairement en lecture seule et réservées à `is_staff=True`.

## Inscription

```bash
curl -X POST http://127.0.0.1:8000/user/auth/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "amina@example.com",
    "password": "Un-mot-de-passe-solide-2026!",
    "first_name": "Amina",
    "last_name": "Banda",
    "tel": "+260970000000",
    "sexe": "Femme"
  }'
```

Champs acceptés : `email`, `password`, `first_name`, `last_name`, `tel`, `photo` et `sexe`. `email` et `password` sont obligatoires. Les valeurs autorisées pour `sexe` sont `Homme` et `Femme`.

Les validateurs Django sont appliqués au mot de passe (longueur minimale, mot de passe courant, etc.). Une adresse e-mail déjà utilisée produit une réponse `400 Bad Request`.

## Connexion

```bash
curl -X POST http://127.0.0.1:8000/user/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "amina@example.com",
    "password": "Un-mot-de-passe-solide-2026!"
  }'
```

En cas d’identifiants invalides ou de compte désactivé, l’API répond `400 Bad Request` sans révéler d’information sensible.

## Profil

Lire son profil :

```bash
curl http://127.0.0.1:8000/user/profile/ \
  -H 'Authorization: Token VOTRE_TOKEN'
```

Mettre à jour certains champs :

```bash
curl -X PATCH http://127.0.0.1:8000/user/profile/ \
  -H 'Authorization: Token VOTRE_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "Amina",
    "tel": "+260971111111",
    "photo": "https://example.com/photos/amina.jpg"
  }'
```

La réponse n’expose jamais `password`, `is_staff`, `is_superuser`, les groupes ou les permissions.

## Déconnexion

```bash
curl -X POST http://127.0.0.1:8000/user/auth/logout/ \
  -H 'Authorization: Token VOTRE_TOKEN'
```

La réponse est `204 No Content`. Le même jeton ne permet plus d’accéder au profil.

## Vérification

```bash
python manage.py check
python manage.py test accounts -v 2
```

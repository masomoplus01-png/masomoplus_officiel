# Guide de déploiement du backend MASOMOPLUS

## 1. Objectif

Ce guide permet de mettre le backend Django REST Framework en production sur un serveur Linux, avec un proxy HTTP (Nginx) et une base PostgreSQL en production.

Le projet est configuré pour utiliser SQLite en mode debug et PostgreSQL quand `DEBUG = False`.

---

## 2. Pré-requis

- Python 3.11+ recommandé
- pip / virtualenv
- PostgreSQL (recommandé en prod)
- Nginx ou un reverse proxy équivalent
- Git
- compte serveur Linux avec accès SSH

Vérifier le fichier de configuration Django :

- `backend_masomoplus/settings.py`

Le projet utilise :
- `AUTH_USER_MODEL = 'accounts.User'`
- `TokenAuthentication` pour l’API
- `ALLOWED_HOSTS = ['*']` en local
- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`

---

## 3. Variables d’environnement de production

Créer un fichier `.env` côté serveur, par exemple :

```env
DEBUG=False
SECRET_KEY=remplacer-par-une-cle-secrete-forte
ALLOWED_HOSTS=example.com,www.example.com,127.0.0.1
DB_NAME=masomoplus
DB_USER=postgres
DB_PASSWORD=mot_de_passe_strong
DB_HOST=localhost
DB_PORT=5432
```

Important :
- `settings.py` lit ces variables seulement dans le bloc `else` de la configuration DB.
- Pour un vrai déploiement, il faut que `DEBUG` soit `False`.
- Le code actuel ne charge pas explicitement `CSRF_TRUSTED_ORIGINS`; si vous utilisez un domaine public, il faut le configurer dans `settings.py` ou via variables si vous le souhaitez.

---

## 4. Préparer l’environnement serveur

### 4.1 Cloner le projet

```bash
cd /srv
git clone <url-du-repo> backend_masomoplus
cd backend_masomoplus
```

### 4.2 Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

### 4.3 Installer les dépendances

S’il existe un fichier `requirements.txt` :

```bash
pip install -r requirements.txt
```

Sinon, installer au minimum les dépendances Django/DRF nécessaires au projet :

```bash
pip install django djangorestframework django-cors-headers python-dotenv pillow
```

---

## 5. Base de données PostgreSQL

### 5.1 Créer la base

```sql
CREATE DATABASE masomoplus;
CREATE USER postgres WITH PASSWORD 'mot_de_passe_strong';
ALTER ROLE postgres WITH SUPERUSER;
```

### 5.2 Vérifier la configuration Django

Dans `backend_masomoplus/settings.py`, le bloc PostgreSQL est déjà prévu :

```python
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT", "5432"),
            "OPTIONS": {
                "sslmode": "require",
                "channel_binding": "require",
            },
        }
    }
```

En production, il faut absolument :
- `DEBUG = False`
- une vraie base PostgreSQL
- des identifiants sécurisés

---

## 6. Migration et préparation du projet

Exécuter :

```bash
python manage.py migrate
python manage.py check
```

Créer un superadmin si nécessaire :

```bash
python manage.py createsuperuser
```

Pour les fichiers statiques :

```bash
python manage.py collectstatic --noinput
```

Si des fichiers médias sont nécessaires, vérifier les permissions du dossier `media/` :

```bash
mkdir -p media
chmod -R 755 media
```

---

## 7. Lancer le backend en production

### Option recommandée : Gunicorn

Installer Gunicorn si absent :

```bash
pip install gunicorn
```

Lancer le service :

```bash
gunicorn backend_masomoplus.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Exemple de commande de démarrage dans un système service type systemd :

```ini
[Unit]
Description=MasomoPlus Django API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/srv/backend_masomoplus
Environment="PATH=/srv/backend_masomoplus/venv/bin"
ExecStart=/srv/backend_masomoplus/venv/bin/gunicorn backend_masomoplus.wsgi:application --bind 0.0.0.0:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

Lancer :

```bash
sudo systemctl daemon-reload
sudo systemctl enable backend-masomoplus
sudo systemctl start backend-masomoplus
sudo systemctl status backend-masomoplus
```

---

## 8. Configuration Nginx

Exemple de configuration proxy :

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    client_max_body_size 100M;

    location /static/ {
        alias /srv/backend_masomoplus/static/;
    }

    location /media/ {
        alias /srv/backend_masomoplus/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Tester la config :

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 9. CORS et front-end

Le projet utilise `django-cors-headers` et `CorsMiddleware` dans `MIDDLEWARE`.

En production, configurez bien les origines autorisées selon votre front-end NestJS ou autre frontend.

Exemple dans `settings.py` (à adapter selon votre besoin) :

```python
CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
    "http://localhost:3000",
]
```

Sinon, si le front est derrière un proxy ou un sous-domaine, configurez les règles correspondantes lors de votre déploiement réel.

---

## 10. Sécurité de production

À vérifier avant mise en ligne :

- `DEBUG = False`
- `SECRET_KEY` unique et forte
- base PostgreSQL en prod
- `ALLOWED_HOSTS` restreint
- accès admin limité
- `HTTPS` activé via proxy ou certif CAT
- fichiers médias avec permissions correctes
- sauvegardes de la base
- journaux d’erreurs / logs

---

## 11. Vérification finale avant ouverture

Tester les éléments clés :

```bash
python manage.py check
python manage.py migrate
python manage.py test
```

Puis vérifier l’API avec un vrai token sur des endpoints protégés :

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/user/profile/
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/documents/
```

---

## 12. Checklist de déploiement

- [ ] `DEBUG=False`
- [ ] clé secrète générée
- [ ] environnement `.env` rempli
- [ ] PostgreSQL prêt
- [ ] migrations appliquées
- [ ] `collectstatic` exécuté
- [ ] Gunicorn ou autre WSGI démarré
- [ ] Nginx en proxy
- [ ] HTTPS actif
- [ ] CORS configuré
- [ ] media/static permissions OK
- [ ] tests Django validés
- [ ] token auth fonctionnel

---

## 13. Points importants

- Le projet est bien orienté API DRF, mais il n’est pas encore un modèle de déploiement complet prêt pour production sans quelques ajustements serveur et sécurité.
- La base SQLite est utile pour le développement, mais il est fortement recommandé d’utiliser PostgreSQL en production.
- Les uploads de fichiers et les médias doivent être servis par le reverse proxy ou un stockage durable selon l’infrastructure choisie.
- Les valeurs CORS et domaines doivent être adaptées à l’environnement réel de production.

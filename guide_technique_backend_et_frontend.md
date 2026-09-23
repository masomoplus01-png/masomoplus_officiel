# Guide technique backend Django REST + frontend NestJS

## 1) Lancement du backend

### Démarrage

```bash
cd /media/anderson/Nouveau_nom/Programmation/JOB-2026/proffetionel/backend_Masomoplus/backend_masomoplus
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### URL de base

```text
http://127.0.0.1:8000
```

### Configuration utile

Le projet Django contient :
- `AUTH_USER_MODEL = 'accounts.User'`
- `TokenAuthentication` activé dans DRF
- `DEFAULT_PERMISSION_CLASSES = ['rest_framework.permissions.IsAuthenticated']`
- `MEDIA_URL = "/media/"`
- `MEDIA_ROOT = BASE_DIR / "media"`
- `ALLOWED_HOSTS = ['*']`
- `corsheaders` est installé et `CorsMiddleware` est présent dans `MIDDLEWARE`

Important : il n’y a pas de whitelist CORS explicite visible dans `settings.py`. À vérifier côté frontend / proxy si nécessaire.

---

## 2) Authentification

### Méthode utilisée

Le backend utilise le système de jetons DRF : `TokenAuthentication`.

### Endpoint de connexion

```http
POST /user/auth/login/
Content-Type: application/json
```

```json
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

### Réponse attendue

```json
{
  "token": "<token_string>",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Test",
    "last_name": "User",
    "tel": null,
    "photo": "https://kamatboost.com",
    "sexe": null,
    "date_joined": "2026-09-23T12:00:00Z"
  }
}
```

### Envoi du token dans les requêtes

```http
Authorization: Token <token>
```

Exemple :

```bash
curl -H "Authorization: Token abcdef123456" http://127.0.0.1:8000/user/profile/
```

### Inscription / logout

```http
POST /user/auth/register/
POST /user/auth/logout/
```

`/user/auth/logout/` supprime le token actuel pour l’utilisateur authentifié.

---

## 3) Endpoints principaux

### 3.1 Comptes / profil

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/user/auth/register/` | POST | Non | Crée un compte et renvoie un token |
| `/user/auth/login/` | POST | Non | Connecte un utilisateur |
| `/user/auth/logout/` | POST | Token | Déconnecte l’utilisateur |
| `/user/profile/` | GET/PATCH | Token | Profil utilisateur |
| `/user/users/` | GET | Admin | Liste des utilisateurs |

Paramètres principaux :
- `email`, `password`, `first_name`, `last_name`, `tel`, `photo`, `sexe`

Réponse type :
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "Test",
  "last_name": "User",
  "tel": null,
  "photo": "https://kamatboost.com",
  "sexe": null,
  "date_joined": "2026-09-23T12:00:00Z"
}
```

### 3.2 Annuaire académique

Routes réelles :

```text
/api/academic/facultes/
/api/academic/departements/
/api/academic/filieres/
/api/academic/categories/
```

Méthodes : `GET`, `POST`, `GET/{id}`, `PATCH/{id}` selon le ViewSet standard.

Paramètres principaux :
- `facultes`: `code_faculte`, `nom`, `déscription`
- `departements`: `code_departement`, `nom`, `déscription`, `faculte`
- `filieres`: `code_filiere`, `nom`, `déscription`, `département`
- `categories`: `code_categorie`, `nom`, `déscription`

### 3.3 Documents

Base :
```text
/api/documents/
```

Routes réelles :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/documents/` | GET | Token | Liste les documents |
| `/api/documents/` | POST | Token | Crée un document |
| `/api/documents/{id}/` | GET | Token | Détail |
| `/api/documents/{id}/` | PATCH | Token | Modification |
| `/api/documents/{id}/` | DELETE | Token | Suppression |
| `/api/documents/{id}/status/` | PATCH | Token | Change `statut` |
| `/api/documents/search/?q=...` | GET | Token | Recherche textuelle |

Paramètres principaux :
- `code_document`, `titre`, `resume`, `mots_cles`, `fichier` (PDF requis), `couverture` (image JPG/JPEG/PNG/WEBP), `annee_publication`, `langue`, `nombre_pages`, `statut`, `id_categorie`, `id_filiere`

Filtres disponibles :
- `categorie=<id>`
- `filiere=<id>`
- `annee=<année>`
- `statut=<statut>`
- `auteur=<id>`

Recherche :
```http
GET /api/documents/search/?q=memoires
```

Réponse type (document) :
```json
{
  "id_document": 1,
  "code_document": "DOC001",
  "titre": "Mon mémoire",
  "resume": "Résumé",
  "mots_cles": "ai, django",
  "fichier": "/media/documents/pdfs/mon-memoire.pdf",
  "couverture": null,
  "annee_publication": 2026,
  "langue": "fr",
  "nombre_pages": 120,
  "statut": "Brouillon",
  "date_depot": "2026-09-23T12:00:00Z",
  "id_categorie": 1,
  "id_filiere": 2,
  "id_utilisateur": 5
}
```

Permissions :
- auteur du document ou staff peuvent modifier le statut / document
- lecture selon DRF + permissions métier

### 3.4 Auteurs

Routes réelles :

```text
/api/authors/auteurs/
/api/authors/auteurs/{id}/
/api/authors/document-auteurs/
/api/authors/document-auteurs/{id}/
/api/authors/document-auteurs/{id}/update-role/
/api/authors/document-auteurs/{id}/remove/
```

Paramètres principaux :
- `Auteur`: `code_auteur`, `nom`, `postnom`, `prenom`, `email`, `affiliation`, `biographie`, `orcid`
- `DocumentAuteur`: `id_document`, `id_auteur`, `ordre_auteur`, `role_auteur`

Rôles autorisés :
- `Auteur`, `Co-auteur`, `Directeur`, `Encadreur`

### 3.5 Modération / validation

Base :
```text
/api/moderation/
```

Routes réelles :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/moderation/` | GET/POST | Staff | Liste / créer validation |
| `/api/moderation/{id}/` | GET/PATCH/DELETE | Staff | Détails |
| `/api/moderation/{id}/accept/` | POST | Staff | Accepte la validation |
| `/api/moderation/{id}/reject/` | POST | Staff | Rejette la validation |
| `/api/moderation/{id}/archive/` | POST | Staff | Archive la validation |
| `/api/moderation/document/?document_id=...` | GET | Auth | Validations d’un document |

Paramètres principaux :
- `code_validation`, `id_document`, `decision`, `commentaire`

Décisions autorisées selon workflow :
- `Brouillon` → `En attente`
- `En attente` → `Accepté` ou `Rejeté`
- `Accepté` → `Archivé`

### 3.6 Interactions

Base :
```text
/api/interactions/
```

Routes :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/interactions/telechargements/` | GET/POST | Token | Téléchargements |
| `/api/interactions/telechargements/{id}/` | GET/DELETE | Token | Détail |
| `/api/interactions/consultations/` | GET/POST | Token | Consultations |
| `/api/interactions/consultations/{id}/` | GET/DELETE | Token | Détail |
| `/api/interactions/favoris/` | GET/POST | Token | Favoris de l’utilisateur |
| `/api/interactions/favoris/{id}/` | GET/DELETE | Token | Favori |
| `/api/interactions/commentaires/` | GET/POST | Token | Commentaires |
| `/api/interactions/commentaires/{id}/` | GET/PATCH/DELETE | Token | Commentaire |

Paramètres principaux :
- `id_document`, `contenu`, `adresse_ip`, `appareil`

Important :
- les favoris visibles sont filtrés par `id_utilisateur` connecté
- les commentaires sont protégés : un utilisateur ne peut modifier/supprimer que ses propres commentaires

### 3.7 Analytics

Route réelle :
```text
GET /api/analytics/
```

Réponse type :
```json
{
  "nombre_documents": 12,
  "nombre_telechargements": 8,
  "nombre_consultations": 25,
  "nombre_favoris": 10,
  "nombre_publications": 6
}
```

Permissions : authentification requise.

### 3.8 Collaboration

Base :
```text
/api/projets/
```

Routes réelles :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/projets/` | GET/POST | Token | Liste / créer projet |
| `/api/projets/{id}/` | GET/PATCH/DELETE | Token | Détail / mise à jour / suppression |

Paramètres principaux :
- `code_projet`, `titre`, `description`, `domaine`, `statut`

Important :
- l’utilisateur n’est autorisé à modifier/supprimer que ses propres projets, sauf staff

### 3.9 Notifications

Base :
```text
/api/notifications/
```

Routes réelles :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/notifications/` | GET/POST | Token | Liste / création |
| `/api/notifications/{id}/` | GET/PATCH | Token | Détail / mise à jour |
| `/api/notifications/{id}/read/` | PATCH | Token | Marque la notification comme lue |

Paramètres :
- `code_notification`, `titre`, `contenu`, `type`, `lu`

Types acceptés :
- `Validation`
- `Nouveau document`
- `Commentaire`
- `Collaboration`
- `Système`

Important :
- l’utilisateur ne voit que ses propres notifications

### 3.10 Support

Base :
```text
/api/support/
```

Routes réelles :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/support/` | GET/POST | Token | Liste / créer ticket |
| `/api/support/{id}/` | GET/PATCH | Token | Détail / mise à jour |

Paramètres principaux :
- `code_support`, `sujet`, `message`, `statut`

Statuts supportés :
- `Ouvert`, `En cours`, `Résolu`, `Fermé`

Le modèle contient `date_resolution` nullable. La date est renseignée côté backend quand le statut est marqué comme résolu.

### 3.11 Actualités

Base :
```text
/api/actualites/
```

Routes réelles :

| Route | Méthode | Auth | Description |
| --- | --- | --- | --- |
| `/api/actualites/` | GET/POST | Token | Liste / création |
| `/api/actualites/{id}/` | GET/PATCH/DELETE | Token | Détail / mise à jour / suppression |

Paramètres principaux :
- `code_actualite`, `titre`, `contenu`, `image`

Important :
- `image` est un champ upload de fichier (`ImageField`)
- l’auteur de l’actualité est automatiquement lié à l’utilisateur authentifié

---

## 4) Tests API

### 4.1 Login

```bash
curl -X POST http://127.0.0.1:8000/user/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "StrongPass123!"
  }'
```

### 4.2 Liste des documents avec filtres

```bash
curl -H "Authorization: Token <token>" \
  "http://127.0.0.1:8000/api/documents/?categorie=1&filiere=2&statut=Validé"
```

Recherche textuelle :

```bash
curl -H "Authorization: Token <token>" \
  "http://127.0.0.1:8000/api/documents/search/?q=memoires"
```

### 4.3 Création de document (upload PDF)

```bash
curl -X POST http://127.0.0.1:8000/api/documents/ \
  -H "Authorization: Token <token>" \
  -F "code_document=DOC123" \
  -F "titre=Mon nouveau mémoire" \
  -F "resume=Résumé du mémoire" \
  -F "mots_cles=django, rest, api" \
  -F "annee_publication=2026" \
  -F "id_categorie=1" \
  -F "id_filiere=2" \
  -F "fichier=@/chemin/vers/memoire.pdf"
```

`fichier` doit être un PDF. Si `couverture` est fournie, elle doit être JPG/JPEG/PNG/WEBP.

### 4.4 Mise à jour du statut d’un document

```bash
curl -X PATCH http://127.0.0.1:8000/api/documents/12/status/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "statut": "Validé"
  }'
```

### 4.5 Validation de document (modération)

```bash
curl -X POST http://127.0.0.1:8000/api/moderation/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "code_validation": "VAL001",
    "id_document": 12,
    "decision": "Accepté",
    "commentaire": "OK"
  }'
```

Action dédiée :

```bash
curl -X POST http://127.0.0.1:8000/api/moderation/5/accept/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "commentaire": "Bonne pièce"
  }'
```

### 4.6 Téléchargement / consultation / favori

Téléchargement :

```bash
curl -X POST http://127.0.0.1:8000/api/interactions/telechargements/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id_document": 12,
    "adresse_ip": "127.0.0.1",
    "appareil": "Chrome"
  }'
```

Consultation :

```bash
curl -X POST http://127.0.0.1:8000/api/interactions/consultations/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id_document": 12
  }'
```

Favori :

```bash
curl -X POST http://127.0.0.1:8000/api/interactions/favoris/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id_document": 12
  }'
```

### 4.7 Commentaires

Créer :

```bash
curl -X POST http://127.0.0.1:8000/api/interactions/commentaires/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id_document": 12,
    "contenu": "Très bon document"
  }'
```

Modifier :

```bash
curl -X PATCH http://127.0.0.1:8000/api/interactions/commentaires/4/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "contenu": "Nouvelle version du commentaire"
  }'
```

### 4.8 Notifications

Liste :

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/notifications/
```

Marquer comme lue :

```bash
curl -X PATCH http://127.0.0.1:8000/api/notifications/3/read/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json"
```

### 4.9 Statistiques

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/analytics/
```

---

## 5) Intégration NestJS

### 5.1 Configuration de l’URL backend

Dans `.env` :

```env
BACKEND_API_URL=http://127.0.0.1:8000
```

Exemple de config NestJS :

```ts
export const config = {
  backendUrl: process.env.BACKEND_API_URL || 'http://127.0.0.1:8000',
};
```

### 5.2 Service HTTP centralisé

```ts
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

export class BackendHttpService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.BACKEND_API_URL || 'http://127.0.0.1:8000',
      timeout: 20000,
    });

    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('masomoplus_token');
      if (token) {
        config.headers = {
          ...config.headers,
          Authorization: `Token ${token}`,
        };
      }
      return config;
    });
  }

  get<T>(url: string, config?: AxiosRequestConfig) {
    return this.client.get<T>(url, config);
  }

  post<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.client.post<T>(url, data, config);
  }

  patch<T>(url: string, data?: any, config?: AxiosRequestConfig) {
    return this.client.patch<T>(url, data, config);
  }

  delete<T>(url: string, config?: AxiosRequestConfig) {
    return this.client.delete<T>(url, config);
  }
}
```

### 5.3 Gestion du token

- Stocker le token après `/user/auth/login/`
- Le réinjecter dans chaque requête via interceptor HTTP
- Supprimer le token au logout

Exemple :

```ts
const login = async (email: string, password: string) => {
  const { data } = await axios.post('http://127.0.0.1:8000/user/auth/login/', {
    email,
    password,
  });

  localStorage.setItem('masomoplus_token', data.token);
  return data;
};
```

### 5.4 Gestion des erreurs

Le backend répond généralement avec :
- `400 Bad Request` pour validation métier / mauvais payload
- `401 Unauthorized` si token absent/invalid
- `403 Forbidden` si permission refusée
- `404 Not Found` si ressource absente

Exemple NestJS :

```ts
try {
  const response = await backendHttp.get('/api/documents/');
  return response.data;
} catch (error: any) {
  if (error.response?.status === 401) {
    // token perdu ou invalide
  }
  if (error.response?.status === 403) {
    // permission refusée
  }
  console.error(error.response?.data || error.message);
  throw error;
}
```

### 5.5 Pagination et filtres

Le backend DRF a pagination globale activée (`PageNumberPagination`). Les listes retournent souvent :

```json
{
  "count": 26,
  "next": "http://127.0.0.1:8000/api/documents/?page=2",
  "previous": null,
  "results": [
    { "id_document": 1, "titre": "Mon document" }
  ]
}
```

Donc côté NestJS, traiter:

```ts
const data = response.data;
const items = data.results ?? data;
```

Filtres disponibles côté documents :
- `categorie`, `filiere`, `annee`, `statut`, `auteur`
- recherche : `?q=...` sur `/api/documents/search/`

### 5.6 Upload de fichiers

Pour les documents :

```ts
const formData = new FormData();
formData.append('code_document', 'DOC123');
formData.append('titre', 'Mon mémoire');
formData.append('resume', 'Résumé');
formData.append('annee_publication', '2026');
formData.append('id_categorie', '1');
formData.append('id_filiere', '2');
formData.append('fichier', file);

await axios.post('http://127.0.0.1:8000/api/documents/', formData, {
  headers: {
    Authorization: `Token ${token}`,
    'Content-Type': 'multipart/form-data',
  },
});
```

Les fichiers PDF sont autorisés uniquement pour `fichier` ; les images pour `couverture` doivent être `.jpg`, `.jpeg`, `.png` ou `.webp`.

### 5.7 Variables `.env`

```env
BACKEND_API_URL=http://127.0.0.1:8000
AUTH_TOKEN_KEY=masomoplus_token
```

---

## 6) Checklist finale

- [ ] Authentification fonctionnelle via `TokenAuthentication`
- [ ] Login / logout testés
- [ ] Tokens envoyés dans l’header `Authorization: Token ...`
- [ ] Permissions vérifiées sur documents, commentaires, notifications, projets, support, actualités
- [ ] Endpoints principaux testés (`documents`, `academic`, `authors`, `moderation`, `interactions`, `analytics`, `projets`, `notifications`, `support`, `actualites`)
- [ ] Upload PDF / images validés
- [ ] CORS vérifié en environnement local et prod
- [ ] Intégration NestJS validée pour appels HTTP + token + erreurs

---

## 7) Points importants à retenir

- Ne pas inventer d’endpoint.
- Les vraies routes du backend sont celles listées ci-dessus.
- Les réponses paginées utilisent le format DRF standard quand la liste est retournée par ViewSet.
- Les permissions métier sont strictes sur les objets dont l’utilisateur n’est pas propriétaire.
- Le backend ne fournit pas de schéma OpenAPI automatique dans le code visible, donc le frontend doit s’appuyer sur ces routes réelles et sur les payloads mentionnés ici.

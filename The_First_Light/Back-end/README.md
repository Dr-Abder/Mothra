# 🦋 Mothra API - Back-end

API RESTful sécurisée pour la détection des maladies de la peau par Intelligence Artificielle.

## 🚀 Démarrage rapide

### 1. Installation des dépendances

```bash
cd The_First_Light/Back-end
pip install -r requirements.txt
```

### 2. Configuration de la base de données

Assurez-vous que PostgreSQL est démarré :

```bash
sudo service postgresql start
```

La base `mothra_db` sera créée automatiquement au premier lancement.

### 3. Lancer l'API

```bash
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : **http://localhost:8000**

Documentation interactive : **http://localhost:8000/docs**

---

## 📚 Documentation API

### 🔐 Authentication (`/api/v1/auth`)

| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/signup` | Créer un compte utilisateur |
| POST | `/login` | Connexion (retourne JWT) |
| POST | `/logout` | Déconnexion |

### 👤 Users (`/api/v1/users`)

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| GET | `/me` | Voir mon profil | ✅ |
| PUT | `/me` | Modifier mon profil | ✅ |
| DELETE | `/me` | Supprimer mon compte (RGPD) | ✅ |
| GET | `/me/data-export` | Exporter mes données (RGPD) | ✅ |
| DELETE | `/me/analyses` | Supprimer toutes mes analyses | ✅ |

### 📊 Analyses (`/api/v1/analyses`)

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| POST | `` | Créer une analyse | ✅ |
| GET | `` | Lister mes analyses | ✅ |
| GET | `/{id}` | Voir une analyse | ✅ |
| DELETE | `/{id}` | Supprimer une analyse | ✅ |

### 🤖 Prediction (`/api/v1/predict`)

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| POST | `` | Upload image + prédiction | ✅ |

### ℹ️ Informations

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/v1/model` | Info sur le modèle Mothra |
| GET | `/api/v1/projects/mothra-v2` | Info sur Mothra V2 |
| GET | `/api/v1/legal/rgpd` | Politique RGPD |

---

## 🔒 Authentification

Toutes les routes protégées nécessitent un token JWT dans le header :

```http
Authorization: Bearer <votre_token_jwt>
```

### Exemple de workflow

1. **Inscription**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean@example.com",
    "password": "SecurePass@123",
    "age": 30,
    "sex": "homme",
    "consent_rgpd": true
  }'
```

2. **Connexion**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jean@example.com",
    "password": "SecurePass@123"
  }'
```

Réponse :
```json
{
  "access_token": "eyJhbGc....",
  "token_type": "bearer",
  "user_id": "uuid-here"
}
```

3. **Utiliser le token**
```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer eyJhbGc...."
```

---

## 📁 Structure du projet

```
Back-end/
├── app/
│   ├── main.py              # Application FastAPI principale
│   ├── schemas.py           # Schémas Pydantic (validation)
│   ├── auth_utils.py        # Utilitaires JWT
│   ├── api/                 # Routes API
│   │   ├── auth.py          # Authentification
│   │   ├── users.py         # Gestion utilisateur
│   │   ├── analyses.py      # Gestion analyses
│   │   └── predict.py       # Prédiction ML
│   └── models/              # Modèles de données
│       ├── DBHandler.py     # Gestionnaire BDD
│       ├── User.py          # Modèle User
│       ├── Analyse.py       # Modèle Analyse
│       └── test_models.py   # Tests des modèles
└── requirements.txt         # Dépendances Python
```

---

## ✅ Tests

### Tester les modèles de données

```bash
cd app/models
python test_models.py
```

### Tester l'API avec Swagger UI

Accédez à : **http://localhost:8000/docs**

---

## 🛡️ Sécurité

- ✅ Mots de passe hashés avec **bcrypt**
- ✅ Authentification **JWT** (expiration 30 min)
- ✅ Validation des données avec **Pydantic**
- ✅ Protection **CORS** configurée
- ✅ Isolation des données utilisateur
- ✅ **CASCADE DELETE** pour RGPD
- ✅ Validation upload (taille max 10MB, formats autorisés)

---

## 🗄️ Base de données

### Tables

**users**
- id (UUID, PK)
- first_name, last_name
- email (unique)
- password_hash
- age, sex
- created_at, updated_at

**analyses**
- id (UUID, PK)
- user_id (FK → users.id, CASCADE DELETE)
- photo (URL/nom fichier)
- diagnostic (text)
- confidence (0.0-1.0)
- created_at

---

## 📝 Conformité RGPD

✅ **Droit d'accès** : `GET /api/v1/users/me`

✅ **Droit de rectification** : `PUT /api/v1/users/me`

✅ **Droit à l'effacement** : `DELETE /api/v1/users/me`

✅ **Droit à la portabilité** : `GET /api/v1/users/me/data-export`

---

## 🚧 TODO

- [ ] Intégrer le vrai modèle ML (remplacer le mock dans predict.py)
- [ ] Stocker les images sur S3/MinIO
- [ ] Implémenter le blacklist JWT pour logout
- [ ] Ajouter rate limiting
- [ ] Logger les actions critiques
- [ ] Mettre SECRET_KEY dans variables d'environnement
- [ ] Configurer SSL/TLS en production
- [ ] Restreindre CORS en production

---

## 📞 Support

Pour toute question : **support@mothra-health.com**

---

**Made with ❤️ by the Mothra Team**

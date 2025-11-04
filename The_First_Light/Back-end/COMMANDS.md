# 📋 TOUTES LES COMMANDES MOTHRA API

## 🗄️ POSTGRESQL - BASE DE DONNÉES

### Démarrer/Arrêter PostgreSQL
```bash
# Démarrer PostgreSQL
sudo service postgresql start

# Vérifier le status
sudo service postgresql status

# Arrêter PostgreSQL
sudo service postgresql stop

# Redémarrer PostgreSQL
sudo service postgresql restart
```

### Se connecter à PostgreSQL
```bash
# Se connecter en tant que postgres
sudo -u postgres psql

# Se connecter directement à la base mothra_db
sudo -u postgres psql -d mothra_db
```

### Commandes SQL utiles

#### Créer la base manuellement (optionnel, l'API le fait auto)
```sql
-- Se connecter à PostgreSQL
sudo -u postgres psql

-- Créer la base de données
CREATE DATABASE mothra_db;

-- Se connecter à la base
\c mothra_db

-- Créer les tables (déjà fait par l'API)
CREATE TABLE IF NOT EXISTS users(
    id UUID PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    age INTEGER NOT NULL,
    sex VARCHAR (10) NOT NULL,
    skin_type VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analyses(
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    photo TEXT NOT NULL,
    diagnostic TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### Voir les données
```sql
-- Lister toutes les bases de données
\l

-- Se connecter à mothra_db
\c mothra_db

-- Lister toutes les tables
\dt

-- Voir la structure d'une table
\d users
\d analyses

-- Compter les utilisateurs
SELECT COUNT(*) FROM users;

-- Voir tous les utilisateurs
SELECT id, first_name, last_name, email, created_at FROM users;

-- Voir toutes les analyses
SELECT id, user_id, diagnostic, confidence, created_at FROM analyses;

-- Voir les analyses d'un utilisateur spécifique
SELECT * FROM analyses WHERE user_id = 'UUID_ICI';

-- Joindre users et analyses
SELECT
    u.first_name,
    u.last_name,
    a.diagnostic,
    a.confidence,
    a.created_at
FROM users u
LEFT JOIN analyses a ON u.id = a.user_id
ORDER BY a.created_at DESC;
```

#### Supprimer des données
```sql
-- Supprimer toutes les analyses
DELETE FROM analyses;

-- Supprimer tous les utilisateurs (et leurs analyses via CASCADE)
DELETE FROM users;

-- Supprimer un utilisateur spécifique
DELETE FROM users WHERE email = 'email@example.com';

-- Supprimer une analyse spécifique
DELETE FROM analyses WHERE id = 'UUID_ICI';
```

#### Réinitialiser complètement la base
```sql
-- Supprimer la base
DROP DATABASE IF EXISTS mothra_db;

-- Recréer la base
CREATE DATABASE mothra_db;
```

#### Quitter PostgreSQL
```sql
\q
```

---

## 🐍 PYTHON - INSTALLATION ET GESTION

### Installation des dépendances
```bash
# Aller dans le dossier Back-end
cd /workspaces/Mothra/The_First_Light/Back-end

# Installer les dépendances
pip install -r requirements.txt

# Vérifier les packages installés
pip list | grep -E 'fastapi|uvicorn|psycopg2|jose|bcrypt'
```

---

## 🧪 TESTS

### Tester les modèles de données
```bash
# Aller dans le dossier models
cd /workspaces/Mothra/The_First_Light/Back-end/app/models

# Lancer les tests
python test_models.py
```

### Tester la migration CASCADE
```bash
cd /workspaces/Mothra/The_First_Light/Back-end/app/models
python migrate_cascade.py
```

---

## 🚀 LANCER L'API

### Méthode 1: Script automatique (recommandé)
```bash
cd /workspaces/Mothra/The_First_Light/Back-end
./start_api.sh
```

### Méthode 2: Manuelle
```bash
# Démarrer PostgreSQL
sudo service postgresql start

# Aller dans le dossier app
cd /workspaces/Mothra/The_First_Light/Back-end/app

# Lancer l'API
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Méthode 3: Sans reload (production)
```bash
cd /workspaces/Mothra/The_First_Light/Back-end/app
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Arrêter l'API
```bash
# Ctrl + C dans le terminal où l'API tourne
# Ou trouver le processus et le tuer
ps aux | grep uvicorn
kill -9 <PID>
```

---

## 🌐 ACCÉDER À L'API

### URLs importantes
```
API principale        : http://localhost:8000
Documentation Swagger : http://localhost:8000/docs
Documentation Redoc   : http://localhost:8000/redoc
Health check         : http://localhost:8000/health
Info modèle          : http://localhost:8000/api/v1/model
```

---

## 🧪 TESTER L'API AVEC CURL

### 1. Inscription (Signup)
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jean",
    "last_name": "Dupont",
    "email": "jean.dupont@example.com",
    "password": "SecurePass@123",
    "age": 30,
    "sex": "homme",
    "consent_rgpd": true
  }'
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "uuid-here"
}
```

### 2. Connexion (Login)
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jean.dupont@example.com",
    "password": "SecurePass@123"
  }'
```

### 3. Voir mon profil (nécessite TOKEN)
```bash
# Remplace TOKEN par le token JWT reçu
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer TOKEN"
```

### 4. Créer une analyse
```bash
curl -X POST http://localhost:8000/api/v1/analyses \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "photo": "scan_peau_001.jpg",
    "diagnostic": "Mélanome détecté",
    "confidence": 0.92
  }'
```

### 5. Lister mes analyses
```bash
curl -X GET http://localhost:8000/api/v1/analyses \
  -H "Authorization: Bearer TOKEN"
```

### 6. Upload d'image pour prédiction
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@/path/to/image.jpg"
```

### 7. Export de données (RGPD)
```bash
curl -X GET http://localhost:8000/api/v1/users/me/data-export \
  -H "Authorization: Bearer TOKEN"
```

### 8. Supprimer mon compte (RGPD)
```bash
curl -X DELETE http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer TOKEN"
```

---

## 🧪 TESTER L'API AVEC PYTHON

### Script de test complet
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Inscription
signup_data = {
    "first_name": "Marie",
    "last_name": "Martin",
    "email": "marie.martin@test.com",
    "password": "TestPass@123",
    "age": 25,
    "sex": "femme",
    "consent_rgpd": True
}

response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
print("Signup:", response.json())
token = response.json()["access_token"]

# 2. Headers avec le token
headers = {"Authorization": f"Bearer {token}"}

# 3. Voir mon profil
response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
print("Profile:", response.json())

# 4. Créer une analyse
analyse_data = {
    "photo": "test_image.jpg",
    "diagnostic": "Test diagnostic",
    "confidence": 0.85
}
response = requests.post(f"{BASE_URL}/api/v1/analyses", json=analyse_data, headers=headers)
print("Analyse créée:", response.json())

# 5. Lister les analyses
response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
print("Mes analyses:", response.json())

# 6. Export de données
response = requests.get(f"{BASE_URL}/api/v1/users/me/data-export", headers=headers)
print("Export:", response.json())
```

### Sauvegarder ce script
```bash
# Créer le fichier
cat > /workspaces/Mothra/The_First_Light/Back-end/test_api.py << 'EOF'
# (Coller le script ci-dessus)
EOF

# Lancer le test
python test_api.py
```

---

## 📊 MONITORING ET LOGS

### Voir les logs de l'API en temps réel
```bash
# L'API affiche les logs dans le terminal où elle tourne
# Pour sauvegarder les logs dans un fichier:
uvicorn main:app --reload --host 0.0.0.0 --port 8000 > api.log 2>&1 &

# Voir les logs en temps réel
tail -f api.log
```

### Vérifier la santé de l'API
```bash
curl http://localhost:8000/health
```

### Vérifier les processus
```bash
# Voir les processus Python/Uvicorn
ps aux | grep uvicorn

# Voir les processus PostgreSQL
ps aux | grep postgres
```

---

## 🔧 DÉPANNAGE

### Problème: Port déjà utilisé
```bash
# Voir quel processus utilise le port 8000
lsof -i :8000

# Tuer le processus
kill -9 <PID>
```

### Problème: PostgreSQL ne démarre pas
```bash
# Voir les logs PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-16-main.log

# Réinitialiser PostgreSQL
sudo service postgresql stop
sudo service postgresql start
```

### Problème: Erreur de connexion à la base
```bash
# Vérifier que PostgreSQL écoute
sudo netstat -plnt | grep 5432

# Vérifier les paramètres de connexion dans main.py
# Ligne 33-38
```

### Problème: Dépendances manquantes
```bash
# Réinstaller toutes les dépendances
pip install -r requirements.txt --force-reinstall
```

---

## 🧹 NETTOYAGE

### Nettoyer la base de données
```bash
# Supprimer toutes les données
sudo -u postgres psql -d mothra_db -c "DELETE FROM analyses; DELETE FROM users;"

# Ou via script Python
python -c "
from models.DBHandler import DBHandler
db = DBHandler('mothra_db', 'postgres', 'root', 'localhost', '5432')
db.connect()
db.execute('DELETE FROM analyses')
db.execute('DELETE FROM users')
print('✅ Base nettoyée')
db.disconnect()
"
```

### Supprimer la base complètement
```bash
sudo -u postgres psql -c "DROP DATABASE IF EXISTS mothra_db;"
```

---

## 📦 STRUCTURE COMPLÈTE DU PROJET

```
Back-end/
├── app/
│   ├── main.py                 # Application FastAPI
│   ├── schemas.py              # Validation Pydantic
│   ├── auth_utils.py           # JWT & Auth
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py             # Routes auth
│   │   ├── users.py            # Routes users
│   │   ├── analyses.py         # Routes analyses
│   │   └── predict.py          # Routes prediction
│   └── models/
│       ├── DBHandler.py        # Gestionnaire BDD
│       ├── User.py             # Modèle User
│       ├── Analyse.py          # Modèle Analyse
│       ├── test_models.py      # Tests
│       └── migrate_cascade.py  # Migration
├── requirements.txt            # Dépendances
├── README.md                   # Documentation
├── COMMANDS.md                 # Ce fichier
└── start_api.sh                # Script de démarrage
```

---

## 🎯 WORKFLOW COMPLET DE DÉVELOPPEMENT

### 1. Démarrage du projet
```bash
# Terminal 1: Démarrer PostgreSQL
sudo service postgresql start

# Terminal 2: Lancer l'API
cd /workspaces/Mothra/The_First_Light/Back-end/app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Développement
```bash
# Modifier les fichiers dans app/
# L'API se recharge automatiquement avec --reload
```

### 3. Tests
```bash
# Terminal 3: Tester l'API
curl http://localhost:8000/docs  # Ouvrir dans le navigateur
# Ou utiliser les commandes curl ci-dessus
```

### 4. Base de données
```bash
# Terminal 4: Monitorer la base
sudo -u postgres psql -d mothra_db
# Puis exécuter des requêtes SQL
```

---

## 🔐 VARIABLES D'ENVIRONNEMENT (PRODUCTION)

### Créer un fichier .env
```bash
cat > /workspaces/Mothra/The_First_Light/Back-end/.env << 'EOF'
# Base de données
DB_NAME=mothra_db
DB_USER=postgres
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=5432

# JWT
SECRET_KEY=votre-cle-secrete-ultra-securisee-changez-moi
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_HOST=0.0.0.0
API_PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
EOF
```

### Charger les variables d'environnement
```python
# Dans main.py, ajouter:
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "mothra_db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
```

---

## ✅ CHECKLIST DE VÉRIFICATION

Avant de démarrer l'API, vérifier :

- [ ] PostgreSQL est démarré
- [ ] La base `mothra_db` existe (ou sera créée auto)
- [ ] Les dépendances Python sont installées
- [ ] Le port 8000 est libre
- [ ] Les modèles User et Analyse sont OK

---

**Toutes les commandes sont prêtes ! 🚀**

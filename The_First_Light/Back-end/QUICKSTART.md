# 🚀 QUICKSTART - API Mothra

Guide ultra-rapide pour démarrer en 5 minutes !

---

## ⚡ DÉMARRAGE RAPIDE (3 commandes)

```bash
# 1. Démarrer PostgreSQL
sudo service postgresql start

# 2. Installer les dépendances (première fois seulement)
cd /workspaces/Mothra/The_First_Light/Back-end
pip install -r requirements.txt

# 3. Lancer l'API
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**C'est tout ! 🎉**

Accédez à la documentation : **http://localhost:8000/docs**

---

## 🧪 TESTER L'API (3 commandes)

### Option 1: Avec le script de test automatique
```bash
cd /workspaces/Mothra/The_First_Light/Back-end
python test_api_quick.py
```

### Option 2: Avec curl (manuel)

**1. Inscription**
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"TestPass@123","age":25,"sex":"homme","consent_rgpd":true}'
```

**2. Connexion** (copie le token de la réponse)
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass@123"}'
```

**3. Voir mon profil** (remplace TOKEN)
```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer TOKEN"
```

---

## 📊 COMMANDES SQL UTILES

```bash
# Se connecter à la base
sudo -u postgres psql -d mothra_db

# Voir tous les utilisateurs
SELECT first_name, last_name, email FROM users;

# Voir toutes les analyses
SELECT diagnostic, confidence, created_at FROM analyses;

# Compter les utilisateurs
SELECT COUNT(*) FROM users;

# Quitter
\q
```

---

## 📁 FICHIERS IMPORTANTS

| Fichier | Description |
|---------|-------------|
| `COMMANDS.md` | **TOUTES les commandes détaillées** |
| `README.md` | Documentation complète de l'API |
| `test_api_quick.py` | Script de test automatique |
| `start_api.sh` | Script de démarrage automatique |
| `app/main.py` | Application FastAPI principale |
| `app/models/test_models.py` | Tests des modèles de données |

---

## 🎯 ROUTES PRINCIPALES

| Route | Description |
|-------|-------------|
| `/docs` | Documentation Swagger (interactive) |
| `/health` | Health check |
| `/api/v1/auth/signup` | Créer un compte |
| `/api/v1/auth/login` | Se connecter (JWT) |
| `/api/v1/users/me` | Mon profil |
| `/api/v1/analyses` | Mes analyses |
| `/api/v1/predict` | Upload image + prédiction |

---

## 🐛 PROBLÈMES COURANTS

### L'API ne démarre pas
```bash
# Vérifier que PostgreSQL tourne
sudo service postgresql status
sudo service postgresql start
```

### Port 8000 déjà utilisé
```bash
# Trouver et tuer le processus
lsof -i :8000
kill -9 <PID>
```

### Erreur de dépendances
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 POUR ALLER PLUS LOIN

- Voir **COMMANDS.md** pour toutes les commandes détaillées
- Voir **README.md** pour la documentation complète
- Tester avec **Swagger UI** : http://localhost:8000/docs

---

**Bon développement ! 🦋**

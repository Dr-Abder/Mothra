"""
Application FastAPI principale - Back-end Mothra
API RESTful sécurisée pour la détection des maladies de la peau
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os

from app.db.DBHandler import DBHandler
from app.models.User import User
from app.models.Analyse import Analyse

# Import des routers
from app.api import auth, users, analyses, predict, images

# Gestionnaire de base de données global
db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestionnaire du cycle de vie de l'application"""
    global db

    # Startup: Connexion à la base de données
    print("🚀 Démarrage de l'application Mothra...")
    db = DBHandler(
        dbname=os.getenv("DB_NAME", "mothra_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "root"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

    try:
        db.connect()
        print("✅ Connexion à la base de données réussie")

        # Créer les tables si elles n'existent pas
        db.create_tables()
        print("✅ Tables vérifiées/créées")

        # Lier la base de données aux modèles
        User.db = db
        Analyse.db = db
        print("✅ Modèles liés à la base de données")

    except Exception as e:
        print(f"❌ Erreur lors de la connexion à la base de données: {e}")
        raise

    yield

    # Shutdown: Déconnexion propre
    print("🛑 Arrêt de l'application...")
    if db:
        db.disconnect()
        print("✅ Déconnexion de la base de données")


# Créer l'application FastAPI
app = FastAPI(
    title="Mothra API",
    description="""
    API Back-end pour le projet Mothra - Détection des maladies de la peau par IA

    ## Fonctionnalités

    ### 🔐 Authentification
    - Inscription et connexion sécurisées avec JWT
    - Hash des mots de passe avec bcrypt

    ### 👤 Gestion utilisateur
    - CRUD complet du profil utilisateur
    - Conformité RGPD (export et suppression des données)

    ### 📊 Analyses
    - Création et gestion des diagnostics
    - Historique complet des analyses

    ### 🤖 Prédiction ML
    - Upload d'images pour diagnostic
    - Résultats avec niveau de confiance

    ## Sécurité
    - Authentification JWT obligatoire pour toutes les routes protégées
    - Validation des données avec Pydantic
    - Protection CORS configurée
    - Isolation des données utilisateur
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Dev local
        "https://mothra-n1mv6qmut-dr-abders-projects.vercel.app",  # Vercel preview
        "https://mothra-git-main-dr-abders-projects.vercel.app",  # Vercel production
        "https://*.vercel.app",  # Tous les déploiements Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(analyses.router, prefix="/api/v1/analyses", tags=["Analyses"])
app.include_router(predict.router, prefix="/api/v1/predict", tags=["Prediction"])
app.include_router(images.router, prefix="/api/v1/images", tags=["Images"])


@app.get("/")
async def root():
    """Route racine - Informations sur l'API"""
    return {
        "message": "Bienvenue sur l'API Mothra",
        "version": "1.0.0",
        "documentation": "/docs",
        "status": "✅ Opérationnel"
    }


@app.get("/health")
async def health_check():
    """Health check pour monitoring"""
    db_status = "✅ Connecté" if db and db.conn else "❌ Déconnecté"
    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    }


@app.get("/api/v1/model")
async def get_model_info():
    """Informations sur le modèle Mothra"""
    return {
        "name": "Mothra",
        "version": "1.0",
        "description": "Modèle de détection des maladies de la peau par IA",
        "accuracy": 0.95,
        "classes": [
            "Mélanome",
            "Carcinome basocellulaire",
            "Carcinome épidermoïde",
            "Kératose actinique",
            "Naevus",
            "Normal"
        ],
        "input_format": ["jpg", "jpeg", "png", "webp"],
        "max_file_size": "10MB"
    }


@app.get("/api/v1/projects/mothra-v2")
async def get_mothra_v2_info():
    """Informations sur le futur projet Mothra V2"""
    return {
        "name": "Mothra V2",
        "version": "2.0",
        "status": "En développement",
        "description": "Prochaine génération du système de détection avec plus de classes et meilleure précision",
        "planned_features": [
            "Support de 20+ classes de maladies",
            "Précision améliorée (>97%)",
            "Détection multi-zones",
            "Recommandations personnalisées",
            "Intégration telemédecine"
        ],
        "release_date": "2026-Q2"
    }


@app.get("/api/v1/legal/rgpd")
async def get_rgpd_info():
    """Informations RGPD et mentions légales"""
    return {
        "title": "Politique de confidentialité RGPD",
        "last_updated": "2025-11-04",
        "sections": [
            {
                "title": "Collecte des données",
                "content": "Nous collectons uniquement les données nécessaires au fonctionnement du service: nom, email, âge, sexe, et images médicales."
            },
            {
                "title": "Utilisation des données",
                "content": "Vos données sont utilisées exclusivement pour fournir des diagnostics et améliorer notre modèle (avec votre consentement)."
            },
            {
                "title": "Vos droits",
                "content": "Vous avez le droit d'accéder, modifier, exporter et supprimer vos données à tout moment via l'API."
            },
            {
                "title": "Sécurité",
                "content": "Toutes les données sont chiffrées et stockées de manière sécurisée. Les mots de passe sont hashés avec bcrypt."
            },
            {
                "title": "Conservation",
                "content": "Vos données sont conservées tant que votre compte est actif. Suppression définitive possible à tout moment."
            }
        ],
        "contact": "rgpd@mothra-health.com"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


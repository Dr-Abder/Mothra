#!/bin/bash

# Script de lancement de l'API Mothra

echo "🦋 Démarrage de l'API Mothra..."

# Vérifier que PostgreSQL est démarré
echo "📦 Vérification de PostgreSQL..."
sudo service postgresql start

# Attendre que PostgreSQL soit prêt
sleep 2

# Lancer l'API
echo "🚀 Lancement de FastAPI..."
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

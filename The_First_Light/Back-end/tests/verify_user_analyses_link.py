"""
Vérification du lien User <-> Analyses dans la base de données
"""

import sys
import os

# Ajouter le chemin de app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from db.DBHandler import DBHandler
from models.User import User
from models.Analyse import Analyse
import requests
import io
from PIL import Image
import numpy as np
import time


def create_test_image():
    """Crée une image de test"""
    img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.read()


def verify_database_link():
    """Vérifie le lien dans la base de données directement"""
    print("\n" + "="*70)
    print("🔍 VÉRIFICATION DU LIEN USER <-> ANALYSES")
    print("="*70)

    # Connexion à la base de données
    print("\n[1] Connexion à la base de données...")
    db = DBHandler(
        dbname="mothra_db",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )
    db.connect()
    User.db = db
    Analyse.db = db
    print("✅ Connexion réussie")

    # Créer un utilisateur de test via l'API
    print("\n[2] Création d'un utilisateur via l'API...")
    BASE_URL = "http://localhost:8000"
    signup_data = {
        "first_name": "LinkTest",
        "last_name": "User",
        "email": f"linktest.{int(time.time())}@example.com",
        "password": "LinkTest@123",
        "age": 30,
        "sex": "homme",
        "consent_rgpd": True
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        if response.status_code == 201:
            result = response.json()
            token = result["access_token"]
            user_id = result["user_id"]
            print(f"✅ Utilisateur créé (ID: {user_id})")
        else:
            print(f"❌ Échec: {response.status_code}")
            db.disconnect()
            return
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        db.disconnect()
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Faire 3 prédictions via l'API
    print("\n[3] Création de 3 prédictions via l'API...")
    for i in range(3):
        test_image = create_test_image()
        files = {"file": (f"test_link_{i}.jpg", test_image, "image/jpeg")}

        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                files=files,
                headers=headers
            )

            if response.status_code == 200:
                print(f"   ✅ Prédiction {i+1}/3 créée")
            else:
                print(f"   ❌ Prédiction {i+1}/3 échouée")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

    # Vérifier via les modèles directement
    print("\n[4] Vérification via les modèles...")

    # Récupérer l'utilisateur
    user = User.get_by_id(user_id)
    if user:
        print(f"✅ Utilisateur trouvé: {user.first_name} {user.last_name}")
        print(f"   Email: {user.email}")
    else:
        print("❌ Utilisateur non trouvé")
        db.disconnect()
        return

    # Récupérer ses analyses
    analyses = Analyse.get_by_user(user_id)
    print(f"\n✅ Analyses de l'utilisateur: {len(analyses)}")

    if len(analyses) == 3:
        print("✅✅ SUCCÈS: 3 analyses trouvées (comme attendu)")

        for idx, analyse in enumerate(analyses, 1):
            print(f"\n   Analyse {idx}:")
            print(f"      ID: {analyse.id}")
            print(f"      User ID: {analyse.user_id}")
            print(f"      Photo: {analyse.photo}")
            print(f"      Diagnostic: {analyse.diagnostic}")
            print(f"      Confiance: {analyse.confidence:.1%}")
            print(f"      Date: {analyse.created_at}")

            # Vérifier que le user_id correspond
            if analyse.user_id == user_id:
                print(f"      ✅ user_id correspond")
            else:
                print(f"      ❌ user_id ne correspond pas!")
    else:
        print(f"❌ Nombre d'analyses incorrect: attendu 3, trouvé {len(analyses)}")

    # Vérifier la contrainte de clé étrangère
    print("\n[5] Vérification de la contrainte de clé étrangère...")
    query = """
        SELECT
            conname AS constraint_name,
            pg_get_constraintdef(c.oid) AS constraint_definition
        FROM pg_constraint c
        JOIN pg_namespace n ON n.oid = c.connamespace
        WHERE conrelid = 'analyses'::regclass
        AND contype = 'f'
    """

    try:
        constraints = db.fetch_all(query)
        if constraints:
            print("✅ Contraintes de clé étrangère trouvées:")
            for constraint in constraints:
                print(f"   {constraint['constraint_name']}")
                print(f"   {constraint['constraint_definition']}")

                # Vérifier CASCADE DELETE
                if "ON DELETE CASCADE" in constraint['constraint_definition']:
                    print("   ✅ ON DELETE CASCADE configuré")
                else:
                    print("   ⚠️  ON DELETE CASCADE non configuré")
        else:
            print("⚠️  Aucune contrainte de clé étrangère trouvée")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Vérifier via requête SQL directe
    print("\n[6] Vérification via requête SQL directe...")
    query = """
        SELECT
            u.id AS user_id,
            u.first_name,
            u.last_name,
            u.email,
            COUNT(a.id) AS nb_analyses
        FROM users u
        LEFT JOIN analyses a ON u.id = a.user_id
        WHERE u.id = %s
        GROUP BY u.id, u.first_name, u.last_name, u.email
    """

    try:
        result = db.fetch_one(query, (user_id,))
        if result:
            print("✅ Requête JOIN réussie:")
            print(f"   User: {result['first_name']} {result['last_name']}")
            print(f"   Email: {result['email']}")
            print(f"   Analyses: {result['nb_analyses']}")

            if result['nb_analyses'] == 3:
                print("   ✅✅ Le JOIN fonctionne correctement!")
        else:
            print("❌ Aucun résultat trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test CASCADE DELETE
    print("\n[7] Test CASCADE DELETE...")
    print("   Suppression de l'utilisateur (devrait supprimer les analyses)...")

    try:
        # Compter les analyses avant suppression
        query = "SELECT COUNT(*) as count FROM analyses WHERE user_id = %s"
        before = db.fetch_one(query, (user_id,))
        print(f"   Analyses avant suppression: {before['count']}")

        # Supprimer l'utilisateur
        user.delete()
        print("   ✅ Utilisateur supprimé")

        # Compter les analyses après suppression
        after = db.fetch_one(query, (user_id,))
        print(f"   Analyses après suppression: {after['count']}")

        if after['count'] == 0:
            print("   ✅✅ CASCADE DELETE fonctionne correctement!")
        else:
            print(f"   ❌ CASCADE DELETE ne fonctionne pas: {after['count']} analyses restantes")

    except Exception as e:
        print(f"   ❌ Erreur: {e}")

    # Déconnexion
    db.disconnect()
    print("\n" + "="*70)
    print("✅ VÉRIFICATION TERMINÉE")
    print("="*70 + "\n")


if __name__ == "__main__":
    verify_database_link()

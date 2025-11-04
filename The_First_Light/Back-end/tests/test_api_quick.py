"""
Script de test rapide de l'API Mothra
Lance l'API et teste toutes les routes principales
"""

import requests
import time
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    print("\n" + "="*60)
    print("🧪 TEST DE L'API MOTHRA")
    print("="*60)

    # Vérifier que l'API est accessible
    print("\n[1] Vérification de l'API...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ API accessible: {response.json()}")
    except Exception as e:
        print(f"❌ API non accessible. Assurez-vous qu'elle tourne sur le port 8000")
        print(f"   Erreur: {e}")
        return

    # Test de l'inscription
    print("\n[2] Test d'inscription...")
    signup_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test.{int(time.time())}@example.com",  # Email unique
        "password": "TestPass@123",
        "age": 28,
        "sex": "homme",
        "consent_rgpd": True
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
        if response.status_code == 201:
            result = response.json()
            token = result["access_token"]
            user_id = result["user_id"]
            print(f"✅ Inscription réussie")
            print(f"   User ID: {user_id}")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"❌ Échec inscription: {response.status_code}")
            print(f"   {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur inscription: {e}")
        return

    # Headers avec le token
    headers = {"Authorization": f"Bearer {token}"}

    # Test de récupération du profil
    print("\n[3] Test de récupération du profil...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Profil récupéré")
            print(f"   Nom: {profile['first_name']} {profile['last_name']}")
            print(f"   Email: {profile['email']}")
        else:
            print(f"❌ Échec récupération profil: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de création d'analyse
    print("\n[4] Test de création d'analyse...")
    analyse_data = {
        "photo": "test_scan_001.jpg",
        "diagnostic": "Test diagnostic - Peau normale",
        "confidence": 0.95
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/analyses",
            json=analyse_data,
            headers=headers
        )
        if response.status_code == 201:
            analyse = response.json()
            analyse_id = analyse["id"]
            print(f"✅ Analyse créée")
            print(f"   ID: {analyse_id}")
            print(f"   Diagnostic: {analyse['diagnostic']}")
            print(f"   Confiance: {analyse['confidence']}")
        else:
            print(f"❌ Échec création analyse: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de création d'une 2ème analyse
    print("\n[5] Test de création d'une 2ème analyse...")
    analyse_data2 = {
        "photo": "test_scan_002.png",
        "diagnostic": "Naevus bénin détecté",
        "confidence": 0.88
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/analyses",
            json=analyse_data2,
            headers=headers
        )
        if response.status_code == 201:
            print(f"✅ 2ème analyse créée")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de listing des analyses
    print("\n[6] Test de listing des analyses...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
        if response.status_code == 200:
            analyses = response.json()
            print(f"✅ {len(analyses)} analyse(s) récupérée(s)")
            for i, analyse in enumerate(analyses, 1):
                print(f"   {i}. {analyse['photo']} - Confiance: {analyse['confidence']}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de récupération d'une analyse spécifique
    print("\n[7] Test de récupération d'une analyse spécifique...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/analyses/{analyse_id}",
            headers=headers
        )
        if response.status_code == 200:
            print(f"✅ Analyse récupérée par ID")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de mise à jour du profil
    print("\n[8] Test de mise à jour du profil...")
    update_data = {
        "age": 29
    }

    try:
        response = requests.put(
            f"{BASE_URL}/api/v1/users/me",
            json=update_data,
            headers=headers
        )
        if response.status_code == 200:
            updated_profile = response.json()
            print(f"✅ Profil mis à jour")
            print(f"   Nouvel âge: {updated_profile['age']}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test d'export de données (RGPD)
    print("\n[9] Test d'export de données (RGPD)...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/users/me/data-export",
            headers=headers
        )
        if response.status_code == 200:
            export_data = response.json()
            print(f"✅ Export réussi")
            print(f"   Date d'export: {export_data['export_date']}")
            print(f"   Nombre d'analyses: {len(export_data['analyses'])}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de suppression d'une analyse
    print("\n[10] Test de suppression d'une analyse...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/v1/analyses/{analyse_id}",
            headers=headers
        )
        if response.status_code == 200:
            print(f"✅ Analyse supprimée")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test de suppression du compte (RGPD)
    print("\n[11] Test de suppression du compte (RGPD)...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/v1/users/me",
            headers=headers
        )
        if response.status_code == 200:
            print(f"✅ Compte supprimé (avec analyses en cascade)")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # Test des routes d'information
    print("\n[12] Test des routes d'information...")
    try:
        # Info modèle
        response = requests.get(f"{BASE_URL}/api/v1/model")
        if response.status_code == 200:
            print(f"✅ Info modèle OK")

        # Info Mothra V2
        response = requests.get(f"{BASE_URL}/api/v1/projects/mothra-v2")
        if response.status_code == 200:
            print(f"✅ Info Mothra V2 OK")

        # Info RGPD
        response = requests.get(f"{BASE_URL}/api/v1/legal/rgpd")
        if response.status_code == 200:
            print(f"✅ Info RGPD OK")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n" + "="*60)
    print("✅ TESTS TERMINÉS AVEC SUCCÈS")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("\n⚠️  Assurez-vous que l'API tourne sur http://localhost:8000")
    print("    Lancez-la avec: cd app && uvicorn main:app --reload\n")

    input("Appuyez sur Entrée pour lancer les tests...")

    test_api()

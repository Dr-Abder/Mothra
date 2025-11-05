"""
Test de la sauvegarde automatique des prédictions
"""

import requests
import io
from PIL import Image
import numpy as np
import time

BASE_URL = "http://localhost:8000"


def create_test_image():
    """Crée une image de test"""
    img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.read()


def test_auto_save():
    """Test de la sauvegarde automatique des analyses"""
    print("\n" + "="*70)
    print("🧪 TEST DE SAUVEGARDE AUTOMATIQUE DES PRÉDICTIONS")
    print("="*70)

    # 1. Créer un compte utilisateur
    print("\n[1] Inscription utilisateur...")
    signup_data = {
        "first_name": "AutoSave",
        "last_name": "Test",
        "email": f"autosave.{int(time.time())}@example.com",
        "password": "TestAutoSave@123",
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
            print(f"✅ Utilisateur créé (ID: {user_id[:8]}...)")
        else:
            print(f"❌ Échec inscription: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("⚠️  Assurez-vous que l'API tourne sur http://localhost:8000")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Vérifier qu'il n'y a pas d'analyses au début
    print("\n[2] Vérification - Analyses initiales...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
        if response.status_code == 200:
            analyses = response.json()
            print(f"✅ Nombre d'analyses initiales: {len(analyses)}")
            initial_count = len(analyses)
        else:
            print(f"❌ Échec: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # 3. Faire une prédiction
    print("\n[3] Prédiction avec image...")
    test_image = create_test_image()
    files = {"file": ("test_auto_save.jpg", test_image, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Prédiction réussie")
            print(f"   Diagnostic: {result['prediction']['diagnostic']}")
            print(f"   Confiance: {result['prediction']['confidence']:.1%}")
        else:
            print(f"❌ Échec prédiction: {response.status_code}")
            print(f"   Détail: {response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # 4. Vérifier que l'analyse a été sauvegardée
    print("\n[4] Vérification - Analyse sauvegardée...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
        if response.status_code == 200:
            analyses = response.json()
            new_count = len(analyses)
            print(f"✅ Nombre d'analyses après prédiction: {new_count}")

            if new_count == initial_count + 1:
                print("✅✅ SUCCÈS: L'analyse a été automatiquement sauvegardée!")

                # Afficher les détails de la dernière analyse
                last_analyse = analyses[0]  # Tri DESC par created_at
                print(f"\n📊 Détails de l'analyse sauvegardée:")
                print(f"   ID: {last_analyse['id']}")
                print(f"   Photo: {last_analyse['photo']}")
                print(f"   Diagnostic: {last_analyse['diagnostic']}")
                print(f"   Confiance: {last_analyse['confidence']:.1%}")
                print(f"   Date: {last_analyse['created_at']}")
            else:
                print(f"❌ ÉCHEC: Nombre d'analyses attendu {initial_count + 1}, trouvé {new_count}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 5. Faire plusieurs prédictions pour tester
    print("\n[5] Test avec 3 prédictions supplémentaires...")
    for i in range(3):
        test_image = create_test_image()
        files = {"file": (f"test_{i}.jpg", test_image, "image/jpeg")}

        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                files=files,
                headers=headers
            )

            if response.status_code == 200:
                print(f"   ✅ Prédiction {i+1}/3 réussie")
            else:
                print(f"   ❌ Prédiction {i+1}/3 échouée")
        except Exception as e:
            print(f"   ❌ Erreur prédiction {i+1}: {e}")

    # 6. Vérifier le total d'analyses
    print("\n[6] Vérification finale...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
        if response.status_code == 200:
            analyses = response.json()
            final_count = len(analyses)
            expected_count = initial_count + 4  # 1 + 3 prédictions

            print(f"✅ Nombre final d'analyses: {final_count}")

            if final_count == expected_count:
                print(f"✅✅ PARFAIT: Toutes les prédictions ont été sauvegardées!")
            else:
                print(f"⚠️  Attendu {expected_count}, trouvé {final_count}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 7. Test de récupération par ID
    print("\n[7] Test de récupération d'une analyse par ID...")
    try:
        if analyses:
            analyse_id = analyses[0]['id']
            response = requests.get(
                f"{BASE_URL}/api/v1/analyses/{analyse_id}",
                headers=headers
            )

            if response.status_code == 200:
                analyse = response.json()
                print("✅ Récupération par ID réussie")
                print(f"   Diagnostic: {analyse['diagnostic']}")
            else:
                print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 8. Test RGPD - Export des données
    print("\n[8] Test RGPD - Export des données avec analyses...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/users/me/data-export",
            headers=headers
        )

        if response.status_code == 200:
            export = response.json()
            print("✅ Export RGPD réussi")
            print(f"   Analyses exportées: {len(export['analyses'])}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 9. Nettoyage - Supprimer le compte (CASCADE DELETE)
    print("\n[9] Nettoyage - Suppression du compte et analyses...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/v1/users/me",
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Compte supprimé (analyses supprimées automatiquement)")
        else:
            print(f"⚠️  Échec suppression: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n" + "="*70)
    print("✅ TESTS DE SAUVEGARDE AUTOMATIQUE TERMINÉS")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_auto_save()

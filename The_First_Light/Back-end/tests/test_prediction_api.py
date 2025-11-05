"""
Test complet de l'API de prédiction avec upload d'image
"""

import requests
import io
from PIL import Image
import numpy as np
import time

BASE_URL = "http://localhost:8000"


def create_test_image(size=(128, 128), image_type="random"):
    """
    Crée une image de test

    Args:
        size: Taille de l'image (width, height)
        image_type: Type d'image ('random', 'skin_normal', 'skin_anomaly')

    Returns:
        bytes: Image en bytes JPEG
    """
    if image_type == "random":
        # Image aléatoire
        img_array = np.random.randint(0, 255, (size[1], size[0], 3), dtype=np.uint8)

    elif image_type == "skin_normal":
        # Simule une peau normale (tons chair)
        img_array = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        img_array[:, :, 0] = np.random.randint(200, 230, (size[1], size[0]))  # R
        img_array[:, :, 1] = np.random.randint(160, 190, (size[1], size[0]))  # G
        img_array[:, :, 2] = np.random.randint(150, 180, (size[1], size[0]))  # B

    elif image_type == "skin_anomaly":
        # Simule une anomalie (zone plus sombre)
        img_array = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        img_array[:, :, 0] = np.random.randint(100, 150, (size[1], size[0]))  # R
        img_array[:, :, 1] = np.random.randint(50, 100, (size[1], size[0]))   # G
        img_array[:, :, 2] = np.random.randint(40, 90, (size[1], size[0]))    # B

    # Créer l'image PIL
    img = Image.fromarray(img_array)

    # Convertir en bytes JPEG
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    return img_bytes.read()


def test_prediction_with_upload():
    """Test complet : signup -> login -> upload image -> prédiction"""

    print("\n" + "="*70)
    print("🧪 TEST COMPLET DE L'API DE PRÉDICTION ML")
    print("="*70)

    # 1. Créer un compte utilisateur
    print("\n[1] Inscription utilisateur...")
    signup_data = {
        "first_name": "TestML",
        "last_name": "User",
        "email": f"testml.{int(time.time())}@example.com",
        "password": "TestML@123",
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

    # 2. Test avec image aléatoire
    print("\n[2] Test prédiction - Image aléatoire...")
    test_image_1 = create_test_image(image_type="random")

    files = {"file": ("test_random.jpg", test_image_1, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Prédiction réussie (Image aléatoire)")
            print(f"   Diagnostic: {result['prediction']['diagnostic']}")
            print(f"   Confiance: {result['prediction']['confidence']:.1%}")
            print(f"   Modèle: {result['prediction']['model_version']}")
            print(f"   Message: {result['message'][:80]}...")
        else:
            print(f"❌ Échec: {response.status_code}")
            print(f"   Détail: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 3. Test avec simulation peau normale
    print("\n[3] Test prédiction - Simulation peau normale...")
    test_image_2 = create_test_image(image_type="skin_normal")

    files = {"file": ("test_normal.jpg", test_image_2, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Prédiction réussie (Peau normale simulée)")
            print(f"   Diagnostic: {result['prediction']['diagnostic']}")
            print(f"   Confiance: {result['prediction']['confidence']:.1%}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 4. Test avec simulation anomalie
    print("\n[4] Test prédiction - Simulation anomalie cutanée...")
    test_image_3 = create_test_image(image_type="skin_anomaly")

    files = {"file": ("test_anomaly.jpg", test_image_3, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Prédiction réussie (Anomalie simulée)")
            print(f"   Diagnostic: {result['prediction']['diagnostic']}")
            print(f"   Confiance: {result['prediction']['confidence']:.1%}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 5. Test avec différentes tailles d'images
    print("\n[5] Test avec image plus grande (512x512)...")
    test_image_large = create_test_image(size=(512, 512))

    files = {"file": ("test_large.jpg", test_image_large, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Prédiction réussie (Image 512x512)")
            print(f"   Le modèle a automatiquement redimensionné à 128x128")
            print(f"   Confiance: {result['prediction']['confidence']:.1%}")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 6. Test format PNG
    print("\n[6] Test format PNG...")
    img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    test_image_png = img_bytes.read()

    files = {"file": ("test_image.png", test_image_png, "image/png")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Format PNG supporté")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 7. Test format non supporté
    print("\n[7] Test format non supporté (devrait échouer)...")
    files = {"file": ("test.txt", b"not an image", "text/plain")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 400:
            print("✅ Format invalide correctement rejeté")
            print(f"   Message: {response.json()['detail']}")
        else:
            print(f"⚠️  Code inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 8. Test sans authentification (devrait échouer)
    print("\n[8] Test sans authentification (devrait échouer)...")
    files = {"file": ("test.jpg", test_image_1, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files
        )

        if response.status_code == 401 or response.status_code == 403:
            print("✅ Requête non authentifiée correctement rejetée")
        else:
            print(f"⚠️  Code inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 9. Nettoyer - Supprimer le compte de test
    print("\n[9] Nettoyage - Suppression du compte de test...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/v1/users/me",
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Compte de test supprimé")
        else:
            print(f"⚠️  Échec suppression: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n" + "="*70)
    print("✅ TESTS DE PRÉDICTION TERMINÉS")
    print("="*70 + "\n")


def quick_test():
    """Test rapide avec image existante si disponible"""
    print("\n🚀 Test rapide de prédiction...")
    print("⚠️  Ce test nécessite que vous soyez déjà connecté\n")

    # Demander le token
    token = input("Entrez votre token JWT (ou appuyez sur Entrée pour test complet): ").strip()

    if not token:
        print("\n📋 Lancement du test complet...\n")
        test_prediction_with_upload()
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Créer une image de test
    test_image = create_test_image()
    files = {"file": ("quick_test.jpg", test_image, "image/jpeg")}

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print("\n✅ Prédiction réussie!")
            print(f"Diagnostic: {result['prediction']['diagnostic']}")
            print(f"Confiance: {result['prediction']['confidence']:.1%}")
            print(f"Message: {result['message']}\n")
        else:
            print(f"\n❌ Échec: {response.status_code}")
            print(f"Détail: {response.text}\n")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("⚠️  Assurez-vous que l'API tourne sur http://localhost:8000\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        print("\n⚠️  Assurez-vous que l'API Mothra tourne sur http://localhost:8000")
        input("Appuyez sur Entrée pour lancer les tests...\n")
        test_prediction_with_upload()

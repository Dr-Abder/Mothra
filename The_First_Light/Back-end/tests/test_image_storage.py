"""
Test complet du système de stockage des images
"""

import requests
import io
from PIL import Image
import numpy as np
import time

BASE_URL = "http://localhost:8000"


def create_test_image(color="random"):
    """Crée une image de test avec une couleur spécifique"""
    if color == "random":
        img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    elif color == "red":
        img_array = np.zeros((128, 128, 3), dtype=np.uint8)
        img_array[:, :, 0] = 255  # Rouge
    elif color == "blue":
        img_array = np.zeros((128, 128, 3), dtype=np.uint8)
        img_array[:, :, 2] = 255  # Bleu

    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.read()


def test_image_storage():
    """Test complet du stockage des images"""
    print("\n" + "="*70)
    print("🧪 TEST COMPLET DU STOCKAGE DES IMAGES")
    print("="*70)

    # 1. Créer un compte utilisateur
    print("\n[1] Inscription utilisateur...")
    signup_data = {
        "first_name": "ImageTest",
        "last_name": "User",
        "email": f"imagetest.{int(time.time())}@example.com",
        "password": "ImageTest@123",
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

    # 2. Faire une prédiction avec image
    print("\n[2] Upload d'image + prédiction...")
    test_image = create_test_image("red")
    files = {"file": ("test_red.jpg", test_image, "image/jpeg")}

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
        else:
            print(f"❌ Échec: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # 3. Récupérer les analyses pour obtenir l'ID
    print("\n[3] Récupération des analyses...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
        if response.status_code == 200:
            analyses = response.json()
            if analyses:
                analyse_id = analyses[0]['id']
                image_path = analyses[0]['photo']
                print(f"✅ Analyse récupérée (ID: {analyse_id[:8]}...)")
                print(f"   Chemin image: {image_path}")
            else:
                print("❌ Aucune analyse trouvée")
                return
        else:
            print(f"❌ Échec: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return

    # 4. Récupérer l'image via l'API
    print("\n[4] Récupération de l'image via API...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/images/analyses/{analyse_id}/image",
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Image récupérée avec succès")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Taille: {len(response.content)} bytes")

            # Vérifier que c'est bien une image valide
            try:
                img = Image.open(io.BytesIO(response.content))
                print(f"   Dimensions: {img.size}")
                print(f"   Format: {img.format}")
                print("   ✅✅ Image valide!")
            except Exception as e:
                print(f"   ❌ Image invalide: {e}")
        else:
            print(f"❌ Échec: {response.status_code}")
            print(f"   Détail: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 5. Faire plusieurs prédictions
    print("\n[5] Test avec 3 images supplémentaires...")
    for i, color in enumerate(["blue", "random", "red"]):
        test_image = create_test_image(color)
        files = {"file": (f"test_{color}_{i}.jpg", test_image, "image/jpeg")}

        try:
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                files=files,
                headers=headers
            )

            if response.status_code == 200:
                print(f"   ✅ Image {i+1}/3 uploadée ({color})")
            else:
                print(f"   ❌ Échec image {i+1}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

    # 6. Vérifier les statistiques de stockage
    print("\n[6] Statistiques de stockage...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/images/storage/stats",
            headers=headers
        )

        if response.status_code == 200:
            stats = response.json()
            print("✅ Statistiques récupérées:")
            print(f"   Images utilisateur: {stats['user']['images_count']}")
            print(f"   Total utilisateurs: {stats['global']['users_count']}")
            print(f"   Total images: {stats['global']['total_images']}")
            print(f"   Taille totale: {stats['global']['total_size_mb']} MB")

            if stats['user']['images_count'] == 4:
                print("   ✅✅ 4 images stockées comme attendu!")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 7. Test de sécurité - Essayer d'accéder à l'image d'un autre user
    print("\n[7] Test de sécurité - Accès image autre utilisateur...")
    # Créer un second utilisateur
    signup_data2 = {
        "first_name": "SecondUser",
        "last_name": "Test",
        "email": f"second.{int(time.time())}@example.com",
        "password": "Second@123",
        "age": 25,
        "sex": "femme",
        "consent_rgpd": True
    }

    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data2)
        if response.status_code == 201:
            token2 = response.json()["access_token"]
            headers2 = {"Authorization": f"Bearer {token2}"}

            # Essayer d'accéder à l'image du premier utilisateur
            response = requests.get(
                f"{BASE_URL}/api/v1/images/analyses/{analyse_id}/image",
                headers=headers2
            )

            if response.status_code == 403:
                print("✅ Accès refusé - Sécurité OK!")
            else:
                print(f"⚠️  Code inattendu: {response.status_code}")

            # Supprimer le second utilisateur
            requests.delete(f"{BASE_URL}/api/v1/users/me", headers=headers2)
        else:
            print(f"⚠️  Échec création second user")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 8. Test de suppression d'une image spécifique
    print("\n[8] Test de suppression d'une image...")
    try:
        # Récupérer les analyses
        response = requests.get(f"{BASE_URL}/api/v1/analyses", headers=headers)
        analyses = response.json()

        if len(analyses) > 0:
            first_analyse_id = analyses[-1]['id']  # Prendre la plus ancienne

            # Supprimer l'image
            response = requests.delete(
                f"{BASE_URL}/api/v1/images/analyses/{first_analyse_id}/image",
                headers=headers
            )

            if response.status_code == 200:
                print("✅ Image supprimée")

                # Vérifier qu'on ne peut plus la récupérer
                response = requests.get(
                    f"{BASE_URL}/api/v1/images/analyses/{first_analyse_id}/image",
                    headers=headers
                )

                if response.status_code == 404:
                    print("✅ Image bien supprimée - 404 attendu")
                else:
                    print(f"⚠️  Code inattendu: {response.status_code}")
            else:
                print(f"❌ Échec suppression: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 9. Test de suppression de toutes les analyses
    print("\n[9] Test de suppression de toutes les analyses...")
    try:
        response = requests.delete(
            f"{BASE_URL}/api/v1/users/me/analyses",
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result['message']}")

            # Vérifier les stats
            response = requests.get(
                f"{BASE_URL}/api/v1/images/storage/stats",
                headers=headers
            )

            if response.status_code == 200:
                stats = response.json()
                if stats['user']['images_count'] == 0:
                    print("✅ Toutes les images supprimées")
        else:
            print(f"❌ Échec: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    # 10. Test final - Upload et suppression du compte
    print("\n[10] Test final - Upload + suppression compte...")
    try:
        # Upload une dernière image
        test_image = create_test_image("blue")
        files = {"file": ("final_test.jpg", test_image, "image/jpeg")}

        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Image finale uploadée")

        # Supprimer le compte
        response = requests.delete(
            f"{BASE_URL}/api/v1/users/me",
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Compte supprimé (images supprimées automatiquement)")
        else:
            print(f"⚠️  Échec suppression compte: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

    print("\n" + "="*70)
    print("✅ TESTS DE STOCKAGE DES IMAGES TERMINÉS")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_image_storage()

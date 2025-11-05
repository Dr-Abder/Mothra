"""
Test de prédiction avec une vraie image
Usage: python test_with_real_image.py <chemin_image> <token_jwt>
"""

import requests
import sys
import os

BASE_URL = "http://localhost:8000"


def test_real_image(image_path: str, token: str):
    """
    Teste une prédiction avec une vraie image

    Args:
        image_path: Chemin vers l'image
        token: Token JWT
    """
    print("\n" + "="*70)
    print("🧪 TEST DE PRÉDICTION AVEC IMAGE RÉELLE")
    print("="*70)

    # Vérifier que l'image existe
    if not os.path.exists(image_path):
        print(f"\n❌ Erreur: Fichier introuvable: {image_path}")
        return

    # Vérifier la taille du fichier
    file_size = os.path.getsize(image_path)
    print(f"\n📁 Fichier: {os.path.basename(image_path)}")
    print(f"   Taille: {file_size / 1024:.1f} KB")

    if file_size > 10 * 1024 * 1024:  # 10 MB
        print(f"⚠️  Attention: Fichier > 10MB (limite de l'API)")

    # Lire l'image
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Préparer la requête
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (os.path.basename(image_path), image_data)}

    # Envoyer la requête
    print(f"\n🚀 Envoi de l'image à l'API...")

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/predict",
            files=files,
            headers=headers
        )

        if response.status_code == 200:
            result = response.json()

            print("\n✅ PRÉDICTION RÉUSSIE!\n")
            print("="*70)
            print(f"📊 RÉSULTATS:")
            print("="*70)
            print(f"Diagnostic:    {result['prediction']['diagnostic']}")
            print(f"Confiance:     {result['prediction']['confidence']:.1%}")
            print(f"Modèle:        {result['prediction']['model_version']}")
            print(f"Timestamp:     {result['prediction']['timestamp']}")
            print(f"\n💬 Message:")
            print(f"   {result['message']}")
            print("="*70 + "\n")

        elif response.status_code == 401:
            print("\n❌ Erreur d'authentification")
            print("   Token JWT invalide ou expiré")
            print("   Connectez-vous d'abord pour obtenir un nouveau token\n")

        elif response.status_code == 400:
            print(f"\n❌ Requête invalide")
            print(f"   {response.json().get('detail', 'Erreur inconnue')}\n")

        elif response.status_code == 413:
            print(f"\n❌ Fichier trop volumineux")
            print(f"   Taille max: 10MB\n")

        else:
            print(f"\n❌ Erreur: Code {response.status_code}")
            print(f"   Détail: {response.text}\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ Impossible de se connecter à l'API")
        print("   Assurez-vous que l'API tourne sur http://localhost:8000\n")

    except Exception as e:
        print(f"\n❌ Erreur: {e}\n")


def print_usage():
    """Affiche l'aide"""
    print("\n" + "="*70)
    print("📖 USAGE")
    print("="*70)
    print("\nOption 1: Avec token JWT")
    print("  python test_with_real_image.py <chemin_image> <token_jwt>")
    print("\nOption 2: Mode interactif")
    print("  python test_with_real_image.py")
    print("\nExemple:")
    print("  python test_with_real_image.py /path/to/skin_image.jpg eyJhbGc...")
    print("\n" + "="*70 + "\n")


def interactive_mode():
    """Mode interactif"""
    print("\n🤖 MODE INTERACTIF - Test de prédiction ML")
    print("="*70)

    # Demander le chemin de l'image
    image_path = input("\n📁 Chemin vers l'image: ").strip()

    if not image_path:
        print("❌ Chemin d'image requis")
        return

    # Demander le token
    print("\n🔑 Token JWT:")
    print("   (Obtenez-le en vous connectant: POST /api/v1/auth/login)")
    token = input("   Token: ").strip()

    if not token:
        print("❌ Token JWT requis")
        return

    # Lancer le test
    test_real_image(image_path, token)


def quick_login_and_test():
    """Login rapide + test"""
    print("\n🚀 LOGIN + TEST RAPIDE")
    print("="*70)

    email = input("\n📧 Email: ").strip()
    password = input("🔒 Mot de passe: ").strip()
    image_path = input("📁 Chemin image: ").strip()

    if not all([email, password, image_path]):
        print("❌ Tous les champs sont requis")
        return

    # Login
    print("\n🔐 Connexion...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Connecté!")

            # Test
            test_real_image(image_path, token)
        else:
            print(f"❌ Échec connexion: {response.status_code}")
            print(f"   {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Mode avec arguments
        image_path = sys.argv[1]
        token = sys.argv[2]
        test_real_image(image_path, token)

    elif len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help", "help"]:
        # Aide
        print_usage()

    else:
        # Mode interactif
        print("\n" + "="*70)
        print("🎯 MODE DE TEST")
        print("="*70)
        print("\n1. Mode interactif (avec token)")
        print("2. Login + Test rapide")
        print("3. Aide")

        choice = input("\nChoix (1-3): ").strip()

        if choice == "1":
            interactive_mode()
        elif choice == "2":
            quick_login_and_test()
        elif choice == "3":
            print_usage()
        else:
            print("\n❌ Choix invalide")
            print_usage()

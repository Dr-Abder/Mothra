"""
Test rapide du modèle ML avec une image test
"""

import sys
import os

# Ajouter le chemin de app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from services.ml_service import get_ml_service
from PIL import Image
import numpy as np
import io

def create_test_image():
    """Crée une image de test 128x128"""
    # Créer une image RGB aléatoire
    img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)

    # Convertir en bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    return img_bytes.read()

def test_prediction():
    """Test une prédiction"""
    print("\n" + "="*60)
    print("🧪 TEST DE PRÉDICTION ML")
    print("="*60)

    # Charger le service
    print("\n[1] Chargement du modèle...")
    ml_service = get_ml_service()
    print("✅ Modèle chargé")

    # Créer une image de test
    print("\n[2] Création d'une image de test 128x128...")
    test_image = create_test_image()
    print(f"✅ Image créée ({len(test_image)} bytes)")

    # Faire une prédiction
    print("\n[3] Prédiction en cours...")
    result = ml_service.get_detailed_prediction(test_image)

    print("✅ Prédiction terminée!\n")
    print(f"   Diagnostic: {result['diagnostic']}")
    print(f"   Confiance: {result['confidence']:.1%}")
    print(f"   Classe: {result['class_name']}")
    print(f"   Recommandation: {result['recommendation']}")
    print(f"   Modèle: {result['model_version']}")

    print("\n" + "="*60)
    print("✅ TEST RÉUSSI")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_prediction()

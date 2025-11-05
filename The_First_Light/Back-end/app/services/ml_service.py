"""
Service de Machine Learning pour les prédictions avec le modèle Mothra
"""

import numpy as np
from PIL import Image
import io
import tensorflow as tf
from typing import Tuple
import os

class MLService:
    """Service de prédiction ML"""

    def __init__(self, model_path: str):
        """
        Initialise le service ML avec le modèle

        Args:
            model_path: Chemin vers le fichier .h5 du modèle
        """
        self.model_path = model_path
        self.model = None
        self.input_shape = (128, 128)  # Taille attendue par le modèle
        self.classes = {
            0: "Peau normale - Aucune anomalie détectée",
            1: "Anomalie cutanée détectée - Consultation recommandée"
        }

    def load_model(self):
        """Charge le modèle TensorFlow"""
        if self.model is None:
            print(f"🤖 Chargement du modèle depuis {self.model_path}...")
            self.model = tf.keras.models.load_model(self.model_path)
            print("✅ Modèle chargé avec succès")
        return self.model

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Prétraite l'image pour la prédiction

        Args:
            image_bytes: Image en bytes

        Returns:
            np.ndarray: Image prétraitée (1, 128, 128, 3)
        """
        # Ouvrir l'image avec PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Convertir en RGB si nécessaire
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Redimensionner à 128x128
        image = image.resize(self.input_shape)

        # Convertir en array numpy
        image_array = np.array(image)

        # Normaliser les pixels (0-255 → 0-1)
        image_array = image_array.astype('float32') / 255.0

        # Ajouter dimension batch (1, 128, 128, 3)
        image_array = np.expand_dims(image_array, axis=0)

        return image_array

    def predict(self, image_bytes: bytes) -> Tuple[str, float, int]:
        """
        Fait une prédiction sur l'image

        Args:
            image_bytes: Image en bytes

        Returns:
            Tuple[str, float, int]: (diagnostic, confiance, classe)
        """
        # Charger le modèle si nécessaire
        if self.model is None:
            self.load_model()

        # Prétraiter l'image
        processed_image = self.preprocess_image(image_bytes)

        # Faire la prédiction
        prediction = self.model.predict(processed_image, verbose=0)

        # Récupérer le score (probabilité)
        score = float(prediction[0][0])

        # Déterminer la classe (0 ou 1)
        predicted_class = 1 if score > 0.5 else 0

        # Calculer la confiance
        confidence = score if predicted_class == 1 else (1 - score)

        # Obtenir le diagnostic
        diagnostic = self.classes[predicted_class]

        return diagnostic, confidence, predicted_class

    def get_detailed_prediction(self, image_bytes: bytes) -> dict:
        """
        Retourne une prédiction détaillée avec toutes les infos

        Args:
            image_bytes: Image en bytes

        Returns:
            dict: Prédiction complète
        """
        diagnostic, confidence, predicted_class = self.predict(image_bytes)

        return {
            "diagnostic": diagnostic,
            "confidence": round(confidence, 3),
            "predicted_class": predicted_class,
            "class_name": "normal" if predicted_class == 0 else "anomalie",
            "recommendation": self._get_recommendation(predicted_class, confidence),
            "model_version": "mothra_cnn_v1",
            "input_size": f"{self.input_shape[0]}x{self.input_shape[1]}"
        }

    def _get_recommendation(self, predicted_class: int, confidence: float) -> str:
        """
        Génère une recommandation basée sur la prédiction

        Args:
            predicted_class: Classe prédite (0 ou 1)
            confidence: Niveau de confiance

        Returns:
            str: Recommandation
        """
        if predicted_class == 0:
            if confidence > 0.9:
                return "Peau en bon état. Continuez vos soins habituels."
            else:
                return "Résultat normal mais confiance modérée. Surveillez l'évolution."
        else:
            if confidence > 0.8:
                return "Anomalie détectée avec forte confiance. Consultation dermatologique urgente recommandée."
            elif confidence > 0.6:
                return "Anomalie potentielle détectée. Consultez un dermatologue par précaution."
            else:
                return "Résultat incertain. Prenez une photo de meilleure qualité ou consultez un professionnel."


# Instance globale du service (singleton)
ml_service = None

def get_ml_service() -> MLService:
    """
    Retourne l'instance du service ML (singleton)

    Returns:
        MLService: Instance du service
    """
    global ml_service
    if ml_service is None:
        # Chemin vers le modèle
        model_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "..", "V1", "models", "mothra_cnn_v1.h5"
        )
        ml_service = MLService(model_path)
        ml_service.load_model()
    return ml_service

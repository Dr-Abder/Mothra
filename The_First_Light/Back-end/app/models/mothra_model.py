import tensorflow as tf
import numpy as np

class MothraModel:
    def __init__(self, model_path: str = "/workspaces/Mothra/The_First_Light/V1/models/mothra_cnn_v1.h5"):
        # Charger le modèle Keras sauvegardé
        self.model = tf.keras.models.load_model(model_path)
        print("✅ Modèle chargé avec succès.")

    def predict(self, img_array: np.ndarray) -> float:
        """
        Prédit la probabilité d'une lésion maligne.
        
        Args:
            img_array (np.ndarray): image prétraitée, shape (1, 128, 128, 3)
        
        Returns:
            float: score de prédiction (entre 0 et 1)
        """
        # Prédiction du modèle : sortie entre 0 et 1
        preds = self.model.predict(img_array)
        # preds est un tableau 2D shape (1,1), on récupère le scalaire
        score = float(preds[0][0])
        return score

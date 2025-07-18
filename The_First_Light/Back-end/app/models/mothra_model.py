from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

class MothraModel:

    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "mothra_cnn_v1.h5")
        print("Chargement du modèle IA...")
        self.model = load_model(model_path)
        print("✅ Modèle chargé avec succès.")

    def predict(self, img_path):
        # Chargement et pré-traitement de l'image
        img = image.load_img(img_path, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Prédiction
        prediction = self.model.predict(img_array)[0][0]
        return float(prediction)  # retourne un float simple

# Variable globale pour l'instance unique (sera assignée au démarrage)
mothra_model_instance = None

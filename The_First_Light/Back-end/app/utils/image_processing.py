from PIL import Image
import numpy as np

def preprocess_image(image_path: str, target_size=(128, 128)) -> np.ndarray:
    """
    Charge une image depuis un chemin, la redimensionne, la convertit en tableau numpy,
    normalise les pixels entre 0 et 1 et ajoute une dimension batch (1, h, w, c).

    Args:
        image_path (str): chemin vers l'image à charger
        target_size (tuple): taille cible (largeur, hauteur)

    Returns:
        np.ndarray: image prête à être passée au modèle, shape (1, h, w, c)
    """
    img = Image.open(image_path).convert("RGB")          # Charger et forcer RGB
    img = img.resize(target_size)                        # Redimensionner
    img_array = np.array(img) / 255.0                    # Normaliser pixels
    img_array = np.expand_dims(img_array, axis=0)       # Ajouter batch dimension
    return img_array

import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

def test_image(img_path, model_path="models/mothra_cnn_v1.h5"):
    # Charger le modèle sauvegardé
    model = load_model(model_path)

    # Charger et préparer l'image
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter la dimension batch

    # Prédiction
    prediction = model.predict(img_array)[0][0]
    print(f"Probabilité d’être malin : {prediction:.4f}")

    if prediction > 0.5:
        print("➡️ Le modèle pense que c'est **MALIN** (mélanome)")
    else:
        print("➡️ Le modèle pense que c'est **BENIN** (grain de beauté)")

if __name__ == "__main__":
    # Chemin vers ton image de test à adapter
    img_path = '/workspaces/Mothra/The_First_Light/V1/test_mothra/data_test/benin/bn_1.jpg'
    test_image(img_path)

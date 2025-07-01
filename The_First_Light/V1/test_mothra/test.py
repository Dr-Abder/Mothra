import numpy as np
from tensorflow.keras.preprocessing import image

img_path = '/content/test_upu/benin/bn_1.jpg'  # à adapter
img = image.load_img(img_path, target_size=(128, 128))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)[0][0]
print("Probabilité d’être malin :", prediction)

if prediction > 0.5:
    print("➡️ Le modèle pense que c'est **MALIN** (mélanome)")
else:
    print("➡️ Le modèle pense que c'est **BENIN** (grain de beauté)")
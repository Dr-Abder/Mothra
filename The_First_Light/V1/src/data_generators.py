from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Création d’un générateur avec normalisation et split auto
datagen = ImageDataGenerator(
    rescale=1./255,        # Normalisation des pixels (0-1)
    validation_split=0.2   # 80% entraînement / 20% validation
)

# 📦 Générateur d'entraînement
train_generator = datagen.flow_from_directory(
    "dataset",             # Racine contenant /benin et /malin
    target_size=(128, 128),# Redimensionnement
    batch_size=32,
    class_mode='binary',   # 0 ou 1 : car classification binaire
    subset='training'      # 80% ici
)

# 📦 Générateur de validation
val_generator = datagen.flow_from_directory(
    "dataset",
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='validation'    # 20% ici
)

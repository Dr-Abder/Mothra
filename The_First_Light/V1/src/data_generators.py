from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Création d’un générateur avec normalisation et split auto
datagen = ImageDataGenerator(
    rescale=1./255,        
    validation_split=0.2
)


train_generator = datagen.flow_from_directory(
    "dataset",
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='training'     
)


val_generator = datagen.flow_from_directory(
    "dataset",
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)

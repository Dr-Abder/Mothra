from tensorflow.keras import layers, models

def build_model():
    model = models.Sequential([
        layers.Input(shape=(128, 128, 3)),              # Entrée : image 128x128 RGB

        layers.Conv2D(32, (3, 3), activation='relu'),   # 1er bloc convolution / filtres
        layers.MaxPooling2D(pool_size=(2, 2)),

        layers.Conv2D(64, (3, 3), activation='relu'),   # 2e bloc
        layers.MaxPooling2D(pool_size=(2, 2)),

        layers.Conv2D(128, (3, 3), activation='relu'),  # 3e bloc
        layers.MaxPooling2D(pool_size=(2, 2)),

        layers.Flatten(),                               # Données 2D / 1D
        layers.Dense(128, activation='relu'),           # 128 CO
        layers.Dropout(0.5),                            # Pour éviter l’overfitting 50ù

        layers.Dense(1, activation='sigmoid')           # Sortie binaire : 0 / 1
])
    return model

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pickle

from model_architecture import build_model
from src.data_generators import train_generator, val_generator

# 1. Construire le modèle
model = build_model()

# 2. Compiler le modèle
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 3. Entraîner le modèle
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

# Sauvegarde de l'historique d'entraînement
with open("models/history.pkl", "wb") as f:
    pickle.dump(history.history, f)

# 4. Sauvegarder le modèle
model.save("models/mothra_cnn_v1.h5")

print("✅ Modèle entraîné et sauvegardé.")
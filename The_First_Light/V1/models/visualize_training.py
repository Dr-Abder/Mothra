import matplotlib.pyplot as plt
import pickle
import os

# 📦 Optionnel : changer ce chemin si le fichier history est sauvegardé ailleurs
history_path = "models/history.pkl"

# ✅ Charger l'historique de l'entraînement
with open(history_path, "rb") as f:
    history = pickle.load(f)

# 🎯 Extraire les données
acc = history['accuracy']
val_acc = history['val_accuracy']
loss = history['loss']
val_loss = history['val_loss']
epochs = range(1, len(acc) + 1)

# 📊 Tracer les courbes
plt.figure(figsize=(12, 5))

# Accuracy
plt.subplot(1, 2, 1)
plt.plot(epochs, acc, 'b-', label='Train accuracy')
plt.plot(epochs, val_acc, 'g-', label='Val accuracy')
plt.title('Accuracy over epochs')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# Loss
plt.subplot(1, 2, 2)
plt.plot(epochs, loss, 'r-', label='Train loss')
plt.plot(epochs, val_loss, 'orange', label='Val loss')
plt.title('Loss over epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig("notebooks/training_metrics.png")
plt.show()
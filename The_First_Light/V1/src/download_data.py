import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

# 🔁 Récupérer le chemin absolu du projet
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 📁 Fichier source = ton kaggle.json dans /V1/kaggle/
kaggle_json_src = os.path.join(base_dir, "kaggle", "kaggle.json")

# 📁 Dossier cible = ~/.config/kaggle (exigé par l'API)
kaggle_config_dir = os.path.expanduser("~/.config/kaggle")
kaggle_json_dst = os.path.join(kaggle_config_dir, "kaggle.json")

# 📦 Créer le dossier ~/.config/kaggle si besoin
os.makedirs(kaggle_config_dir, exist_ok=True)

# 📤 Copier kaggle.json dans le bon dossier
shutil.copy(kaggle_json_src, kaggle_json_dst)
os.chmod(kaggle_json_dst, 0o600)  # 🔐 Permissions sécurisées

# ✅ Authentification et téléchargement
api = KaggleApi()
api.authenticate()

api.dataset_download_files(
    'kmader/skin-cancer-mnist-ham10000',
    path=os.path.join(base_dir, 'data'),
    unzip=True
)

print("✅ Dataset téléchargé et extrait dans le dossier 'data/'")

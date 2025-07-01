import os
import shutil

# 1. Config des chemins
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kaggle_json_src = os.path.join(base_dir, "kaggle", "kaggle.json")
kaggle_config_dir = os.path.expanduser("~/.config/kaggle")
kaggle_json_dst = os.path.join(kaggle_config_dir, "kaggle.json")

# 2. Copier et sécuriser
os.makedirs(kaggle_config_dir, exist_ok=True)
shutil.copy(kaggle_json_src, kaggle_json_dst)
os.chmod(kaggle_json_dst, 0o600)

# ✅ 3. Import seulement maintenant que le fichier est bien copié
from kaggle.api.kaggle_api_extended import KaggleApi

# 4. Authentification et téléchargement
api = KaggleApi()
api.authenticate()

api.dataset_download_files(
    'kmader/skin-cancer-mnist-ham10000',
    path=os.path.join(base_dir, 'data'),
    unzip=True
)

print("✅ Dataset téléchargé et extrait dans le dossier 'data/'")

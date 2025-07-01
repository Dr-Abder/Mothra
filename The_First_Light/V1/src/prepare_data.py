import os
import pandas as pd
import shutil

# Chemins
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_dir, 'data')
metadata_path = os.path.join(data_dir, 'HAM10000_metadata.csv')
image_dirs = [
    os.path.join(data_dir, 'HAM10000_images_part_1'),
    os.path.join(data_dir, 'HAM10000_images_part_2')
]

# Chargement du CSV
df = pd.read_csv(metadata_path)

# Garde seulement 'mel' (malin) et 'nv' (bénin)
df = df[df['dx'].isin(['mel', 'nv'])]

# Création des dossiers
dataset_dir = os.path.join(base_dir, 'dataset')
benin_dir = os.path.join(dataset_dir, 'benin')
malin_dir = os.path.join(dataset_dir, 'malin')

os.makedirs(benin_dir, exist_ok=True)
os.makedirs(malin_dir, exist_ok=True)

# Fonction de copie
def copy_image(image_id, dx):
    filename = image_id + ".jpg"
    dst_dir = malin_dir if dx == "mel" else benin_dir

    for src_dir in image_dirs:
        src_path = os.path.join(src_dir, filename)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_dir)
            return

# Lancer la copie
for _, row in df.iterrows():
    copy_image(row['image_id'], row['dx'])

print("✅ Images triées et copiées dans 'dataset/benin' et 'dataset/malin'")

# 📸 Système de stockage des images

## Vue d'ensemble

Le système de stockage des images Mothra permet de sauvegarder automatiquement toutes les images uploadées par les utilisateurs lors des prédictions ML.

## Architecture

### Structure des dossiers

```
uploads/
├── {user_id_1}/
│   ├── 20251105_163112_77f4f26b.jpg
│   ├── 20251105_163245_a3b2c1d4.jpg
│   └── ...
├── {user_id_2}/
│   ├── 20251105_164530_e5f6g7h8.jpg
│   └── ...
└── ...
```

### Nom des fichiers

Format: `{timestamp}_{uuid8}.{ext}`
- `timestamp`: Format `YYYYMMDD_HHMMSS`
- `uuid8`: 8 premiers caractères d'un UUID unique
- `ext`: Extension originale (.jpg, .jpeg, .png, .webp)

Exemple: `20251105_163112_77f4f26b.jpg`

## Composants

### 1. StorageService ([services/storage_service.py](../app/services/storage_service.py))

Service singleton pour la gestion du stockage.

**Méthodes principales:**

```python
# Sauvegarder une image
image_path = storage_service.save_image(
    user_id="uuid",
    filename="photo.jpg",
    file_content=b"..."
)
# Retourne: "user_id/20251105_163112_77f4f26b.jpg"

# Récupérer le chemin complet
full_path = storage_service.get_image_path("user_id/20251105_163112_77f4f26b.jpg")

# Supprimer une image
storage_service.delete_image("user_id/20251105_163112_77f4f26b.jpg")

# Supprimer toutes les images d'un utilisateur
storage_service.delete_user_images("user_id")

# Statistiques
stats = storage_service.get_storage_stats()
```

### 2. API Images ([api/images.py](../app/api/images.py))

Routes pour accéder aux images stockées.

**Endpoints:**

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/v1/images/analyses/{analyse_id}/image` | Récupère l'image d'une analyse |
| DELETE | `/api/v1/images/analyses/{analyse_id}/image` | Supprime l'image d'une analyse |
| GET | `/api/v1/images/storage/stats` | Statistiques de stockage |

### 3. Intégration avec l'API de prédiction

Lors d'une prédiction ([api/predict.py:62-67](../app/api/predict.py#L62-L67)):

```python
# Sauvegarder l'image sur le serveur
image_path = storage_service.save_image(
    user_id=current_user.id,
    filename=file.filename,
    file_content=contents
)

# Sauvegarder l'analyse avec le chemin de l'image
analyse = Analyse(
    user_id=current_user.id,
    photo=image_path,  # "user_id/20251105_163112_77f4f26b.jpg"
    diagnostic=prediction_result["diagnostic"],
    confidence=prediction_result["confidence"]
)
```

## Flux complet

```
1. Utilisateur upload une image
   ↓
2. API /predict reçoit l'image
   ↓
3. StorageService sauvegarde l'image
   uploads/{user_id}/{timestamp}_{uuid}.jpg
   ↓
4. ML Service fait la prédiction
   ↓
5. Analyse sauvegardée en BD avec chemin de l'image
   photo = "user_id/timestamp_uuid.jpg"
   ↓
6. Utilisateur peut récupérer l'image via
   GET /api/v1/images/analyses/{analyse_id}/image
```

## Sécurité

### 1. Isolation des utilisateurs
- Chaque utilisateur a son propre dossier
- Les images d'un utilisateur ne sont pas accessibles aux autres

### 2. Vérification des droits
```python
# L'API vérifie que l'analyse appartient à l'utilisateur
if analyse.user_id != current_user.id:
    raise HTTPException(status_code=403)
```

### 3. Validation des formats
Formats supportés: `.jpg`, `.jpeg`, `.png`, `.webp`

### 4. Limite de taille
Taille maximale: 10 MB par image

## Conformité RGPD

### Suppression automatique

**Suppression d'un utilisateur:**
```python
# Supprime toutes les images + compte + analyses
DELETE /api/v1/users/me
```

**Suppression de toutes les analyses:**
```python
# Supprime toutes les images + analyses (conserve le compte)
DELETE /api/v1/users/me/analyses
```

**Suppression d'une image spécifique:**
```python
# Supprime une image (conserve l'analyse en BD)
DELETE /api/v1/images/analyses/{analyse_id}/image
```

### Export des données
Les chemins des images sont inclus dans l'export RGPD:
```python
GET /api/v1/users/me/data-export
```

## Configuration

### Variables d'environnement
Aucune configuration requise par défaut.

### Personnalisation
Pour changer le répertoire de base:

```python
# Dans main.py ou config
storage_service = StorageService(base_upload_dir="/custom/path/uploads")
```

## Maintenance

### Nettoyage manuel
```bash
# Supprimer toutes les images
rm -rf uploads/

# Le dossier sera recréé automatiquement au prochain upload
```

### Sauvegarde
```bash
# Sauvegarder les images
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# Restaurer
tar -xzf uploads_backup_20251105.tar.gz
```

### Monitoring
```python
# Via l'API
GET /api/v1/images/storage/stats

# Retourne:
{
  "user": {
    "user_id": "...",
    "images_count": 5
  },
  "global": {
    "users_count": 10,
    "total_images": 50,
    "total_size_bytes": 5242880,
    "total_size_mb": 5.0
  }
}
```

## Tests

### Test complet
```bash
cd /workspaces/Mothra/The_First_Light/Back-end
python tests/test_image_storage.py
```

### Tests couverts
✅ Upload et sauvegarde d'image
✅ Récupération d'image via API
✅ Format et validation de l'image
✅ Statistiques de stockage
✅ Sécurité (accès interdit entre users)
✅ Suppression d'une image
✅ Suppression de toutes les analyses
✅ Suppression du compte (CASCADE)

## Performance

### Optimisations
- **Singleton**: Une seule instance du service
- **Lazy loading**: Dossiers créés à la demande
- **Noms uniques**: Pas de collisions, pas de vérification nécessaire

### Scalabilité
Pour une production à grande échelle:
1. Utiliser un service cloud (AWS S3, Google Cloud Storage)
2. Implémenter un CDN pour la distribution
3. Ajouter une compression automatique
4. Mettre en place une rotation des logs

## Exemple d'utilisation

### Python (requests)
```python
import requests

# Upload et prédiction
with open("skin_photo.jpg", "rb") as f:
    files = {"file": f}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        "http://localhost:8000/api/v1/predict",
        files=files,
        headers=headers
    )

analyse_id = response.json()["analyse_id"]

# Récupérer l'image
response = requests.get(
    f"http://localhost:8000/api/v1/images/analyses/{analyse_id}/image",
    headers=headers
)

# Sauvegarder localement
with open("downloaded.jpg", "wb") as f:
    f.write(response.content)
```

### cURL
```bash
# Upload
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@skin_photo.jpg"

# Récupérer l'image
curl -X GET "http://localhost:8000/api/v1/images/analyses/$ANALYSE_ID/image" \
  -H "Authorization: Bearer $TOKEN" \
  --output downloaded.jpg
```

## Dépannage

### Erreur 404 - Image introuvable
- L'image a peut-être été supprimée
- Vérifier que l'analyse existe et appartient à l'utilisateur
- Vérifier les permissions du dossier `uploads/`

### Erreur 403 - Accès interdit
- L'utilisateur n'est pas propriétaire de l'analyse
- Vérifier le token JWT

### Dossier uploads/ vide
- Normal si aucune prédiction n'a été faite
- Le dossier est créé automatiquement au premier upload

## Roadmap

### Améliorations futures
- [ ] Compression automatique des images
- [ ] Support de formats additionnels (TIFF, BMP)
- [ ] Génération de thumbnails
- [ ] Watermarking automatique
- [ ] Migration vers cloud storage (S3/GCS)
- [ ] Rotation automatique EXIF
- [ ] Détection de duplicatas
- [ ] Quota par utilisateur

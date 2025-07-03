from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models.mothra_model import MothraModel
from PIL import Image, UnidentifiedImageError
from tempfile import NamedTemporaryFile
import shutil
import os

router = APIRouter()
model = MothraModel()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Mo

@router.post("/")
async def predict_skin_lesion(file: UploadFile = File(...)):
    # 1. Vérifier le type MIME (image uniquement)
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier doit être une image (jpeg, png, etc.)."
        )
    
    # 2. Vérifier la taille du fichier
    file_size = 0
    try:
        contents = await file.read()
        file_size = len(contents)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le fichier est trop volumineux (max {MAX_FILE_SIZE // (1024*1024)} Mo)."
            )
    finally:
        await file.seek(0)  # Remettre le curseur au début pour la suite

    # 3. Sauvegarder temporairement le fichier uploadé
    tmp_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # 4. Vérifier que le fichier est une image valide
        try:
            img = Image.open(tmp_path)
            img.verify()  # Vérifie l’intégrité de l’image
        except (UnidentifiedImageError, OSError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le fichier uploadé n'est pas une image valide."
            )

        # 5. Faire la prédiction
        prediction_score = model.predict(tmp_path)

    except HTTPException:
        raise  # Propager les erreurs HTTP levées précédemment
    except Exception as e:
        # Erreur inattendue
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la prédiction : {str(e)}"
        )
    finally:
        file.file.close()
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    # 6. Interpréter le score
    result = "MALIN" if prediction_score > 0.5 else "BENIN"

    return {
        "prediction_score": prediction_score,
        "result": result
    }

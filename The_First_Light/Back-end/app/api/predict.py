from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.models.mothra_model import MothraModel
from PIL import Image, UnidentifiedImageError
from tempfile import NamedTemporaryFile
import shutil
import os

router = APIRouter()
model = None  # Lazy load du modèle

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Mo

def get_model():
    global model
    if model is None:
        model = MothraModel()
    return model

@router.post("/")
async def predict_skin_lesion(file: UploadFile = File(...)):
    # 1. Vérifier le type MIME
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier doit être une image (jpeg, png, etc.)."
        )
    
    # 2. Vérifier la taille
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Le fichier est trop volumineux (max {MAX_FILE_SIZE // (1024*1024)} Mo)."
            )
    finally:
        await file.seek(0)

    tmp_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        try:
            img = Image.open(tmp_path)
            img.verify()
        except (UnidentifiedImageError, OSError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Le fichier uploadé n'est pas une image valide."
            )

        prediction_score = get_model().predict(tmp_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur serveur lors de la prédiction : {str(e)}"
        )
    finally:
        file.file.close()
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    result = "MALIN" if prediction_score > 0.5 else "BENIN"

    return {
        "prediction_score": prediction_score,
        "result": result
    }

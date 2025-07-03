from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.mothra_model import MothraModel
from app.utils.image_processing import preprocess_image
from app.schemas.predict_schema import PredictionResponse
import shutil
import os
from tempfile import NamedTemporaryFile
import numpy as np

router = APIRouter()

# Charger le modèle une seule fois au démarrage
model = MothraModel()

@router.post("/predict")
async def predict_skin_lesion(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Le fichier doit être une image")

    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        # Prétraiter l'image
        img_array = preprocess_image(tmp_path)

        # Prédire avec le modèle (img_array, pas le chemin)
        prediction_score = model.predict(img_array)

    finally:
        file.file.close()
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    result = "MALIN" if prediction_score > 0.5 else "BENIN"

    return {
        "prediction_score": prediction_score,
        "result": result
    }

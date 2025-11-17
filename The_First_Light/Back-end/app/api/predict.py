"""
Route de prédiction ML - Upload d'image et diagnostic avec modèle CNN
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from datetime import datetime
import os

from app.models.User import User
from app.models.Analyse import Analyse
from app.schemas import PredictionResponse, PredictionResult, AnalyseResponse
from app.services.auth_utils import get_current_user
from app.services.ml_service import get_ml_service
from app.services.storage_service import get_storage_service

router = APIRouter(tags=["Prediction"])

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


@router.post("", response_model=PredictionResponse)
async def predict_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload d'une image pour prédiction/diagnostic avec le modèle Mothra CNN

    - **file**: Image à analyser (formats: jpg, jpeg, png, webp, max 10MB)

    Retourne un diagnostic avec le niveau de confiance du modèle de Deep Learning.

    Le modèle analyse l'image (128x128) et détecte les anomalies cutanées.
    """

    # Vérifier l'extension du fichier
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Format de fichier non supporté. Utilisez: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Lire le contenu du fichier
    try:
        contents = await file.read()
        file_size = len(contents)

        # Vérifier la taille du fichier
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Fichier trop volumineux. Taille max: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Obtenir les services
        ml_service = get_ml_service()
        storage_service = get_storage_service()

        # Sauvegarder l'image sur le serveur
        image_path = storage_service.save_image(
            user_id=current_user.id,
            filename=file.filename,
            file_content=contents
        )

        # Faire la prédiction avec le vrai modèle
        prediction_result = ml_service.get_detailed_prediction(contents)

        # Sauvegarder automatiquement l'analyse dans la base de données
        analyse = Analyse(
            user_id=current_user.id,
            photo=image_path,  # Chemin relatif de l'image
            diagnostic=prediction_result["diagnostic"],
            confidence=prediction_result["confidence"]
        )
        analyse.save()

        # Créer l'objet PredictionResult
        prediction = PredictionResult(
            diagnostic=prediction_result["diagnostic"],
            confidence=prediction_result["confidence"],
            model_version=prediction_result["model_version"],
            timestamp=datetime.now().isoformat()
        )

        return PredictionResponse(
            success=True,
            prediction=prediction,
            message=f"Prédiction réussie - Classe: {prediction_result['class_name']} - {prediction_result['recommendation']}"
        )

    except HTTPException:
        raise
    except Exception as e:
        # Log l'erreur (en production, utiliser un vrai logger)
        print(f"❌ Erreur prédiction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse de l'image: {str(e)}"
        )

"""
Route de prédiction ML - Upload d'image et diagnostic
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Depends
from datetime import datetime

from models.User import User
from schemas import PredictionResponse, PredictionResult
from services.auth_utils import get_current_user

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
    Upload d'une image pour prédiction/diagnostic

    - **file**: Image à analyser (formats: jpg, jpeg, png, webp, max 10MB)

    Retourne un diagnostic avec le niveau de confiance.

    ⚠️ Note: Cette version est un mock. Intégrez votre modèle ML ici.
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

        # TODO: Intégrer votre modèle ML ici
        # Pour l'instant, on retourne un résultat mock
        prediction = mock_prediction(file.filename)

        return PredictionResponse(
            success=True,
            prediction=prediction,
            message="Prédiction effectuée avec succès (mock)"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'analyse: {str(e)}"
        )


def mock_prediction(filename: str) -> PredictionResult:
    """
    Fonction mock pour la prédiction
    TODO: Remplacer par votre vrai modèle ML
    """
    import random

    diagnostics = [
        "Mélanome détecté - Consultation urgente recommandée",
        "Carcinome basocellulaire suspect - Consultez un dermatologue",
        "Kératose actinique détectée - Surveillance recommandée",
        "Naevus bénin - Pas d'inquiétude",
        "Peau normale - Aucune anomalie détectée"
    ]

    diagnostic = random.choice(diagnostics)
    confidence = random.uniform(0.75, 0.99)

    return PredictionResult(
        diagnostic=diagnostic,
        confidence=round(confidence, 2),
        model_version="mothra-v1.0",
        timestamp=datetime.now().isoformat()
    )

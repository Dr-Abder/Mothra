"""
Routes pour la gestion des analyses
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.User import User
from app.models.Analyse import Analyse
from schemas import AnalyseCreate, AnalyseResponse, SuccessResponse
from app.services.auth_utils import get_current_user

router = APIRouter(tags=["Analyses"])


@router.post("", response_model=AnalyseResponse, status_code=status.HTTP_201_CREATED)
async def create_analyse(
    analyse_data: AnalyseCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Créer une nouvelle analyse/diagnostic

    - **photo**: Nom ou URL de l'image (formats: jpg, jpeg, png, webp)
    - **diagnostic**: Résultat du diagnostic (max 2000 caractères)
    - **confidence**: Niveau de confiance (0.0 à 1.0)

    L'analyse sera automatiquement liée au compte utilisateur connecté
    """

    try:
        analyse = Analyse(
            user_id=current_user.id,
            photo=analyse_data.photo,
            diagnostic=analyse_data.diagnostic,
            confidence=analyse_data.confidence
        )
        analyse.save()

        return analyse.to_dict()

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'analyse: {str(e)}"
        )


@router.get("/{analyse_id}", response_model=AnalyseResponse)
async def get_analyse(
    analyse_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Récupérer une analyse spécifique par son ID

    L'utilisateur ne peut accéder qu'à ses propres analyses
    """

    analyse = Analyse.get_by_id(analyse_id)

    if not analyse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analyse non trouvée"
        )

    # Vérifier que l'analyse appartient bien à l'utilisateur connecté
    if analyse.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas accès à cette analyse"
        )

    return analyse.to_dict()


@router.get("", response_model=List[AnalyseResponse])
async def get_my_analyses(current_user: User = Depends(get_current_user)):
    """
    Récupérer toutes mes analyses

    Retourne la liste de toutes les analyses de l'utilisateur connecté,
    triées par date de création (plus récentes en premier)
    """

    try:
        analyses = Analyse.get_by_user(current_user.id)
        return [analyse.to_dict() for analyse in analyses]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des analyses: {str(e)}"
        )


@router.delete("/{analyse_id}", response_model=SuccessResponse)
async def delete_analyse(
    analyse_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Supprimer une analyse

    L'utilisateur ne peut supprimer que ses propres analyses
    """

    analyse = Analyse.get_by_id(analyse_id)

    if not analyse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analyse non trouvée"
        )

    # Vérifier que l'analyse appartient bien à l'utilisateur connecté
    if analyse.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas la permission de supprimer cette analyse"
        )

    try:
        analyse.delete()
        return SuccessResponse(
            message=f"Analyse {analyse_id} supprimée avec succès"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression: {str(e)}"
        )

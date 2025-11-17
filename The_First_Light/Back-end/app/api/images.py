"""
Routes pour la récupération des images stockées
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import FileResponse
from pathlib import Path

from app.models.User import User
from app.models.Analyse import Analyse
from app.services.auth_utils import get_current_user, get_current_user_from_query
from app.services.storage_service import get_storage_service

router = APIRouter(tags=["Images"])


@router.get("/analyses/{analyse_id}/image")
async def get_analyse_image(
    analyse_id: str,
    token: str = None,
    current_user: User = Depends(get_current_user_from_query)
):
    """
    Récupère l'image associée à une analyse

    - **analyse_id**: ID de l'analyse
    - **token**: Token JWT d'authentification (en query parameter)

    L'utilisateur ne peut récupérer que les images de ses propres analyses.
    """
    # Récupérer l'analyse
    analyse = Analyse.get_by_id(analyse_id)

    if not analyse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analyse introuvable"
        )

    # Vérifier que l'analyse appartient à l'utilisateur
    if analyse.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas accès à cette image"
        )

    # Récupérer le chemin de l'image
    storage_service = get_storage_service()
    image_path = storage_service.get_image_path(analyse.photo)

    if not image_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image introuvable sur le serveur"
        )

    # Déterminer le type MIME
    ext = image_path.suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp'
    }
    media_type = media_types.get(ext, 'image/jpeg')

    # Retourner l'image
    return FileResponse(
        path=image_path,
        media_type=media_type,
        filename=image_path.name
    )


@router.get("/storage/stats")
async def get_storage_stats(current_user: User = Depends(get_current_user)):
    """
    Récupère les statistiques de stockage de l'utilisateur

    Retourne le nombre d'images et l'espace utilisé.
    """
    storage_service = get_storage_service()

    # Stats utilisateur
    user_images_count = storage_service.get_user_images_count(current_user.id)

    # Stats globales (pour info)
    global_stats = storage_service.get_storage_stats()

    return {
        "user": {
            "user_id": current_user.id,
            "images_count": user_images_count
        },
        "global": global_stats
    }


@router.delete("/analyses/{analyse_id}/image")
async def delete_analyse_image(
    analyse_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Supprime l'image associée à une analyse

    - **analyse_id**: ID de l'analyse

    ATTENTION: Cette action est irréversible!
    """
    # Récupérer l'analyse
    analyse = Analyse.get_by_id(analyse_id)

    if not analyse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analyse introuvable"
        )

    # Vérifier que l'analyse appartient à l'utilisateur
    if analyse.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas accès à cette image"
        )

    # Supprimer l'image du serveur
    storage_service = get_storage_service()
    success = storage_service.delete_image(analyse.photo)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image introuvable sur le serveur"
        )

    return {
        "success": True,
        "message": "Image supprimée avec succès"
    }

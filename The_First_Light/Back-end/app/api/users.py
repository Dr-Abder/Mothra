"""
Routes utilisateur: gestion du compte + RGPD
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime

from models.User import User
from models.Analyse import Analyse
from schemas import UserResponse, UserUpdate, UserDataExport, SuccessResponse
from services.auth_utils import get_current_user

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Récupérer les informations de mon compte

    Nécessite un token JWT valide dans le header Authorization
    """
    return current_user.to_dict()


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Mettre à jour mes informations personnelles

    Tous les champs sont optionnels. Seuls les champs fournis seront mis à jour.

    - **first_name**: Nouveau prénom
    - **last_name**: Nouveau nom
    - **email**: Nouvel email
    - **age**: Nouvel âge
    - **sex**: Nouveau sexe
    - **password**: Nouveau mot de passe (doit respecter les critères de sécurité)
    """

    try:
        # Mettre à jour les champs modifiés
        if update_data.first_name is not None:
            current_user.first_name = current_user.valide_name(update_data.first_name)

        if update_data.last_name is not None:
            current_user.last_name = current_user.valide_name(update_data.last_name)

        if update_data.email is not None:
            # Vérifier si le nouvel email n'est pas déjà utilisé
            if update_data.email != current_user.email:
                existing_user = User.get_by_email(update_data.email)
                if existing_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Cet email est déjà utilisé"
                    )
            current_user.email = current_user.valide_email(update_data.email)

        if update_data.age is not None:
            current_user.age = current_user.valide_age(update_data.age)

        if update_data.sex is not None:
            current_user.sex = current_user.valide_sex(update_data.sex)

        if update_data.password is not None:
            current_user.valide_password(update_data.password)
            current_user.password_hash = current_user.hash_password(update_data.password)

        # Sauvegarder les modifications
        current_user.update()

        # Récupérer l'utilisateur mis à jour
        updated_user = User.get_by_id(current_user.id)
        return updated_user.to_dict()

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour: {str(e)}"
        )


@router.delete("/me", response_model=SuccessResponse)
async def delete_my_account(current_user: User = Depends(get_current_user)):
    """
    Supprimer mon compte (conformité RGPD)

    Supprime définitivement le compte utilisateur et toutes les analyses associées
    grâce au CASCADE DELETE configuré dans la base de données.

    ⚠️ Cette action est irréversible !
    """

    try:
        user_id = current_user.id
        current_user.delete()

        return SuccessResponse(
            message=f"Compte {user_id} supprimé définitivement (RGPD)"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du compte: {str(e)}"
        )


@router.get("/me/data-export", response_model=UserDataExport)
async def export_my_data(current_user: User = Depends(get_current_user)):
    """
    Exporter toutes mes données personnelles (conformité RGPD)

    Retourne un export JSON complet de toutes les données:
    - Informations du compte utilisateur
    - Liste de toutes les analyses effectuées
    - Date de l'export

    Cet export peut être utilisé pour la portabilité des données (droit RGPD)
    """

    try:
        # Récupérer toutes les analyses de l'utilisateur
        analyses = Analyse.get_by_user(current_user.id)
        analyses_data = [analyse.to_dict() for analyse in analyses]

        # Préparer l'export complet
        export_data = UserDataExport(
            user=current_user.to_dict(),
            analyses=analyses_data,
            export_date=datetime.now().isoformat()
        )

        return export_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'export des données: {str(e)}"
        )


@router.delete("/me/analyses", response_model=SuccessResponse)
async def delete_all_my_analyses(current_user: User = Depends(get_current_user)):
    """
    Supprimer toutes mes analyses

    Supprime toutes les analyses liées au compte utilisateur
    tout en conservant le compte actif.
    """

    try:
        # Récupérer toutes les analyses
        analyses = Analyse.get_by_user(current_user.id)

        # Supprimer chaque analyse
        count = 0
        for analyse in analyses:
            analyse.delete()
            count += 1

        return SuccessResponse(
            message=f"{count} analyse(s) supprimée(s) avec succès"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression des analyses: {str(e)}"
        )

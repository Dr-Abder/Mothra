"""
Routes d'authentification: signup, login, logout
"""

from fastapi import APIRouter, HTTPException, status
from datetime import timedelta

from app.models.User import User
from app.schemas import UserSignup, UserLogin, Token, SuccessResponse
from app.services.auth_utils import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignup):
    """
    Créer un nouveau compte utilisateur

    - **first_name**: Prénom (1-50 caractères)
    - **last_name**: Nom (1-50 caractères)
    - **email**: Email valide et unique
    - **password**: Min 8 caractères, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial
    - **age**: Âge (> 0)
    - **sex**: "homme" ou "femme"
    - **consent_rgpd**: Consentement RGPD (obligatoire)
    """

    # Vérifier si l'email existe déjà
    existing_user = User.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cet email existe déjà"
        )

    # Créer l'utilisateur
    try:
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password=user_data.password,
            age=user_data.age,
            sex=user_data.sex
        )
        user.save()

        # Créer le token JWT
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )

        return Token(access_token=access_token, user_id=user.id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du compte: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Connexion utilisateur

    - **email**: Email du compte
    - **password**: Mot de passe

    Retourne un token JWT pour l'authentification des requêtes suivantes
    """

    # Récupérer l'utilisateur par email
    user = User.get_by_email(credentials.email)

    # Vérifier si l'utilisateur existe et le mot de passe est correct
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Créer le token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, user_id=user.id)


@router.post("/logout", response_model=SuccessResponse)
async def logout():
    """
    Déconnexion utilisateur

    Note: Avec JWT, la déconnexion est gérée côté client en supprimant le token.
    Cette route est optionnelle et peut être utilisée pour implémenter un blacklist de tokens.
    """
    return SuccessResponse(
        message="Déconnexion réussie. Supprimez le token côté client."
    )

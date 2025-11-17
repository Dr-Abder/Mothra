"""
Utilitaires pour l'authentification JWT
"""
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.User import User
from schemas import TokenData

# Configuration JWT
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Créer un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Vérifier et décoder un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(user_id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Obtenir l'utilisateur connecté depuis le token JWT"""
    token = credentials.credentials
    token_data = verify_token(token)

    user = User.get_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )

    return user


async def get_current_user_from_query(token: Optional[str] = None) -> User:
    """
    Obtenir l'utilisateur connecté depuis le token JWT passé en query parameter
    Utilisé pour les requêtes d'images où on ne peut pas mettre le token dans le header
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token manquant",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = verify_token(token)

    user = User.get_by_id(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )

    return user


def hash_password(password: str) -> str:
    """Hash un mot de passe avec bcrypt"""
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    import bcrypt
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

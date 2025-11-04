"""
Schémas Pydantic pour la validation des requêtes/réponses API
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import re


# ==================== AUTH SCHEMAS ====================

class UserSignup(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int = Field(..., gt=0)
    sex: str = Field(..., pattern="^(homme|femme)$")
    consent_rgpd: bool = True

    @validator('password')
    def validate_password(cls, v):
        if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", v):
            raise ValueError(
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une majuscule, une minuscule, un chiffre et un caractère spécial"
            )
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


# ==================== USER SCHEMAS ====================

class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    age: int
    sex: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0)
    sex: Optional[str] = Field(None, pattern="^(homme|femme)$")
    password: Optional[str] = Field(None, min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", v):
                raise ValueError(
                    "Le mot de passe doit contenir au moins 8 caractères, "
                    "une majuscule, une minuscule, un chiffre et un caractère spécial"
                )
        return v


class UserDataExport(BaseModel):
    user: UserResponse
    analyses: List[dict]
    export_date: str


# ==================== ANALYSE SCHEMAS ====================

class AnalyseCreate(BaseModel):
    photo: str = Field(..., description="URL ou nom de fichier de l'image")
    diagnostic: str = Field(..., min_length=1, max_length=2000)
    confidence: float = Field(..., ge=0.0, le=1.0)

    @validator('photo')
    def validate_photo(cls, v):
        if not v.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            raise ValueError("Format de photo non supporté. Utilisez: jpg, jpeg, png, webp")
        return v


class AnalyseResponse(BaseModel):
    id: str
    user_id: str
    photo: str
    diagnostic: str
    confidence: float
    created_at: str

    class Config:
        from_attributes = True


# ==================== PREDICTION SCHEMAS ====================

class PredictionResult(BaseModel):
    diagnostic: str
    confidence: float
    model_version: str = "mothra-v1.0"
    timestamp: str


class PredictionResponse(BaseModel):
    success: bool
    prediction: PredictionResult
    message: Optional[str] = None


# ==================== INFO SCHEMAS ====================

class ModelInfo(BaseModel):
    name: str = "Mothra"
    version: str = "1.0"
    description: str = "Modèle de détection des maladies de la peau"
    accuracy: float = 0.95
    classes: List[str] = [
        "Mélanome",
        "Carcinome basocellulaire",
        "Carcinome épidermoïde",
        "Kératose actinique",
        "Naevus",
        "Normal"
    ]


class ProjectInfo(BaseModel):
    name: str
    version: str
    status: str
    description: str
    release_date: Optional[str] = None


class RGPDInfo(BaseModel):
    title: str = "Politique de confidentialité RGPD"
    last_updated: str
    sections: List[dict]


# ==================== ERROR SCHEMAS ====================

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    message: str
    success: bool = True

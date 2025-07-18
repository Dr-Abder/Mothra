from pydantic import BaseSettings

class Settings(BaseSettings):
    MODEL_PATH: str = "app/models/mothra_cnn_v1.h5"  # chemin relatif vers ton modèle entraîné
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    class Config:
        env_file = ".env"  # optionnel, pour charger les variables d'environnement

settings = Settings()

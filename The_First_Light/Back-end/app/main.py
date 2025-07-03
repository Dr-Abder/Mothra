from fastapi import FastAPI
from app.api import predict
from app.models.mothra_model import MothraModel, mothra_model_instance
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mothra_model_instance
    mothra_model_instance = MothraModel()  # initialisation au démarrage
    yield
    # ici tu peux ajouter un code pour la fermeture propre, si besoin

app = FastAPI(
    title="Mothra Skin Cancer Detection API",
    description="API pour prédire si un grain de beauté est bénin ou malin à partir d'une image.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(predict.router, prefix="/predict")

@app.get("/")
def root():
    return {"message": "Bienvenue sur Mothra🦋."}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict
from app.models.mothra_model import MothraModel, mothra_model_instance
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global mothra_model_instance
    mothra_model_instance = MothraModel()
    yield

# 1. Créer l'app FastAPI
app = FastAPI(
    title="Mothra Skin Cancer Detection API",
    description="API pour prédire si un grain de beauté est bénin ou malin à partir d'une image.",
    version="1.0.0",
    lifespan=lifespan,
)

# 2. Ajouter CORS middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclure le router de prédiction
app.include_router(predict.router, prefix="/predict")

@app.get("/")
def root():
    return {"message": "Bienvenue sur Mothra🦋."}

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from app.api import predict

# 1. Créer l'app FastAPI
app = FastAPI(
    title="Mothra Skin Cancer Detection API",
    description="API pour prédire si un grain de beauté est bénin ou malin à partir d'une image.",
    version="1.0.0"
)

# 2. Ajouter le CORS middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://mothra-v1.vercel.app",  # <-- CORRECT
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # utilise la variable origins ici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inclure les routes
app.include_router(predict.router, prefix="/predict")

# 4. Route d’accueil simple
@app.get("/")
def root():
    return {"message": "Bienvenue sur Mothra 🦋"}

from fastapi import FastAPI
from app.api import predict

app = FastAPI(
    title="Mothra Skin Cancer Detection API",
    description="API pour prédire si un grain de beauté est bénin ou malin à partir d'une image.",
    version="1.0.0",
)

# Inclure le routeur /api/predict
app.include_router(predict.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Bienvenue sur Mothra🦋."}

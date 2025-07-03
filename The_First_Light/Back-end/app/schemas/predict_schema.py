from pydantic import BaseModel

class PredictionResponse(BaseModel):
    prediction: str          # "benin" ou "malin"
    probability: float      # probabilité entre 0 et 1

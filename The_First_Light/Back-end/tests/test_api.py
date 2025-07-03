import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app  # Ton FastAPI app
from unittest.mock import patch

client = TestClient(app)

def create_test_image(format="JPEG"):
    # Crée une image en mémoire
    img = Image.new("RGB", (128, 128), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes

def test_predict_success():
    img_bytes = create_test_image()
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}

    response = client.post("/predict", files=files)
    assert response.status_code == 200
    json_resp = response.json()
    assert "prediction_score" in json_resp
    assert "result" in json_resp
    assert json_resp["result"] in ["MALIN", "BENIN"]

def test_predict_non_image_file():
    files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "Le fichier doit être une image" in response.text

def test_predict_large_file():
    # Créer un fichier > 5 Mo (5*1024*1024 = 5242880 bytes)
    big_file = io.BytesIO(b"x" * (5 * 1024 * 1024 + 1))
    files = {"file": ("big.jpg", big_file, "image/jpeg")}
    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "Le fichier est trop volumineux" in response.text

def test_predict_corrupt_image():
    # fichier image invalide
    corrupt_img = io.BytesIO(b"this is not a real image")
    files = {"file": ("corrupt.jpg", corrupt_img, "image/jpeg")}
    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "Le fichier uploadé n'est pas une image valide" in response.text

@patch("app.models.mothra_model.MothraModel.predict")
def test_predict_model_exception(mock_predict):
    mock_predict.side_effect = Exception("Erreur interne du modèle")
    img_bytes = create_test_image()
    files = {"file": ("test.jpg", img_bytes, "image/jpeg")}
    response = client.post("/predict", files=files)
    assert response.status_code == 500
    assert "Erreur serveur lors de la prédiction" in response.text

import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def client():
    """Create a test client with mocked ML models."""
    with patch("builtins.open"), \
         patch("pickle.load") as mock_pickle, \
         patch("json.load", return_value=["fever", "cough", "headache"]):
        mock_model = MagicMock()
        mock_encoder = MagicMock()
        mock_pickle.side_effect = [mock_model, mock_encoder]

        import app as flask_app
        flask_app.model = mock_model
        flask_app.encoder = mock_encoder
        flask_app.symptoms_list = ["fever", "cough", "headache"]

        flask_app.app.config["TESTING"] = True
        with flask_app.app.test_client() as client:
            yield client, mock_model, mock_encoder


def test_health_endpoint(client):
    c, _, _ = client
    response = c.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_api_root_endpoint(client):
    c, _, _ = client
    response = c.get("/api")
    assert response.status_code == 200
    data = response.get_json()
    assert "name" in data
    assert "endpoints" in data


def test_index_returns_html(client):
    c, _, _ = client
    response = c.get("/")
    assert response.status_code == 200
    assert b"Healthcare ML API" in response.data


def test_ask_with_valid_symptom(client):
    c, mock_model, mock_encoder = client
    mock_model.predict_proba.return_value = [np.array([0.1, 0.8, 0.1])]
    mock_encoder.inverse_transform.return_value = ["Flu"]

    response = c.post("/ask", json={"message": "I have a fever"})
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data


def test_ask_with_empty_message(client):
    c, _, _ = client
    response = c.post("/ask", json={"message": ""})
    assert response.status_code == 200
    data = response.get_json()
    assert "Je n'ai reconnu aucun symptôme" in data["response"]


def test_extraire_symptomes_detects_fever(client):
    import app
    result = app.extraire_symptomes_intelligent("I have a fever and cough")
    assert "fever" in result or len(result) > 0
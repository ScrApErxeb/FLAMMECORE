from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_execute_actions():
    payload = {
        "actions": [
            {"type": "echo", "message": "test unitaire"},
            {"type": "add", "a": 3, "b": 4}
        ]
    }

    response = client.post("/execute", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2

    first = data["results"][0]
    assert first["status"] == "success"
    assert first["result"] == "test unitaire"

    second = data["results"][1]
    assert second["status"] == "success"
    assert second["result"] == 7

from fastapi.testclient import TestClient
from maint.main import app

client = TestClient(app)


def test_high_and_low():
    assert client.post("/score", json={'vibration': 4, 'temp_c': 95, 'hours': 8000}).json()["label"]
    high = client.post("/score", json={'vibration': 4, 'temp_c': 95, 'hours': 8000}).json()
    low = client.post("/score", json={'vibration': 0.4, 'temp_c': 40, 'hours': 100}).json()
    assert high["label"] != low["label"]
    assert high["score"] > low["score"]


def test_missing_is_refused():
    body = dict({'vibration': 4, 'temp_c': 95, 'hours': 8000})
    body.pop("vibration")
    assert client.post("/score", json=body).status_code == 422

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_get_item():
    resp = client.post("/items", json={"name": "Widget", "price": 9.99})
    assert resp.status_code == 201
    item_id = resp.json()["id"]

    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Widget"


def test_list_items():
    resp = client.get("/items")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_missing_item():
    resp = client.get("/items/99999")
    assert resp.status_code == 404


def test_delete_item():
    resp = client.post("/items", json={"name": "Temp", "price": 1.00})
    item_id = resp.json()["id"]

    resp = client.delete(f"/items/{item_id}")
    assert resp.status_code == 204

    resp = client.get(f"/items/{item_id}")
    assert resp.status_code == 404

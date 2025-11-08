from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_service():
    response = client.post(
        "/api/v1/services", json={"name": "UnitTest", "status": "Running"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "UnitTest"
    assert "id" in data


def test_get_all_services():
    response = client.get("/api/v1/services")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_service():
    post_resp = client.post(
        "/api/v1/services", json={"name": "ToUpdate", "status": "Running"}
    )
    service_id = post_resp.json()["id"]

    put_resp = client.put(
        f"/api/v1/services/{service_id}", json={"name": "ToUpdate", "status": "Stopped"}
    )
    assert put_resp.status_code == 200
    assert put_resp.json()["status"] == "Stopped"


def test_delete_service():
    post_resp = client.post(
        "/api/v1/services", json={"name": "TempService", "status": "Running"}
    )
    service_id = post_resp.json()["id"]

    delete_resp = client.delete(f"/api/v1/services/{service_id}")
    assert delete_resp.status_code == 200
    assert "deleted successfully" in delete_resp.json()["message"].lower()

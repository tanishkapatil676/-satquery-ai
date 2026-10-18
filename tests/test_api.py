from fastapi.testclient import TestClient
from satquery.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "satquery-ai-backend"


def test_spatial_query_endpoint_missing_file():
    payload = {
        "query": "Analyze vegetation health",
        "raster_path": "non_existent_raster.tif"
    }

    response = client.post("/api/v1/query", json=payload)
    assert response.status_code == 404

import pytest
from fastapi.testclient import TestClient
from io import BytesIO

def test_analyze_endpoint_json(client):
    json_content = b'{"services": [{"name": "test", "public": true, "authentication": false}]}'
    
    response = client.post(
        "/analyze",
        files={"file": ("test.json", BytesIO(json_content), "application/json")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "status" in data

def test_analyze_endpoint_markdown(client):
    md_content = """# Test
## Services
| Name | Public | Authentication |
|------|--------|----------------|
| web-server | Yes | No |
""".encode('utf-8')
    
    response = client.post(
        "/analyze",
        files={"file": ("test.md", BytesIO(md_content), "text/markdown")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data

def test_analyze_endpoint_no_file(client):
    response = client.post("/analyze")
    
    assert response.status_code == 422  # Validation error

def test_status_endpoint(client):
    response = client.get("/status/test-job-id")
    
    assert response.status_code == 200
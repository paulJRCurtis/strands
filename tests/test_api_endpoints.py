import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from src.coordinator.main import app

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
    assert "findings" in data
    assert "report" in data

def test_analyze_endpoint_markdown(client):
    md_content = """# Test Architecture
## Services
| Name | Public | Authentication | Port |
|------|--------|----------------|----- |
| web-server | Yes | No | 80 |

## Firewall Rules
| Source | Port | Protocol |
|--------|------|---------|
| 0.0.0.0/0 | 80 | HTTP |
""".encode('utf-8')
    
    response = client.post(
        "/analyze",
        files={"file": ("test.md", BytesIO(md_content), "text/markdown")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert "findings" in data
    assert len(data["findings"]) > 0  # Should detect security issues

def test_analyze_secure_architecture(client):
    secure_content = """# Secure Architecture
## Services
| Name | Public | Authentication | Port |
|------|--------|----------------|----- |
| web-server | Yes | Yes | 443 |

## Firewall Rules
| Source | Port | Protocol |
|--------|------|---------|
| 10.0.0.0/8 | 443 | HTTPS |

## Data Flows
| Source | Destination | Encrypted |
|--------|-------------|----------|
| web-server | database | Yes |

## Databases
| Name | Data Types | Encrypted at Rest |
|------|------------|------------------|
| user-db | user-data | Yes |
""".encode('utf-8')
    
    response = client.post(
        "/analyze",
        files={"file": ("secure.md", BytesIO(secure_content), "text/markdown")}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Secure architecture should have fewer findings
    assert data["report"]["risk_score"] < 50

def test_analyze_endpoint_no_file(client):
    response = client.post("/analyze")
    assert response.status_code == 422

def test_status_endpoint(client):
    response = client.get("/status/test-job-id")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
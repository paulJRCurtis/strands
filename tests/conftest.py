import pytest
from fastapi.testclient import TestClient
from src.coordinator.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_json_file():
    return {
        "services": [{"name": "web-server", "public": True, "authentication": False}],
        "databases": [{"name": "user-db", "data_types": ["pii"], "encrypted_at_rest": False}]
    }

@pytest.fixture
def sample_markdown_content():
    return """# Test Architecture
## Services
| Name | Public | Authentication |
|------|--------|----------------|
| web-server | Yes | No |
"""
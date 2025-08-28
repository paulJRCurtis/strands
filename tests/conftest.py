import pytest
from fastapi.testclient import TestClient
from src.coordinator.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def vulnerable_architecture():
    return {
        "services": [{"name": "web-server", "public": True, "authentication": False, "port": 80}],
        "firewall_rules": [{"source": "0.0.0.0/0", "port": 80, "protocol": "HTTP"}],
        "databases": [{"name": "user-db", "data_types": ["pii", "credentials"], "encrypted_at_rest": False}],
        "data_flows": [{"source": "web-server", "destination": "database", "encrypted": False}],
        "iam_policies": [{"name": "admin-policy", "actions": ["*"], "resources": ["*"]}],
        "storage": [{"name": "public-bucket", "public_read": True, "encryption": False}]
    }

@pytest.fixture
def secure_architecture():
    return {
        "services": [{"name": "web-server", "public": True, "authentication": True, "port": 443}],
        "firewall_rules": [{"source": "10.0.0.0/8", "port": 443, "protocol": "HTTPS"}],
        "databases": [{"name": "user-db", "data_types": ["user-data"], "encrypted_at_rest": True}],
        "data_flows": [{"source": "web-server", "destination": "database", "encrypted": True}],
        "iam_policies": [{"name": "web-policy", "actions": ["s3:GetObject"], "resources": ["arn:aws:s3:::web-assets/*"]}],
        "storage": [{"name": "private-bucket", "public_read": False, "encryption": True}]
    }

@pytest.fixture
def sample_markdown_content():
    return """# Test Architecture
## Services
| Name | Public | Authentication | Port |
|------|--------|----------------|----- |
| web-server | Yes | No | 80 |

## Firewall Rules
| Source | Port | Protocol |
|--------|------|---------|
| 0.0.0.0/0 | 80 | HTTP |
"""
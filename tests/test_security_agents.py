import pytest
from src.agents.network_agent import NetworkSecurityAgent
from src.agents.data_flow_agent import DataFlowAgent
from src.agents.infrastructure_agent import InfrastructureAgent
from src.agents.code_agent import CodeSecurityAgent

@pytest.fixture
def network_agent():
    return NetworkSecurityAgent()

@pytest.fixture
def data_agent():
    return DataFlowAgent()

@pytest.fixture
def infra_agent():
    return InfrastructureAgent()

@pytest.fixture
def code_agent():
    return CodeSecurityAgent()

@pytest.mark.asyncio
async def test_network_security_analysis(network_agent):
    data = {
        "services": [{"name": "web-server", "public": True, "authentication": False, "port": 80}],
        "firewall_rules": [{"source": "0.0.0.0/0", "port": 22, "protocol": "SSH"}]
    }
    
    result = await network_agent.analyze(data)
    
    assert len(result) > 0
    assert any("authentication" in finding["description"].lower() for finding in result)
    assert any(finding["severity"] in ["HIGH", "MEDIUM", "LOW", "CRITICAL"] for finding in result)

@pytest.mark.asyncio
async def test_data_protection_analysis(data_agent):
    data = {
        "databases": [{"name": "user-db", "data_types": ["pii", "credentials"], "encrypted_at_rest": False}],
        "data_flows": [{"source": "web-server", "destination": "database", "encrypted": False}]
    }
    
    result = await data_agent.analyze(data)
    
    assert len(result) > 0
    assert any("encrypted" in finding["description"].lower() for finding in result)
    assert any(finding["severity"] == "CRITICAL" for finding in result)  # PII without encryption

@pytest.mark.asyncio
async def test_infrastructure_security_analysis(infra_agent):
    data = {
        "iam_policies": [{"name": "admin-policy", "actions": ["*"], "resources": ["*"]}],
        "storage": [{"name": "public-bucket", "public_read": True, "encryption": False}]
    }
    
    result = await infra_agent.analyze(data)
    
    assert len(result) > 0
    assert any("wildcard" in finding["description"].lower() for finding in result)
    assert any("public read" in finding["description"].lower() for finding in result)

@pytest.mark.asyncio
async def test_code_security_analysis(code_agent):
    data = {
        "code_files": [{"name": "config.py", "content": "password = 'secret123'"}],
        "authentication": {"multi_factor": False}
    }
    
    result = await code_agent.analyze(data)
    
    assert len(result) > 0
    assert any("credentials" in finding["description"].lower() for finding in result)

@pytest.mark.asyncio
async def test_secure_configuration(network_agent, data_agent, infra_agent):
    secure_data = {
        "services": [{"name": "web-server", "public": True, "authentication": True, "port": 443}],
        "firewall_rules": [{"source": "10.0.0.0/8", "port": 443, "protocol": "HTTPS"}],
        "databases": [{"name": "user-db", "data_types": ["user-data"], "encrypted_at_rest": True}],
        "data_flows": [{"source": "web-server", "destination": "database", "encrypted": True}],
        "iam_policies": [{"name": "web-policy", "actions": ["s3:GetObject"], "resources": ["arn:aws:s3:::web-assets/*"]}],
        "storage": [{"name": "private-bucket", "public_read": False, "encryption": True}]
    }
    
    network_result = await network_agent.analyze(secure_data)
    data_result = await data_agent.analyze(secure_data)
    infra_result = await infra_agent.analyze(secure_data)
    
    # Secure configuration should have minimal findings
    assert len(network_result) == 0
    assert len(data_result) == 0
    assert len(infra_result) == 0

@pytest.mark.asyncio
async def test_empty_data_analysis(network_agent):
    result = await network_agent.analyze({})
    
    assert isinstance(result, list)
    assert len(result) == 0
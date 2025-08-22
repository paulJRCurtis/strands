import pytest
from src.agents.network_agent import NetworkSecurityAgent
from src.agents.data_flow_agent import DataFlowAgent

@pytest.fixture
def network_agent():
    return NetworkSecurityAgent()

@pytest.fixture
def data_agent():
    return DataFlowAgent()

@pytest.mark.asyncio
async def test_network_security_analysis(network_agent):
    data = {
        "services": [{"name": "web-server", "public": True, "authentication": False}],
        "firewall_rules": [{"source": "0.0.0.0/0", "port": 22}]
    }
    
    result = await network_agent.analyze(data)
    
    assert len(result) > 0
    assert any("authentication" in finding["description"].lower() for finding in result)

@pytest.mark.asyncio
async def test_data_protection_analysis(data_agent):
    data = {
        "databases": [{"name": "user-db", "data_types": ["pii"], "encrypted_at_rest": False}],
        "data_flows": [{"source": "web", "destination": "db", "encrypted": False}]
    }
    
    result = await data_agent.analyze(data)
    
    assert len(result) > 0
    assert any("encrypted" in finding["description"].lower() for finding in result)

@pytest.mark.asyncio
async def test_empty_data_analysis(network_agent):
    result = await network_agent.analyze({})
    
    assert isinstance(result, list)
    assert len(result) == 0
import pytest
from unittest.mock import AsyncMock
from src.coordinator.coordinator import CoordinatorAgent

@pytest.fixture
def coordinator():
    return CoordinatorAgent()

@pytest.mark.asyncio
async def test_parse_json_file(coordinator):
    mock_file = AsyncMock()
    mock_file.filename = "test.json"
    mock_file.read.return_value = b'{"services": [{"name": "test", "public": true, "authentication": false}]}'
    
    result = await coordinator.parse_file(mock_file)
    
    assert "services" in result
    assert result["services"][0]["name"] == "test"
    assert result["services"][0]["public"] is True

@pytest.mark.asyncio
async def test_parse_markdown_file(coordinator):
    mock_file = AsyncMock()
    mock_file.filename = "test.md"
    mock_file.read.return_value = """# Test Architecture

## Services

| Name | Public | Authentication | Port |
|------|--------|----------------|----- |
| web-server | Yes | No | 80 |

## Firewall Rules

| Source | Port | Protocol |
|--------|------|---------|
| 0.0.0.0/0 | 22 | SSH |
""".encode('utf-8')
    
    result = await coordinator.parse_file(mock_file)
    
    assert "services" in result
    assert "firewall_rules" in result
    assert result["services"][0]["name"] == "web-server"
    assert result["services"][0]["public"] is True
    assert result["firewall_rules"][0]["source"] == "0.0.0.0/0"

@pytest.mark.asyncio
async def test_parse_complex_markdown(coordinator):
    mock_file = AsyncMock()
    mock_file.filename = "complex.md"
    mock_file.read.return_value = """# Complex Architecture

## Data Flows

| Source | Destination | Encrypted |
|--------|-------------|----------|
| web-server | database | No |

## Databases

| Name | Data Types | Encrypted at Rest |
|------|------------|------------------|
| user-db | pii, credentials | No |

## IAM Policies

| Name | Actions | Resources |
|------|---------|----------|
| admin-policy | * | * |
""".encode('utf-8')
    
    result = await coordinator.parse_file(mock_file)
    
    assert "data_flows" in result
    assert "databases" in result
    assert "iam_policies" in result
    assert result["databases"][0]["encrypted_at_rest"] is False
    assert "*" in result["iam_policies"][0]["actions"]

@pytest.mark.asyncio
async def test_parse_invalid_json(coordinator):
    mock_file = AsyncMock()
    mock_file.filename = "test.json"
    mock_file.read.return_value = b'{"invalid": json}'
    
    result = await coordinator.parse_file(mock_file)
    
    assert "raw_content" in result  # Falls back to text parsing
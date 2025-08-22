import pytest
from unittest.mock import AsyncMock
from src.agents.parser_agent import ArchitectureParserAgent

@pytest.fixture
def parser_agent():
    return ArchitectureParserAgent()

@pytest.mark.asyncio
async def test_parse_json_file(parser_agent):
    mock_file = AsyncMock()
    mock_file.filename = "test.json"
    mock_file.read.return_value = b'{"services": [{"name": "test"}]}'
    
    result = await parser_agent.parse(mock_file)
    
    assert "services" in result
    assert result["services"][0]["name"] == "test"

@pytest.mark.asyncio
async def test_parse_markdown_file(parser_agent):
    mock_file = AsyncMock()
    mock_file.filename = "test.md"
    mock_file.read.return_value = """# Test

## Services

| Name | Public |
|------|--------|
| web-server | Yes |
""".encode('utf-8')
    
    result = await parser_agent.parse(mock_file)
    
    assert "services" in result
    assert result["services"][0]["name"] == "web-server"
    assert result["services"][0]["public"] is True

@pytest.mark.asyncio
async def test_parse_invalid_json(parser_agent):
    mock_file = AsyncMock()
    mock_file.filename = "test.json"
    mock_file.read.return_value = b'{"invalid": json}'
    
    result = await parser_agent.parse(mock_file)
    
    assert "error" in result
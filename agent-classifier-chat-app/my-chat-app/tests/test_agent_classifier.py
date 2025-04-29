import pytest
from src.chat_app.agent_classifier import load_agent, orchestrator
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_load_agent():
    mock_client = AsyncMock()
    agent_id = "test-agent-id"
    mock_client.agents.get_agent.return_value = {"agent_id": agent_id, "agent-name": "Test Agent"}
    
    with patch('src.chat_app.agent_classifier.client', mock_client):
        agent = await load_agent(agent_id)
        assert agent.definition['agent_id'] == agent_id
        assert agent.definition['agent-name'] == "Test Agent"

@pytest.mark.asyncio
async def test_orchestrator_with_specific_agent():
    mock_client = AsyncMock()
    mock_client.agents.get_agent.return_value = {"agent_id": "specific-agent-id", "agent-name": "Specific Agent"}
    
    input_text = "I want to talk to @specific-agent"
    manifest_path = "./agents/agents-manifest.json"
    
    with patch('src.chat_app.agent_classifier.client', mock_client):
        agent_id = await orchestrator(None, manifest_path, input_text)
        assert agent_id == "specific-agent-id"

@pytest.mark.asyncio
async def test_orchestrator_with_generic_agent():
    mock_client = AsyncMock()
    mock_client.agents.get_agent.return_value = {"agent_id": "generic-agent-id", "agent-name": "Generic Agent"}
    
    input_text = "Tell me something."
    manifest_path = "./agents/agents-manifest.json"
    
    with patch('src.chat_app.agent_classifier.client', mock_client):
        agent_id = await orchestrator(None, manifest_path, input_text)
        assert agent_id == "generic-agent-id"  # Assuming this is the fallback agent ID in the test setup.
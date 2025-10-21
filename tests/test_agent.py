"""
Simple tests for the financial agent.
"""

import pytest
from unittest.mock import patch, MagicMock
from finlit_agent.agent import create_financial_agent, BASE_SYSTEM_PROMPT


def test_base_system_prompt_exists():
    """Test that BASE_SYSTEM_PROMPT is defined."""
    assert BASE_SYSTEM_PROMPT is not None
    assert isinstance(BASE_SYSTEM_PROMPT, str)
    assert len(BASE_SYSTEM_PROMPT) > 0


def test_base_system_prompt_in_greek():
    """Test that system prompt contains Greek text."""
    # Check for Greek characters
    greek_chars = ['Ε', 'ο', 'ι', 'α', 'β', 'η', 'τ']
    assert any(char in BASE_SYSTEM_PROMPT for char in greek_chars)


def test_base_system_prompt_mentions_financial_topics():
    """Test that system prompt mentions key financial topics."""
    # Check for financial keywords (in Greek)
    keywords = ['οικονομικ', 'προϋπολογισμ', 'αποταμίευση', 'επένδυση']
    prompt_lower = BASE_SYSTEM_PROMPT.lower()
    
    assert any(keyword in prompt_lower for keyword in keywords)


@patch.dict('os.environ', {}, clear=True)
def test_create_agent_without_api_key():
    """Test that creating agent without API key raises error."""
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        create_financial_agent()


@patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-api-key-123'})
@patch('finlit_agent.agent.ChatGoogleGenerativeAI')
def test_create_agent_with_api_key(mock_chat_class):
    """Test that agent is created with API key."""
    mock_llm = MagicMock()
    mock_chat_class.return_value = mock_llm
    
    agent = create_financial_agent()
    
    assert agent is not None
    mock_chat_class.assert_called_once()


@patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-api-key-123'})
@patch('finlit_agent.agent.ChatGoogleGenerativeAI')
def test_create_agent_uses_correct_model(mock_chat_class):
    """Test that agent uses Gemini 2.0 Flash model."""
    mock_llm = MagicMock()
    mock_chat_class.return_value = mock_llm
    
    create_financial_agent()
    
    # Check that the model parameter was passed
    call_kwargs = mock_chat_class.call_args[1]
    assert 'model' in call_kwargs
    assert 'gemini-2.0' in call_kwargs['model']


@patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-api-key-123'})
@patch('finlit_agent.agent.ChatGoogleGenerativeAI')
def test_create_agent_sets_temperature(mock_chat_class):
    """Test that agent has temperature set."""
    mock_llm = MagicMock()
    mock_chat_class.return_value = mock_llm
    
    create_financial_agent()
    
    call_kwargs = mock_chat_class.call_args[1]
    assert 'temperature' in call_kwargs
    assert 0 <= call_kwargs['temperature'] <= 1


@patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-api-key-123'})
@patch('finlit_agent.agent.ChatGoogleGenerativeAI')
def test_create_agent_passes_api_key(mock_chat_class):
    """Test that API key is passed to the model."""
    mock_llm = MagicMock()
    mock_chat_class.return_value = mock_llm
    
    create_financial_agent()
    
    call_kwargs = mock_chat_class.call_args[1]
    assert 'google_api_key' in call_kwargs
    assert call_kwargs['google_api_key'] == 'test-api-key-123'


@patch.dict('os.environ', {'GOOGLE_API_KEY': ''})
def test_create_agent_with_empty_api_key():
    """Test that empty API key is treated as missing."""
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        create_financial_agent()


@patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'})
@patch('finlit_agent.agent.ChatGoogleGenerativeAI')
def test_create_agent_returns_chat_instance(mock_chat_class):
    """Test that create_financial_agent returns the LLM instance."""
    mock_llm = MagicMock()
    mock_chat_class.return_value = mock_llm
    
    agent = create_financial_agent()
    
    assert agent == mock_llm


def test_system_prompt_mentions_greek_context():
    """Test that prompt mentions Greek household context."""
    prompt_lower = BASE_SYSTEM_PROMPT.lower()
    
    # Should mention Greek or household context
    context_keywords = ['ελληνικ', 'νοικοκυρι']
    assert any(keyword in prompt_lower for keyword in context_keywords)


def test_system_prompt_gives_clear_instructions():
    """Test that prompt contains clear behavioral instructions."""
    # Should have instructions about how to respond
    assert 'Παρέχεις' in BASE_SYSTEM_PROMPT or 'παρέχεις' in BASE_SYSTEM_PROMPT.lower()
    assert 'Απαντάς' in BASE_SYSTEM_PROMPT or 'απαντάς' in BASE_SYSTEM_PROMPT.lower()

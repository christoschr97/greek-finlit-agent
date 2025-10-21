"""
Simple tests for chat UI components.
"""

from unittest.mock import MagicMock, patch, call
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from finlit_agent.ui.chat_ui import render_chat, _display_chat_history, _handle_chat_input


@patch('finlit_agent.ui.chat_ui.st')
def test_render_chat_calls_display_and_input(mock_st):
    """Test that render_chat calls both display and input handlers."""
    mock_st.session_state = {
        'messages': [],
        'agent': MagicMock()
    }
    
    with patch('finlit_agent.ui.chat_ui._display_chat_history') as mock_display:
        with patch('finlit_agent.ui.chat_ui._handle_chat_input') as mock_input:
            render_chat()
            
            mock_display.assert_called_once()
            mock_input.assert_called_once()


@patch('finlit_agent.ui.chat_ui.st')
def test_display_chat_history_with_messages(mock_st):
    """Test displaying chat history with different message types."""
    mock_st.session_state = {
        'messages': [
            SystemMessage(content="System message"),
            HumanMessage(content="User message"),
            AIMessage(content="AI message")
        ]
    }
    mock_st.chat_message = MagicMock()
    
    _display_chat_history()
    
    # System message should not be displayed, only Human and AI
    assert mock_st.chat_message.call_count == 2


@patch('finlit_agent.ui.chat_ui.st')
def test_display_chat_history_empty(mock_st):
    """Test displaying empty chat history."""
    mock_st.session_state = {'messages': []}
    mock_st.chat_message = MagicMock()
    
    _display_chat_history()
    
    # No messages to display
    mock_st.chat_message.assert_not_called()


@patch('finlit_agent.ui.chat_ui.st')
def test_handle_chat_input_no_input(mock_st):
    """Test handling chat input when no input is provided."""
    mock_st.chat_input = MagicMock(return_value=None)
    mock_st.session_state = {'messages': [], 'agent': MagicMock()}
    
    _handle_chat_input()
    
    # Should not process any message
    assert len(mock_st.session_state['messages']) == 0


@patch('finlit_agent.ui.chat_ui.st')
@patch('finlit_agent.ui.chat_ui._process_user_message')
def test_handle_chat_input_with_prompt(mock_process, mock_st):
    """Test handling chat input with user prompt."""
    mock_st.chat_input = MagicMock(return_value="Test prompt")
    
    _handle_chat_input()
    
    mock_process.assert_called_once_with("Test prompt")

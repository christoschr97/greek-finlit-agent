"""
Simple tests for session state management.
"""

from unittest.mock import MagicMock, patch
from finlit_agent.ui.session_state import initialize_session_state, get_state, set_state


@patch('finlit_agent.ui.session_state.st')
def test_initialize_session_state(mock_st):
    """Test that session state is initialized correctly."""
    mock_st.session_state = {}
    
    initialize_session_state()
    
    # Check that all required keys are initialized
    assert 'assessment_done' in mock_st.session_state
    assert 'current_question' in mock_st.session_state
    assert 'assessment' in mock_st.session_state
    assert 'messages' in mock_st.session_state
    assert 'agent' in mock_st.session_state


@patch('finlit_agent.ui.session_state.st')
def test_initialize_session_state_default_values(mock_st):
    """Test that session state has correct default values."""
    mock_st.session_state = {}
    
    initialize_session_state()
    
    assert mock_st.session_state['assessment_done'] is False
    assert mock_st.session_state['current_question'] == 0
    assert mock_st.session_state['messages'] == []
    assert mock_st.session_state['agent'] is None


@patch('finlit_agent.ui.session_state.st')
def test_get_state(mock_st):
    """Test getting a value from session state."""
    mock_st.session_state = {'test_key': 'test_value'}
    
    result = get_state('test_key')
    
    assert result == 'test_value'


@patch('finlit_agent.ui.session_state.st')
def test_set_state(mock_st):
    """Test setting a value in session state."""
    mock_st.session_state = {}
    
    set_state('test_key', 'test_value')
    
    assert mock_st.session_state['test_key'] == 'test_value'


@patch('finlit_agent.ui.session_state.st')
def test_initialize_only_once(mock_st):
    """Test that session state is not reinitialized if already set."""
    mock_st.session_state = {'assessment_done': True}
    
    initialize_session_state()
    
    # Should still be True, not reset to False
    assert mock_st.session_state['assessment_done'] is True

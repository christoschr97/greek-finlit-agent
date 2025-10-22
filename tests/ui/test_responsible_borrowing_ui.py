"""
Tests for responsible borrowing UI components.
"""

from unittest.mock import MagicMock, patch
from finlit_agent.ui.responsible_borrowing_ui import render_responsible_borrowing


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_displays_title(mock_st):
    """Test that responsible borrowing renders title."""
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.info = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should display title
    assert mock_st.markdown.called


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_displays_description(mock_st):
    """Test that responsible borrowing displays description."""
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.info = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should display description
    assert mock_st.write.called


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_displays_under_development(mock_st):
    """Test that responsible borrowing shows under development message."""
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.info = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should display info message
    mock_st.info.assert_called_once()


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_back_button(mock_st):
    """Test that back button is rendered."""
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.info = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should render back button
    mock_st.button.assert_called_once()


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_back_button_click(mock_st):
    """Test clicking back button resets path selection."""
    mock_st.session_state = {
        'path_selected': True,
        'selected_path': 'responsible_borrowing'
    }
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.info = MagicMock()
    mock_st.button = MagicMock(return_value=True)  # Button clicked
    mock_st.rerun = MagicMock()
    
    render_responsible_borrowing()
    
    # Should reset path selection state
    assert mock_st.session_state['path_selected'] is False
    assert mock_st.session_state['selected_path'] is None
    # Should trigger rerun
    mock_st.rerun.assert_called_once()


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_back_button_no_click(mock_st):
    """Test that not clicking back button preserves state."""
    original_state = {
        'path_selected': True,
        'selected_path': 'responsible_borrowing'
    }
    mock_st.session_state = original_state.copy()
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.info = MagicMock()
    mock_st.button = MagicMock(return_value=False)  # Button not clicked
    mock_st.rerun = MagicMock()
    
    render_responsible_borrowing()
    
    # State should remain unchanged
    assert mock_st.session_state['path_selected'] is True
    assert mock_st.session_state['selected_path'] == 'responsible_borrowing'
    # Should not trigger rerun
    mock_st.rerun.assert_not_called()


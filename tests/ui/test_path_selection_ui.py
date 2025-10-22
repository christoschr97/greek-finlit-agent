"""
Tests for path selection UI components.
"""

from unittest.mock import MagicMock, patch
from finlit_agent.ui.path_selection_ui import render_path_selection


@patch('finlit_agent.ui.path_selection_ui.st')
def test_render_path_selection_displays_title(mock_st):
    """Test that path selection renders title."""
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
    mock_st.button = MagicMock(return_value=False)
    
    render_path_selection()
    
    # Should call markdown for title
    assert mock_st.markdown.called
    # Should call write for description
    assert mock_st.write.called


@patch('finlit_agent.ui.path_selection_ui.st')
def test_render_path_selection_displays_two_buttons(mock_st):
    """Test that path selection renders two path buttons."""
    col1 = MagicMock()
    col2 = MagicMock()
    col1.__enter__ = MagicMock(return_value=col1)
    col1.__exit__ = MagicMock(return_value=False)
    col2.__enter__ = MagicMock(return_value=col2)
    col2.__exit__ = MagicMock(return_value=False)
    
    mock_st.columns = MagicMock(return_value=[col1, col2])
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    
    render_path_selection()
    
    # Should create two columns
    mock_st.columns.assert_called_once_with(2)
    # Should call button twice (once in each column context)
    assert mock_st.button.call_count == 2


@patch('finlit_agent.ui.path_selection_ui.st')
def test_path_selection_general_chat_button_click(mock_st):
    """Test clicking general chat button sets session state."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.rerun = MagicMock()
    
    col1 = MagicMock()
    col2 = MagicMock()
    col1.__enter__ = MagicMock(return_value=col1)
    col1.__exit__ = MagicMock(return_value=False)
    col2.__enter__ = MagicMock(return_value=col2)
    col2.__exit__ = MagicMock(return_value=False)
    
    mock_st.columns = MagicMock(return_value=[col1, col2])
    
    # Simulate general chat button clicked (first call), second button not clicked
    mock_st.button = MagicMock(side_effect=[True, False])
    
    render_path_selection()
    
    # Should set session state
    assert mock_st.session_state['selected_path'] == 'general_chat'
    assert mock_st.session_state['path_selected'] is True
    # Should trigger rerun
    mock_st.rerun.assert_called_once()


@patch('finlit_agent.ui.path_selection_ui.st')
def test_path_selection_responsible_borrowing_button_click(mock_st):
    """Test clicking responsible borrowing button sets session state."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.rerun = MagicMock()
    
    col1 = MagicMock()
    col2 = MagicMock()
    col1.__enter__ = MagicMock(return_value=col1)
    col1.__exit__ = MagicMock(return_value=False)
    col2.__enter__ = MagicMock(return_value=col2)
    col2.__exit__ = MagicMock(return_value=False)
    
    mock_st.columns = MagicMock(return_value=[col1, col2])
    
    # Simulate first button not clicked, second button clicked
    mock_st.button = MagicMock(side_effect=[False, True])
    
    render_path_selection()
    
    # Should set session state
    assert mock_st.session_state['selected_path'] == 'responsible_borrowing'
    assert mock_st.session_state['path_selected'] is True
    # Should trigger rerun
    mock_st.rerun.assert_called_once()


@patch('finlit_agent.ui.path_selection_ui.st')
def test_path_selection_no_button_click(mock_st):
    """Test that no button click doesn't set session state."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.rerun = MagicMock()
    
    col1 = MagicMock()
    col2 = MagicMock()
    col1.__enter__ = MagicMock(return_value=col1)
    col1.__exit__ = MagicMock(return_value=False)
    col2.__enter__ = MagicMock(return_value=col2)
    col2.__exit__ = MagicMock(return_value=False)
    
    mock_st.columns = MagicMock(return_value=[col1, col2])
    
    # No button clicked
    mock_st.button = MagicMock(return_value=False)
    
    render_path_selection()
    
    # Session state should remain empty
    assert 'selected_path' not in mock_st.session_state
    assert 'path_selected' not in mock_st.session_state
    # Should not trigger rerun
    mock_st.rerun.assert_not_called()


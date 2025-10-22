"""
Tests for responsible borrowing UI components - Simplified version.
"""

from unittest.mock import MagicMock, patch
from finlit_agent.ui.responsible_borrowing_ui import render_responsible_borrowing


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_displays_title(mock_st):
    """Test that responsible borrowing renders title."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.text_area = MagicMock(return_value="")
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should display title
    assert mock_st.markdown.called


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_asks_for_input_initially(mock_st):
    """Test that it shows input screen when no classification exists."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.text_area = MagicMock(return_value="")
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should show text area for input
    assert mock_st.text_area.called


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_shows_explanation_after_classification(mock_st):
    """Test that it shows explanation when classification exists."""
    mock_st.session_state = {
        "rb_loan_type": "mortgage",
        "rb_confidence": 0.95,
        "rb_reasoning": "User wants to buy a house"
    }
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.success = MagicMock()
    mock_st.caption = MagicMock()
    mock_st.info = MagicMock()
    mock_st.expander = MagicMock()
    mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should show success message
    assert mock_st.success.called


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_back_button(mock_st):
    """Test that back button is rendered."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.text_area = MagicMock(return_value="")
    mock_st.button = MagicMock(return_value=False)
    
    render_responsible_borrowing()
    
    # Should render back button (called at least once)
    assert mock_st.button.called


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
def test_render_responsible_borrowing_back_button_click(mock_st):
    """Test clicking back button resets state."""
    mock_st.session_state = {
        "rb_loan_type": "mortgage",
        "rb_confidence": 0.95,
        "rb_financial_data": {
            "monthly_income": 1000,
            "other_income": 0,
            "monthly_expenses": 600,
            "existing_loans": 0,
            "savings": 5000,
            "loan_amount": 10000
        },
        "path_selected": True,
        "selected_path": "responsible_borrowing"
    }
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.success = MagicMock()
    mock_st.caption = MagicMock()
    mock_st.info = MagicMock()
    mock_st.warning = MagicMock()
    mock_st.expander = MagicMock()
    # Mock columns to return 2 or 3 columns depending on call
    mock_st.columns = MagicMock(side_effect=[
        [MagicMock(), MagicMock()],  # First call (2 columns for terms)
        [MagicMock(), MagicMock(), MagicMock()],  # Second call (3 columns for metrics)
        [MagicMock(), MagicMock()]  # Third call (2 columns for analysis)
    ])
    mock_st.metric = MagicMock()
    mock_st.error = MagicMock()
    # Multiple buttons: reset button in explanation, edit button in summary, back button at bottom
    mock_st.button = MagicMock(side_effect=[False, False, True])  # Reset + Edit + Back
    mock_st.rerun = MagicMock()
    
    render_responsible_borrowing()
    
    # Should reset path selection state
    assert mock_st.session_state['path_selected'] is False
    assert mock_st.session_state['selected_path'] is None
    # Should trigger rerun
    mock_st.rerun.assert_called_once()


@patch('finlit_agent.ui.responsible_borrowing_ui.st')
@patch('finlit_agent.ui.responsible_borrowing_ui.create_loan_classifier_agent')
@patch('finlit_agent.ui.responsible_borrowing_ui.classify_loan_request')
def test_classification_button_triggers_analysis(mock_classify, mock_create_agent, mock_st):
    """Test that clicking analyze button triggers classification."""
    mock_st.session_state = {}
    mock_st.markdown = MagicMock()
    mock_st.write = MagicMock()
    mock_st.text_area = MagicMock(return_value="I want to buy a house")
    mock_st.button = MagicMock(side_effect=[True, False])  # Analyze button clicked
    mock_st.spinner = MagicMock()
    mock_st.rerun = MagicMock()
    
    # Mock successful classification
    mock_agent = MagicMock()
    mock_create_agent.return_value = mock_agent
    mock_classify.return_value = {
        "success": True,
        "loan_type": "mortgage",
        "confidence": 0.95,
        "reasoning": "User wants mortgage",
        "next_question": None,
        "error": None
    }
    
    render_responsible_borrowing()
    
    # Should have called classifier
    assert mock_create_agent.called
    assert mock_classify.called
    # Should save results to session state
    assert mock_st.session_state["rb_loan_type"] == "mortgage"

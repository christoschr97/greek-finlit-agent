"""
Simple tests for assessment UI components.
"""

from unittest.mock import MagicMock, patch
from finlit_agent.ui.assessment_ui import render_assessment, _render_question, _render_results


@patch('finlit_agent.ui.assessment_ui.st')
def test_render_assessment_with_questions_remaining(mock_st):
    """Test rendering assessment when questions remain."""
    mock_assessment = MagicMock()
    mock_assessment.QUESTIONS = [{'id': 1}, {'id': 2}, {'id': 3}]
    
    mock_st.session_state = {
        'assessment': mock_assessment,
        'current_question': 0
    }
    
    with patch('finlit_agent.ui.assessment_ui._render_question') as mock_render_q:
        render_assessment()
        mock_render_q.assert_called_once()


@patch('finlit_agent.ui.assessment_ui.st')
def test_render_assessment_when_complete(mock_st):
    """Test rendering assessment when all questions are answered."""
    mock_assessment = MagicMock()
    mock_assessment.QUESTIONS = [{'id': 1}, {'id': 2}, {'id': 3}]
    
    mock_st.session_state = {
        'assessment': mock_assessment,
        'current_question': 3  # Beyond last question
    }
    
    with patch('finlit_agent.ui.assessment_ui._render_results') as mock_render_r:
        render_assessment()
        mock_render_r.assert_called_once()


@patch('finlit_agent.ui.assessment_ui.st')
def test_render_question_displays_content(mock_st):
    """Test that _render_question displays question content."""
    questions = [{
        'id': 1,
        'question': 'Test question?',
        'options': ['A) Option 1', 'B) Option 2'],
        'correct': 'A'
    }]
    mock_assessment = MagicMock()
    
    mock_st.write = MagicMock()
    mock_st.radio = MagicMock(return_value='A')
    mock_st.button = MagicMock(return_value=False)
    
    _render_question(questions, mock_assessment, 0)
    
    # Check that question content was written
    assert mock_st.write.called


@patch('finlit_agent.ui.assessment_ui.st')
def test_render_question_button_click(mock_st):
    """Test that clicking next button records answer."""
    questions = [{
        'id': 1,
        'question': 'Test question?',
        'options': ['A) Option 1', 'B) Option 2'],
        'correct': 'A'
    }]
    mock_assessment = MagicMock()
    
    mock_st.session_state = {'current_question': 0}
    mock_st.write = MagicMock()
    mock_st.radio = MagicMock(return_value='A')
    mock_st.button = MagicMock(return_value=True)  # Button clicked
    mock_st.rerun = MagicMock()
    
    _render_question(questions, mock_assessment, 0)
    
    # Should record the answer
    mock_assessment.record_answer.assert_called_once_with(1, 'A')


@patch('finlit_agent.ui.assessment_ui.st')
def test_render_results_displays_score(mock_st):
    """Test that _render_results displays score and level."""
    mock_assessment = MagicMock()
    mock_assessment.get_level_name = MagicMock(return_value="Intermediate")
    mock_assessment.score = 2
    mock_assessment.QUESTIONS = [1, 2, 3]
    mock_assessment.answers = {}
    
    mock_st.success = MagicMock()
    mock_st.metric = MagicMock()
    mock_st.expander = MagicMock()
    mock_st.button = MagicMock(return_value=False)
    
    _render_results(mock_assessment)
    
    # Should display success message and metrics
    mock_st.success.assert_called_once()
    mock_st.metric.assert_called_once()


@patch('finlit_agent.ui.assessment_ui.st')
@patch('finlit_agent.ui.assessment_ui.create_financial_agent')
def test_render_results_start_chat(mock_create_agent, mock_st):
    """Test that clicking start chat initializes agent."""
    mock_assessment = MagicMock()
    mock_assessment.get_level_name = MagicMock(return_value="Intermediate")
    mock_assessment.get_context_summary = MagicMock(return_value="Context")
    mock_assessment.score = 2
    mock_assessment.QUESTIONS = [1, 2, 3]
    mock_assessment.answers = {}
    
    mock_agent = MagicMock()
    mock_create_agent.return_value = mock_agent
    
    mock_st.session_state = {}
    mock_st.success = MagicMock()
    mock_st.metric = MagicMock()
    mock_st.expander = MagicMock()
    mock_st.button = MagicMock(return_value=True)  # Button clicked
    mock_st.rerun = MagicMock()
    
    _render_results(mock_assessment)
    
    # Should initialize agent
    assert mock_st.session_state['agent'] == mock_agent
    assert mock_st.session_state['assessment_done'] is True

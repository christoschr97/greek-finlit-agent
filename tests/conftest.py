"""
Pytest configuration and fixtures.
"""

import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_streamlit():
    """Fixture to mock Streamlit."""
    mock_st = MagicMock()
    mock_st.session_state = {}
    return mock_st


@pytest.fixture
def mock_assessment():
    """Fixture to create a mock assessment."""
    mock = MagicMock()
    mock.QUESTIONS = [
        {
            'id': 1,
            'question': 'Test question 1?',
            'options': ['A) Option 1', 'B) Option 2'],
            'correct': 'A'
        },
        {
            'id': 2,
            'question': 'Test question 2?',
            'options': ['A) Option 1', 'B) Option 2'],
            'correct': 'B'
        },
        {
            'id': 3,
            'question': 'Test question 3?',
            'options': ['A) Option 1', 'B) Option 2'],
            'correct': 'A'
        }
    ]
    mock.score = 0
    mock.answers = {}
    mock.get_level_name = MagicMock(return_value="Beginner")
    mock.get_context_summary = MagicMock(return_value="Assessment context")
    return mock

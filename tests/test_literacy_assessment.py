"""
Simple tests for the financial literacy assessment.
"""

import pytest
from finlit_agent.literacy_assessment import (
    FinancialLiteracyAssessment,
    LiteracyLevel
)


def test_assessment_initialization():
    """Test that assessment initializes correctly."""
    assessment = FinancialLiteracyAssessment()
    
    assert assessment.score == 0
    assert assessment.answers == {}


def test_questions_exist():
    """Test that all 3 questions are defined."""
    assessment = FinancialLiteracyAssessment()
    
    assert len(assessment.QUESTIONS) == 3
    assert all('id' in q for q in assessment.QUESTIONS)
    assert all('question' in q for q in assessment.QUESTIONS)
    assert all('correct' in q for q in assessment.QUESTIONS)


def test_record_correct_answer():
    """Test recording a correct answer increases score."""
    assessment = FinancialLiteracyAssessment()
    question = assessment.QUESTIONS[0]
    
    is_correct = assessment.record_answer(question['id'], question['correct'])
    
    assert is_correct is True
    assert assessment.score == 1
    assert question['id'] in assessment.answers


def test_record_incorrect_answer():
    """Test recording an incorrect answer."""
    assessment = FinancialLiteracyAssessment()
    question = assessment.QUESTIONS[0]
    wrong_answer = 'b' if question['correct'] != 'b' else 'a'
    
    is_correct = assessment.record_answer(question['id'], wrong_answer)
    
    assert is_correct is False
    assert assessment.score == 0
    assert question['id'] in assessment.answers


def test_record_invalid_question_id():
    """Test that invalid question ID raises error."""
    assessment = FinancialLiteracyAssessment()
    
    with pytest.raises(ValueError, match="Invalid question_id"):
        assessment.record_answer(999, 'a')


def test_get_level_beginner():
    """Test that 0-1 correct answers = Beginner level."""
    assessment = FinancialLiteracyAssessment()
    assessment.score = 0
    assert assessment.get_level() == LiteracyLevel.BEGINNER
    
    assessment.score = 1
    assert assessment.get_level() == LiteracyLevel.BEGINNER


def test_get_level_intermediate():
    """Test that 2 correct answers = Intermediate level."""
    assessment = FinancialLiteracyAssessment()
    assessment.score = 2
    
    assert assessment.get_level() == LiteracyLevel.INTERMEDIATE


def test_get_level_advanced():
    """Test that 3 correct answers = Advanced level."""
    assessment = FinancialLiteracyAssessment()
    assessment.score = 3
    
    assert assessment.get_level() == LiteracyLevel.ADVANCED


def test_get_level_name():
    """Test that level names are in Greek."""
    assessment = FinancialLiteracyAssessment()
    
    assessment.score = 0
    assert assessment.get_level_name() == "Αρχάριο"
    
    assessment.score = 2
    assert assessment.get_level_name() == "Μέτριο"
    
    assessment.score = 3
    assert assessment.get_level_name() == "Προχωρημένο"


def test_get_short_summary():
    """Test that short summary includes score and level."""
    assessment = FinancialLiteracyAssessment()
    assessment.score = 2
    
    summary = assessment.get_short_summary()
    
    assert "Μέτριο" in summary
    assert "2/3" in summary


def test_get_context_summary():
    """Test that context summary is generated for LLM."""
    assessment = FinancialLiteracyAssessment()
    # Answer all questions correctly
    for q in assessment.QUESTIONS:
        assessment.record_answer(q['id'], q['correct'])
    
    summary = assessment.get_context_summary()
    
    assert "ΕΠΙΠΕΔΟ ΟΙΚΟΝΟΜΙΚΟΥ ΕΓΓΡΑΜΜΑΤΙΣΜΟΥ" in summary
    assert "Προχωρημένο" in summary
    assert "3/3" in summary
    assert "ΟΔΗΓΙΕΣ ΠΡΟΣΑΡΜΟΓΗΣ" in summary


def test_context_summary_includes_correct_instructions():
    """Test that instructions match literacy level."""
    assessment = FinancialLiteracyAssessment()
    
    # Test beginner level - need to record answers first
    assessment.record_answer(1, 'b')  # wrong
    assessment.record_answer(2, 'a')  # wrong
    assessment.record_answer(3, 'a')  # wrong
    summary = assessment.get_context_summary()
    assert "ΠΟΛΥ απλή γλώσσα" in summary
    
    # Test intermediate level
    assessment2 = FinancialLiteracyAssessment()
    assessment2.record_answer(1, assessment2.QUESTIONS[0]['correct'])  # correct
    assessment2.record_answer(2, assessment2.QUESTIONS[1]['correct'])  # correct
    assessment2.record_answer(3, 'a')  # wrong
    summary2 = assessment2.get_context_summary()
    assert "απλή γλώσσα" in summary2
    
    # Test advanced level
    assessment3 = FinancialLiteracyAssessment()
    for q in assessment3.QUESTIONS:
        assessment3.record_answer(q['id'], q['correct'])
    summary3 = assessment3.get_context_summary()
    assert "οικονομικούς όρους" in summary3


def test_all_questions_have_required_fields():
    """Test that all questions have proper structure."""
    assessment = FinancialLiteracyAssessment()
    
    required_fields = ['id', 'dimension', 'question', 'options', 'correct', 'explanation']
    
    for q in assessment.QUESTIONS:
        for field in required_fields:
            assert field in q, f"Question {q.get('id')} missing {field}"
        
        assert isinstance(q['options'], list)
        assert len(q['options']) >= 2
        assert q['correct'] in ['a', 'b', 'c', 'd']


def test_dimensions_are_unique():
    """Test that each question tests a different dimension."""
    assessment = FinancialLiteracyAssessment()
    
    dimensions = [q['dimension'] for q in assessment.QUESTIONS]
    assert len(dimensions) == len(set(dimensions)), "Dimensions should be unique"


def test_answer_storage_structure():
    """Test that answers are stored with correct structure."""
    assessment = FinancialLiteracyAssessment()
    question = assessment.QUESTIONS[0]
    
    assessment.record_answer(question['id'], 'a')
    answer_data = assessment.answers[question['id']]
    
    assert 'question' in answer_data
    assert 'user_answer' in answer_data
    assert 'correct_answer' in answer_data
    assert 'is_correct' in answer_data
    assert 'explanation' in answer_data
    assert isinstance(answer_data['is_correct'], bool)


def test_multiple_answers():
    """Test recording multiple answers updates score correctly."""
    assessment = FinancialLiteracyAssessment()
    
    # Answer first question correctly
    assessment.record_answer(1, assessment.QUESTIONS[0]['correct'])
    assert assessment.score == 1
    
    # Answer second question incorrectly
    wrong_answer = 'b' if assessment.QUESTIONS[1]['correct'] != 'b' else 'a'
    assessment.record_answer(2, wrong_answer)
    assert assessment.score == 1  # Score should not increase
    
    # Answer third question correctly
    assessment.record_answer(3, assessment.QUESTIONS[2]['correct'])
    assert assessment.score == 2


def test_level_names_constant():
    """Test that LEVEL_NAMES constant is properly defined."""
    names = FinancialLiteracyAssessment.LEVEL_NAMES
    
    assert LiteracyLevel.BEGINNER in names
    assert LiteracyLevel.INTERMEDIATE in names
    assert LiteracyLevel.ADVANCED in names
    assert all(isinstance(name, str) for name in names.values())


def test_dimension_names_constant():
    """Test that DIMENSION_NAMES constant is properly defined."""
    dimensions = FinancialLiteracyAssessment.DIMENSION_NAMES
    
    assert 'compound_interest' in dimensions
    assert 'inflation' in dimensions
    assert 'risk_diversification' in dimensions
    assert all(isinstance(name, str) for name in dimensions.values())

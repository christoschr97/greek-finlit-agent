"""
Assessment UI components for the Streamlit app.
"""

from typing import Dict, List, Any
import streamlit as st
from langchain_core.messages import SystemMessage
from finlit_agent.agent import create_financial_agent, BASE_SYSTEM_PROMPT
from finlit_agent.literacy_assessment import FinancialLiteracyAssessment
from .config import (
    ASSESSMENT_TITLE,
    ASSESSMENT_COMPLETE,
    RESULTS_EXPANDER,
    START_CHAT_BUTTON,
    NEXT_BUTTON,
    QUESTION_PROMPT,
    LEVEL_METRIC_LABEL,
    GENERAL_CHAT_PATH,
    RESPONSIBLE_BORROWING_PATH,
    PATH_SELECTION_TITLE,
    SESSION_ASSESSMENT_DONE,
    SESSION_CURRENT_QUESTION,
    SESSION_ASSESSMENT,
    SESSION_MESSAGES,
    SESSION_AGENT,
    SESSION_PATH_SELECTED,
    SESSION_SELECTED_PATH
)


def render_assessment() -> None:
    """Render the financial literacy assessment phase."""
    st.markdown(ASSESSMENT_TITLE)
    
    assessment: FinancialLiteracyAssessment = st.session_state[SESSION_ASSESSMENT]
    questions: List[Dict[str, Any]] = assessment.QUESTIONS
    current_question: int = st.session_state[SESSION_CURRENT_QUESTION]
    
    if current_question < len(questions):
        _render_question(questions, assessment, current_question)
    else:
        _render_results(assessment)


def _render_question(
    questions: List[Dict[str, Any]], 
    assessment: FinancialLiteracyAssessment,
    current_question: int
) -> None:
    """Render a single assessment question."""
    question = questions[current_question]
    question_number = current_question + 1
    total_questions = len(questions)
    
    st.write(f"**Ερώτηση {question_number}/{total_questions}:**")
    st.write(question['question'])
    st.write("")
    
    # Radio buttons for answer
    option_labels: List[str] = question['options']
    option_values: List[str] = [opt[0] for opt in option_labels]
    
    answer = st.radio(
        QUESTION_PROMPT,
        options=option_values,
        format_func=lambda x: next(opt for opt in option_labels if opt.startswith(x)),
        key=f"q_{current_question}"
    )
    
    if st.button(NEXT_BUTTON, type="primary"):
        assessment.record_answer(question['id'], answer)
        st.session_state[SESSION_CURRENT_QUESTION] += 1
        st.rerun()


def _render_results(assessment: FinancialLiteracyAssessment) -> None:
    """Render the assessment results and path selection buttons."""
    st.success(ASSESSMENT_COMPLETE)
    st.metric(
        LEVEL_METRIC_LABEL, 
        assessment.get_level_name(), 
        f"{assessment.score}/{len(assessment.QUESTIONS)}"
    )
    
    with st.expander(RESULTS_EXPANDER):
        for q_id, ans in assessment.answers.items():
            icon = "✅" if ans['is_correct'] else "❌"
            st.write(f"{icon} Ερώτηση {q_id}: {ans['explanation']}")

    # Show path selection directly after results
    st.markdown("---")
    st.markdown(PATH_SELECTION_TITLE)
    st.write("Επιλέξτε μία διαδρομή:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(GENERAL_CHAT_PATH, type="primary", use_container_width=True):
            st.session_state[SESSION_ASSESSMENT_DONE] = True
            st.session_state[SESSION_SELECTED_PATH] = "general_chat"
            st.session_state[SESSION_PATH_SELECTED] = True
            st.rerun()

    with col2:
        if st.button(RESPONSIBLE_BORROWING_PATH, use_container_width=True):
            st.session_state[SESSION_ASSESSMENT_DONE] = True
            st.session_state[SESSION_SELECTED_PATH] = "responsible_borrowing"
            st.session_state[SESSION_PATH_SELECTED] = True
            st.rerun()


def _initialize_chat(assessment: FinancialLiteracyAssessment) -> None:
    """Initialize the chat agent with assessment context."""
    agent = create_financial_agent()
    system_prompt = BASE_SYSTEM_PROMPT + assessment.get_context_summary()
    
    st.session_state[SESSION_AGENT] = agent
    st.session_state[SESSION_MESSAGES] = [SystemMessage(content=system_prompt)]
    
    st.session_state[SESSION_ASSESSMENT_DONE] = True
    st.rerun()

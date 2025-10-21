"""
Session state management for the Streamlit app.
"""

from typing import Any
import streamlit as st
from finlit_agent.literacy_assessment import FinancialLiteracyAssessment
from .config import (
    SESSION_ASSESSMENT_DONE,
    SESSION_CURRENT_QUESTION,
    SESSION_ASSESSMENT,
    SESSION_MESSAGES,
    SESSION_AGENT
)


def initialize_session_state() -> None:
    """Initialize all session state variables."""
    if SESSION_ASSESSMENT_DONE not in st.session_state:
        st.session_state[SESSION_ASSESSMENT_DONE] = False
        st.session_state[SESSION_CURRENT_QUESTION] = 0
        st.session_state[SESSION_ASSESSMENT] = FinancialLiteracyAssessment()
        st.session_state[SESSION_MESSAGES] = []
        st.session_state[SESSION_AGENT] = None


def get_state(key: str) -> Any:
    """Get a value from session state."""
    return st.session_state.get(key)


def set_state(key: str, value: Any) -> None:
    """Set a value in session state."""
    st.session_state[key] = value

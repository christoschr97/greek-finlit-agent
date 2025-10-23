"""
Path selection UI components for choosing between workflows.
"""

import streamlit as st
from .config import (
    PATH_SELECTION_TITLE,
    GENERAL_CHAT_PATH,
    RESPONSIBLE_BORROWING_PATH,
    SESSION_PATH_SELECTED,
    SESSION_SELECTED_PATH
)


def render_path_selection() -> None:
    """Render the path selection interface."""
    st.markdown(PATH_SELECTION_TITLE)
    
    st.write("Με βάση την αξιολόγησή σας, επιλέξτε μία διαδρομή:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(GENERAL_CHAT_PATH, type="primary"):
            st.session_state[SESSION_SELECTED_PATH] = "general_chat"
            st.session_state[SESSION_PATH_SELECTED] = True
            st.rerun()

    with col2:
        if st.button(RESPONSIBLE_BORROWING_PATH):
            st.session_state[SESSION_SELECTED_PATH] = "responsible_borrowing"
            st.session_state[SESSION_PATH_SELECTED] = True
            st.rerun()



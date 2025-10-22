"""
Responsible borrowing workflow UI components.
"""

import streamlit as st
from .config import (
    RESPONSIBLE_BORROWING_TITLE,
    RESPONSIBLE_BORROWING_DESCRIPTION,
    SESSION_PATH_SELECTED,
    SESSION_SELECTED_PATH
)


def render_responsible_borrowing() -> None:
    """Render the responsible borrowing workflow placeholder."""
    st.markdown(RESPONSIBLE_BORROWING_TITLE)
    st.write(RESPONSIBLE_BORROWING_DESCRIPTION)
    
    st.info("🚧 Αυτή η λειτουργία βρίσκεται υπό ανάπτυξη")
    
    if st.button("⬅️ Πίσω στην Επιλογή Διαδρομής"):
        st.session_state[SESSION_PATH_SELECTED] = False
        st.session_state[SESSION_SELECTED_PATH] = None
        st.rerun()



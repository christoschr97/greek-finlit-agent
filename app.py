"""
Streamlit UI for the Greek Financial Literacy Agent.
Run this for the web-based chat experience.
"""

import streamlit as st
from dotenv import load_dotenv
from finlit_agent.ui import (
    initialize_session_state,
    render_assessment,
    render_chat,
    config
)
from finlit_agent.ui.path_selection_ui import render_path_selection
from finlit_agent.ui.responsible_borrowing_ui import render_responsible_borrowing
from finlit_agent.database import check_db_connection, init_db
from finlit_agent.agent import create_financial_agent, BASE_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage

# Load environment variables
load_dotenv()


# Check database connection and initialize if needed
if check_db_connection():
    st.sidebar.success("✅ Database Connected")
    init_db()  # Create tables if they don't exist
else:
    st.sidebar.error("❌ Database Connection Failed")
    st.error("Unable to connect to database. Please check your configuration.")
    st.stop()

# Page config
st.set_page_config(**config.PAGE_CONFIG)

# Initialize session state
initialize_session_state()

# Title
st.title(config.APP_TITLE)

def _render_sidebar_navigation():
    if not st.session_state[config.SESSION_ASSESSMENT_DONE]:
        return
    st.sidebar.markdown(config.SIDEBAR_NAV_TITLE)
    if st.sidebar.button(config.GENERAL_CHAT_PATH, use_container_width=True):
        st.session_state[config.SESSION_SELECTED_PATH] = "general_chat"
        st.session_state[config.SESSION_PATH_SELECTED] = True
        st.rerun()
    if st.sidebar.button(config.RESPONSIBLE_BORROWING_PATH, use_container_width=True):
        st.session_state[config.SESSION_SELECTED_PATH] = "responsible_borrowing"
        st.session_state[config.SESSION_PATH_SELECTED] = True
        st.rerun()


# Main app logic with routing and sidebar navigation
_render_sidebar_navigation()

if not st.session_state[config.SESSION_ASSESSMENT_DONE]:
    render_assessment()
elif not st.session_state[config.SESSION_PATH_SELECTED]:
    render_path_selection()
elif st.session_state[config.SESSION_SELECTED_PATH] == "general_chat":
    # Ensure chat is initialized with assessment context before rendering chat
    if st.session_state[config.SESSION_AGENT] is None:
        agent = create_financial_agent()
        system_prompt = BASE_SYSTEM_PROMPT + st.session_state[config.SESSION_ASSESSMENT].get_context_summary()
        st.session_state[config.SESSION_AGENT] = agent
        st.session_state[config.SESSION_MESSAGES] = [SystemMessage(content=system_prompt)]
    render_chat()
elif st.session_state[config.SESSION_SELECTED_PATH] == "responsible_borrowing":
    render_responsible_borrowing()


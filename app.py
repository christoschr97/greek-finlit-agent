"""
Streamlit UI for the Greek Financial Literacy Agent.
Run this for the web-based chat experience.
"""

import streamlit as st
from dotenv import load_dotenv
from finlit_agent.ui import initialize_session_state, render_assessment, render_chat, config
from finlit_agent.database import check_db_connection, init_db

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

# Main app logic
if not st.session_state[config.SESSION_ASSESSMENT_DONE]:
    render_assessment()
else:
    render_chat()


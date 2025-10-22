"""
Chat UI components for the Streamlit app.
"""

from typing import List
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from .config import (
    CHAT_INPUT_PLACEHOLDER,
    THINKING_SPINNER,
    ERROR_PREFIX,
    SESSION_MESSAGES,
    SESSION_AGENT
)


def render_chat() -> None:
    """Render the chat interface."""
    _display_chat_history()
    _handle_chat_input()


def _display_chat_history() -> None:
    """Display all messages in the chat history (skip system message)."""
    messages: List[BaseMessage] = st.session_state[SESSION_MESSAGES]

    for msg in messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)


def _handle_chat_input() -> None:
    """Handle user input and generate agent response."""
    if prompt := st.chat_input(CHAT_INPUT_PLACEHOLDER):
        _process_user_message(prompt)


def _process_user_message(prompt: str) -> None:
    """Process user message and generate response."""
    # Add user message to history first
    messages: List[BaseMessage] = st.session_state[SESSION_MESSAGES]
    messages.append(HumanMessage(content=prompt))
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate and display agent response
    _generate_agent_response(messages)


def _generate_agent_response(messages: List[BaseMessage]) -> None:
    """Generate and display agent response."""
    agent = st.session_state[SESSION_AGENT]
    
    with st.chat_message("assistant"):
        with st.spinner(THINKING_SPINNER):
            try:
                response = agent.invoke(messages)
                st.write(response.content)
                messages.append(AIMessage(content=response.content))
            except Exception as e:
                error_message = f"{ERROR_PREFIX}: {str(e)}"
                st.error(error_message)
                # Remove the user message if response failed
                if messages and isinstance(messages[-1], HumanMessage):
                    messages.pop()

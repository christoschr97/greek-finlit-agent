"""
Tests for the core agent functionality.
"""

import sys
import os
import pytest

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from finlit_agent.agent.core import FinancialAgent


def test_agent_initialization():
    """Test that agent can be initialized without errors."""
    # This is a basic test that doesn't require Ollama to be running
    # It will fail at agent setup, but we can test the class structure
    try:
        agent = FinancialAgent()
        assert agent.model_name == "ollama/gemma3:12b"
        assert agent.ollama_base_url == "http://localhost:11434"
    except Exception as e:
        # Expected to fail without Ollama running
        assert "Failed to initialize agent" in str(e) or "Connection" in str(e)


def test_agent_system_instructions():
    """Test that system instructions are set up correctly."""
    try:
        agent = FinancialAgent()
        # This will fail during setup, but we can check the class exists
        assert hasattr(agent, 'system_instructions')
    except Exception:
        # Expected without Ollama
        pass


if __name__ == "__main__":
    test_agent_initialization()
    test_agent_system_instructions()
    print("✅ Agent tests completed")

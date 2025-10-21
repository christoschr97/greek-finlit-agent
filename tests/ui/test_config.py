"""
Simple tests for UI configuration.
"""

from finlit_agent.ui import config


def test_page_config_exists():
    """Test that PAGE_CONFIG is defined."""
    assert hasattr(config, 'PAGE_CONFIG')
    assert isinstance(config.PAGE_CONFIG, dict)


def test_page_config_has_required_fields():
    """Test that PAGE_CONFIG has all required fields."""
    assert 'page_title' in config.PAGE_CONFIG
    assert 'page_icon' in config.PAGE_CONFIG
    assert 'layout' in config.PAGE_CONFIG


def test_app_title_exists():
    """Test that APP_TITLE is defined."""
    assert hasattr(config, 'APP_TITLE')
    assert isinstance(config.APP_TITLE, str)
    assert len(config.APP_TITLE) > 0


def test_session_keys_are_strings():
    """Test that all session state keys are strings."""
    assert isinstance(config.SESSION_ASSESSMENT_DONE, str)
    assert isinstance(config.SESSION_CURRENT_QUESTION, str)
    assert isinstance(config.SESSION_ASSESSMENT, str)
    assert isinstance(config.SESSION_MESSAGES, str)
    assert isinstance(config.SESSION_AGENT, str)


def test_ui_strings_exist():
    """Test that UI strings are defined."""
    assert hasattr(config, 'ASSESSMENT_TITLE')
    assert hasattr(config, 'CHAT_INPUT_PLACEHOLDER')
    assert hasattr(config, 'NEXT_BUTTON')
    assert isinstance(config.NEXT_BUTTON, str)

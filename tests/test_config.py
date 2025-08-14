"""
Tests for configuration functionality.
"""

import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from finlit_agent.config.settings import get_config, get_config_dict, Config, AVAILABLE_MODELS, get_model_info, is_valid_model


def test_get_config():
    """Test configuration loading."""
    # Test new Config class
    config = get_config()
    assert isinstance(config, Config)
    assert hasattr(config, 'ollama')
    assert hasattr(config, 'agent')
    assert hasattr(config, 'logging')
    
    # Test backward compatibility with dict format
    config_dict = get_config_dict()
    assert isinstance(config_dict, dict)
    assert "ollama" in config_dict
    assert "agent" in config_dict
    assert "logging" in config_dict


def test_available_models():
    """Test available models configuration."""
    assert isinstance(AVAILABLE_MODELS, dict)
    assert len(AVAILABLE_MODELS) > 0
    assert "gemma3:12b" in AVAILABLE_MODELS


def test_model_validation():
    """Test model validation functions."""
    assert is_valid_model("gemma3:12b") == True
    assert is_valid_model("invalid-model") == False


def test_model_info():
    """Test model info retrieval."""
    info = get_model_info("gemma3:12b")
    assert isinstance(info, dict)
    assert "name" in info
    assert "description" in info


if __name__ == "__main__":
    test_get_config()
    test_available_models()
    test_model_validation()
    test_model_info()
    print("✅ Configuration tests completed")

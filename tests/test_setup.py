#!/usr/bin/env python3
"""
Simple test to verify the agent setup without requiring Ollama to be running.
"""

import sys
import os

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all required packages can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import smolagents
        print("✅ smolagents imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import smolagents: {e}")
        return False
    
    try:
        from smolagents import CodeAgent, DuckDuckGoSearchTool, PythonInterpreterTool
        print("✅ smolagents components imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import smolagents components: {e}")
        return False
    
    try:
        from smolagents.models import LiteLLMModel
        print("✅ LiteLLMModel imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LiteLLMModel: {e}")
        return False
    
    try:
        import litellm
        print("✅ litellm imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import litellm: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import requests: {e}")
        return False
    
    return True


def test_config():
    """Test the configuration module."""
    print("\n🧪 Testing configuration...")
    
    try:
        from finlit_agent.config.settings import get_config
        config = get_config()
        print("✅ Configuration loaded successfully")
        print(f"   Ollama URL: {config.ollama.base_url}")
        print(f"   Model: {config.ollama.model}")
        print(f"   Log Level: {config.logging.level}")
        return True
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False


def main():
    """Run all tests."""
    print("🔬 Financial Literacy Agent - Import Tests")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test configuration
    if not test_config():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! The agent is ready to use.")
        print("\n🚀 To start the agent (requires Ollama with gemma3:12b):")
        print("   python main.py")
    else:
        print("❌ Some tests failed. Please check the installation.")
        sys.exit(1)


if __name__ == "__main__":
    main()

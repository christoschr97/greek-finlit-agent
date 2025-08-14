#!/usr/bin/env python3
"""
Main entry point for the Financial Literacy Agent.

This is the simplified main entry point that imports from the modular structure.
"""

import os
import sys
import logging

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from finlit_agent.agent.core import FinancialAgent
from finlit_agent.config.settings import get_config, get_model_info, is_valid_model
from finlit_agent.utils.ollama import check_ollama_connection

# Get configuration
config = get_config()

# Configure logging using config
logging.basicConfig(
    level=getattr(logging, config.logging.level.upper()),
    format=config.logging.format
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the Financial Literacy Agent."""
    print("🚀 Starting Financial Literacy Agent...")
    
    # Use configuration for Ollama connection
    ollama_url = config.ollama.base_url
    
    if not check_ollama_connection(ollama_url):
        print(f"❌ Error: Could not connect to Ollama server at {ollama_url}")
        print("Please ensure that:")
        print("1. Ollama is installed and running")
        print("2. A compatible model is downloaded")
        print("\nTo install Ollama: https://ollama.ai/")
        print("To download models:")
        print("  ollama pull gemma3:12b    # Recommended (16GB+ RAM)")
        print("  ollama pull gemma3:7b     # Smaller option (8GB+ RAM)")
        print("  ollama pull llama3.2:8b   # Alternative (10GB+ RAM)")
        sys.exit(1)
    
    print("✅ Ollama connection successful!")
    
    # Get model name from configuration
    model_name = config.ollama.model
    # Ensure model name has the ollama/ prefix if not present
    if not model_name.startswith("ollama/"):
        model_name = f"ollama/{model_name}"
    
    # Show model configuration info
    clean_model_name = model_name.replace("ollama/", "")
    if is_valid_model(clean_model_name):
        model_info = get_model_info(clean_model_name)
        print(f"📋 Using model: {model_info.get('name', clean_model_name)}")
        print(f"   {model_info.get('description', 'No description available')}")
    else:
        print(f"📋 Using model: {model_name}")
        print("   (Model not in predefined list - this is okay if it works)")
    
    try:
        # Initialize and start the agent
        agent = FinancialAgent(model_name=model_name, ollama_base_url=ollama_url)
        agent.start_interactive_session()
        
    except Exception as e:
        logger.error(f"Failed to start agent: {e}")
        print(f"❌ Error during startup: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Check if the model is available: ollama list")
        print("2. Try a different model: export OLLAMA_MODEL='gemma3:7b'")
        print("3. Restart Ollama: ollama serve")
        sys.exit(1)


if __name__ == "__main__":
    main()
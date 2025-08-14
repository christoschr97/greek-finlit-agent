#!/usr/bin/env python3
"""
Quickstart script for the Financial Literacy Agent.
This script guides users through the initial setup and model selection.
"""

import os
import sys
import subprocess
import requests

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from finlit_agent.config.settings import AVAILABLE_MODELS, list_available_models


def check_python_version():
    """Check if Python version is 3.12+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 12):
        print(f"❌ Python 3.12+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version OK: {version.major}.{version.minor}")
    return True


def check_ollama():
    """Check if Ollama is installed and running."""
    print("🔍 Checking Ollama...")
    
    # Check if ollama command exists
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        print("✅ Ollama is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Ollama not found")
        print("   Install from: https://ollama.ai/")
        return False
    
    # Check if Ollama server is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running")
            return True
        else:
            print("❌ Ollama server not responding")
            return False
    except requests.exceptions.RequestException:
        print("❌ Ollama server not running")
        print("   Start with: ollama serve")
        return False


def list_installed_models():
    """List models that are already installed."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        installed = []
        for line in lines:
            if line.strip():
                model_name = line.split()[0]
                installed.append(model_name)
        return installed
    except subprocess.CalledProcessError:
        return []


def suggest_model():
    """Suggest the best model based on available models."""
    installed = list_installed_models()
    
    if not installed:
        print("📥 No models installed yet.")
        print("\nRecommended setup:")
        print("  ollama pull gemma3:12b    # Best quality (16GB+ RAM)")
        print("  ollama pull gemma3:7b     # Good performance (8GB+ RAM)")
        return None
    
    print(f"📋 Found {len(installed)} installed model(s):")
    for model in installed:
        if model in AVAILABLE_MODELS:
            info = AVAILABLE_MODELS[model]
            marker = " ⭐ (recommended)" if info["recommended"] else ""
            print(f"  • {model}{marker} - {info['description']}")
        else:
            print(f"  • {model}")
    
    # Find the best available model
    for model_id in ["gemma3:12b", "gemma3:7b", "llama3.2:8b"]:
        if model_id in installed:
            return model_id
    
    # Return the first installed model
    return installed[0] if installed else None


def setup_environment(model_id: str):
    """Set up environment variables."""
    print(f"\n🔧 Setting up environment for model: {model_id}")
    
    # Create a simple .env file
    env_content = f"""# Financial Literacy Agent Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL={model_id}
LOG_LEVEL=INFO
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    print(f"   Model: {model_id}")
    
    print("\n📝 To use these settings:")
    print("   source .env  # (in bash)")
    print("   python main.py")


def run_test():
    """Run a quick test to see if everything works."""
    print("\n🧪 Running quick test...")
    try:
        result = subprocess.run([sys.executable, "test_setup.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def main():
    """Main quickstart flow."""
    print("🚀 Financial Literacy Agent - Quickstart")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_ollama():
        print("\n❌ Please install and start Ollama first, then run this script again.")
        sys.exit(1)
    
    # Show available models
    print("\n📚 Available models:")
    list_available_models()
    
    # Suggest best model
    suggested_model = suggest_model()
    
    if suggested_model:
        print(f"\n💡 Recommended model to use: {suggested_model}")
        
        # Ask user if they want to use the suggested model
        response = input(f"\nUse {suggested_model}? (y/n): ").strip().lower()
        if response in ['y', 'yes', '']:
            setup_environment(suggested_model)
            
            # Run test
            if run_test():
                print("\n🎉 Setup complete! You can now run:")
                print("   python main.py")
            else:
                print("\n⚠️  Setup complete but tests failed. Try running anyway:")
                print("   python main.py")
        else:
            print("\n📝 Manual setup:")
            print("   export OLLAMA_MODEL='your-preferred-model'")
            print("   python main.py")
    else:
        print("\n📝 Please install a model first:")
        print("   ollama pull gemma3:12b")
        print("   python quickstart.py")


if __name__ == "__main__":
    main()

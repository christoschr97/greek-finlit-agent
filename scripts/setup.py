#!/usr/bin/env python3
"""
Setup script for the Financial Literacy Agent.
This script helps users set up the environment and dependencies.
"""

import subprocess
import sys
import os
import requests
from pathlib import Path


def run_command(command, description=""):
    """Run a shell command and handle errors."""
    print(f"🔄 {description or command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description or command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"   Output: {e.stderr}")
        return None


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
    print("🔍 Checking Ollama installation...")
    
    # Check if ollama command exists
    result = run_command("which ollama", "Checking Ollama installation")
    if not result:
        print("❌ Ollama not found. Please install it from https://ollama.ai/")
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
        print("❌ Ollama server not running. Start it with: ollama serve")
        return False


def check_gemma_model():
    """Check if Gemma 2 12B model is available."""
    print("🔍 Checking for Gemma 2 12B model...")
    
    result = run_command("ollama list", "Listing available models")
    if result and "gemma3:12b" in result:
        print("✅ Gemma 2 12B model found")
        return True
    else:
        print("❌ Gemma 2 12B model not found")
        return False


def install_gemma_model():
    """Install the Gemma 2 12B model."""
    print("📥 Installing Gemma 2 12B model (this may take a while)...")
    result = run_command("ollama pull gemma3:12b", "Downloading Gemma 2 12B model")
    return result is not None


def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    
    # Check if uv is available
    if run_command("which uv", "Checking for uv package manager"):
        result = run_command("uv sync", "Installing dependencies with uv")
    else:
        result = run_command("pip install -e .", "Installing dependencies with pip")
    
    return result is not None


def main():
    """Main setup function."""
    print("🚀 Financial Literacy Agent Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        print("\n📋 To install Ollama:")
        print("   Linux/macOS: curl -fsSL https://ollama.ai/install.sh | sh")
        print("   Windows: Download from https://ollama.ai/")
        print("   Then run: ollama serve")
        sys.exit(1)
    
    # Check Gemma model
    if not check_gemma_model():
        print("\n❓ Would you like to download the Gemma 2 12B model? (y/n): ", end="")
        response = input().strip().lower()
        
        if response in ['y', 'yes']:
            if not install_gemma_model():
                print("❌ Failed to install Gemma model")
                sys.exit(1)
        else:
            print("⚠️  You can install it later with: ollama pull gemma3:12b")
    
    # Install Python dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n🏃 To start the agent, run:")
    print("   python main.py")
    print("\n📚 For more information, see README.md")


if __name__ == "__main__":
    main()

"""
Ollama Utilities

Utility functions for interacting with the Ollama server.
"""


def check_ollama_connection(base_url: str = "http://localhost:11434") -> bool:
    """Check if Ollama server is running and accessible."""
    try:
        import requests
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

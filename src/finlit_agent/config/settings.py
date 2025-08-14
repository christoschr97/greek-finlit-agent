"""
Configuration settings for the Financial Literacy Agent.

This module provides a centralized configuration system that supports:
- Environment variables
- .env file loading
- Type validation
- Default values
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# Available models with their configurations
AVAILABLE_MODELS = {
    "gemma3:12b": {
        "name": "Gemma 3 12B",
        "description": "Best quality responses, requires 16GB+ RAM",
        "min_ram_gb": 16,
        "recommended": True
    },
    "gemma3:7b": {
        "name": "Gemma 3 7B", 
        "description": "Good balance of quality and performance, requires 8GB+ RAM",
        "min_ram_gb": 8,
        "recommended": False
    },
    "llama3.2:8b": {
        "name": "Llama 3.2 8B",
        "description": "Alternative model with different strengths, requires 10GB+ RAM", 
        "min_ram_gb": 10,
        "recommended": False
    }
}


@dataclass
class OllamaConfig:
    """Ollama server configuration."""
    base_url: str = "http://localhost:11434"
    model: str = "gemma3:12b"
    timeout: int = 30
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.base_url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid base_url: {self.base_url}")
        if self.timeout <= 0:
            raise ValueError(f"Invalid timeout: {self.timeout}")


@dataclass
class AgentConfig:
    """Agent behavior configuration."""
    max_iterations: int = 10
    temperature: float = 0.7
    enable_search: bool = True
    enable_calculations: bool = True
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not 0 <= self.temperature <= 2:
            raise ValueError(f"Invalid temperature: {self.temperature}")
        if self.max_iterations <= 0:
            raise ValueError(f"Invalid max_iterations: {self.max_iterations}")


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(levelname)s - %(message)s"
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.level.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {self.level}")


@dataclass
class Config:
    """Main configuration class for the Financial Literacy Agent."""
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> 'Config':
        """
        Create configuration from environment variables and optional .env file.
        
        Args:
            env_file: Path to .env file. If None, searches for .env in current directory
            
        Returns:
            Config instance with values from environment
        """
        # Load .env file if available
        if load_dotenv is not None:
            if env_file:
                load_dotenv(env_file)
            else:
                # Look for .env file in project root
                env_path = Path.cwd() / ".env"
                if env_path.exists():
                    load_dotenv(env_path)
        
        # Helper function to get environment variable with type conversion
        def get_env(key: str, default: Any, converter=str):
            value = os.getenv(key)
            if value is None:
                return default
            try:
                if converter == bool:
                    return value.lower() in ('true', '1', 'yes', 'on')
                return converter(value)
            except (ValueError, TypeError):
                return default
        
        # Create configurations from environment
        ollama_config = OllamaConfig(
            base_url=get_env("OLLAMA_BASE_URL", "http://localhost:11434"),
            model=get_env("OLLAMA_MODEL", "gemma3:12b"),
            timeout=get_env("OLLAMA_TIMEOUT", 30, int)
        )
        
        agent_config = AgentConfig(
            max_iterations=get_env("AGENT_MAX_ITERATIONS", 10, int),
            temperature=get_env("AGENT_TEMPERATURE", 0.7, float),
            enable_search=get_env("AGENT_ENABLE_SEARCH", True, bool),
            enable_calculations=get_env("AGENT_ENABLE_CALCULATIONS", True, bool)
        )
        
        logging_config = LoggingConfig(
            level=get_env("LOG_LEVEL", "INFO"),
            format=get_env("LOG_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
        )
        
        return cls(
            ollama=ollama_config,
            agent=agent_config,
            logging=logging_config
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary format (for backward compatibility)."""
        return {
            "ollama": {
                "base_url": self.ollama.base_url,
                "model": self.ollama.model,
                "timeout": self.ollama.timeout,
            },
            "agent": {
                "max_iterations": self.agent.max_iterations,
                "temperature": self.agent.temperature,
                "enable_search": self.agent.enable_search,
                "enable_calculations": self.agent.enable_calculations,
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
            }
        }


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config(reload: bool = False) -> Config:
    """
    Get the global configuration instance.
    
    Args:
        reload: If True, reload configuration from environment
        
    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None or reload:
        _config_instance = Config.from_env()
    return _config_instance


def get_config_dict(reload: bool = False) -> Dict[str, Any]:
    """
    Get configuration as dictionary (for backward compatibility).
    
    Args:
        reload: If True, reload configuration from environment
        
    Returns:
        Configuration dictionary
    """
    return get_config(reload=reload).to_dict()


def list_available_models() -> None:
    """Print available models with their descriptions."""
    print("Available models:")
    print("-" * 50)
    for model_id, info in AVAILABLE_MODELS.items():
        marker = " (recommended)" if info["recommended"] else ""
        print(f"• {model_id}{marker}")
        print(f"  Name: {info['name']}")
        print(f"  Description: {info['description']}")
        print(f"  Min RAM: {info['min_ram_gb']}GB")
        print()


def get_model_info(model_id: str) -> Dict[str, Any]:
    """Get information about a specific model."""
    return AVAILABLE_MODELS.get(model_id, {})


def is_valid_model(model_id: str) -> bool:
    """Check if a model ID is valid."""
    return model_id in AVAILABLE_MODELS


def print_config() -> None:
    """Print current configuration for debugging."""
    config = get_config()
    print("Current Configuration:")
    print("=" * 50)
    print(f"Ollama:")
    print(f"  Base URL: {config.ollama.base_url}")
    print(f"  Model: {config.ollama.model}")
    print(f"  Timeout: {config.ollama.timeout}s")
    print(f"Agent:")
    print(f"  Max Iterations: {config.agent.max_iterations}")
    print(f"  Temperature: {config.agent.temperature}")
    print(f"  Search Enabled: {config.agent.enable_search}")
    print(f"  Calculations Enabled: {config.agent.enable_calculations}")
    print(f"Logging:")
    print(f"  Level: {config.logging.level}")
    print(f"  Format: {config.logging.format}")
"""Configuration management for Project Sovereign.

This module handles loading configuration from environment variables
with sensible defaults.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from .env file if it exists."""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)


class Config:
    """Central configuration class for Project Sovereign."""

    def __init__(self) -> None:
        """Initialize configuration by loading environment variables."""
        load_environment()

    @property
    def ollama_host(self) -> str:
        """Get Ollama host URL from environment or default."""
        return os.getenv("OLLAMA_HOST", "http://localhost:11434")

    @property
    def ollama_model(self) -> str:
        """Get Ollama model name from environment or default."""
        return os.getenv("OLLAMA_MODEL", "llama3.2")

    @property
    def ollama_timeout(self) -> float:
        """Get Ollama request timeout from environment or default."""
        return float(os.getenv("OLLAMA_TIMEOUT", "30.0"))

    @property
    def ollama_max_retries(self) -> int:
        """Get Ollama max retries from environment or default."""
        return int(os.getenv("OLLAMA_MAX_RETRIES", "3"))

    @property
    def ollama_connection_pool_size(self) -> int:
        """Get Ollama connection pool size from environment or default."""
        return int(os.getenv("OLLAMA_CONNECTION_POOL_SIZE", "10"))

    @property
    def debug(self) -> bool:
        """Check if debug mode is enabled."""
        return os.getenv("SOVEREIGN_DEBUG", "").lower() in ("true", "1", "yes", "on")

    @property
    def log_level(self) -> str:
        """Get logging level from environment or default."""
        return os.getenv("SOVEREIGN_LOG_LEVEL", "INFO").upper()


# Global configuration instance
config = Config()

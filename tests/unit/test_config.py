"""
Unit tests for configuration management.
"""

import os
from unittest.mock import patch

import pytest

from project_sovereign.config import Config, load_environment


class TestConfig:
    """Test configuration management."""

    @patch.dict(os.environ, {}, clear=True)
    @patch("project_sovereign.config.load_dotenv")
    def test_default_values(self, mock_load_dotenv):
        """Test default configuration values when no environment variables are set."""
        # Ensure dotenv doesn't load any .env file
        mock_load_dotenv.return_value = None

        config = Config()

        assert config.ollama_host == "http://localhost:11434"
        assert config.ollama_model == "llama3.2"
        assert config.ollama_timeout == 30.0
        assert config.ollama_max_retries == 3
        assert config.ollama_connection_pool_size == 10
        assert config.debug is False
        assert config.log_level == "INFO"

    @patch.dict(
        os.environ,
        {
            "OLLAMA_HOST": "http://custom-host:8080",
            "OLLAMA_MODEL": "custom-model",
            "OLLAMA_TIMEOUT": "60.0",
            "OLLAMA_MAX_RETRIES": "5",
            "OLLAMA_CONNECTION_POOL_SIZE": "20",
            "SOVEREIGN_DEBUG": "true",
            "SOVEREIGN_LOG_LEVEL": "DEBUG",
        },
    )
    def test_environment_values(self):
        """Test configuration from environment variables."""
        config = Config()

        assert config.ollama_host == "http://custom-host:8080"
        assert config.ollama_model == "custom-model"
        assert config.ollama_timeout == 60.0
        assert config.ollama_max_retries == 5
        assert config.ollama_connection_pool_size == 20
        assert config.debug is True
        assert config.log_level == "DEBUG"

    @patch.dict(
        os.environ,
        {
            "SOVEREIGN_DEBUG": "1",
        },
    )
    def test_debug_flag_variations(self):
        """Test different debug flag values."""
        config = Config()
        assert config.debug is True

    @patch.dict(
        os.environ,
        {
            "SOVEREIGN_DEBUG": "yes",
        },
    )
    def test_debug_flag_yes(self):
        """Test debug flag with 'yes' value."""
        config = Config()
        assert config.debug is True

    @patch.dict(
        os.environ,
        {
            "SOVEREIGN_DEBUG": "false",
        },
    )
    def test_debug_flag_false(self):
        """Test debug flag with 'false' value."""
        config = Config()
        assert config.debug is False

    @patch.dict(
        os.environ,
        {
            "OLLAMA_TIMEOUT": "invalid",
        },
    )
    def test_invalid_numeric_value(self):
        """Test handling of invalid numeric values."""
        config = Config()

        with pytest.raises(ValueError):
            _ = config.ollama_timeout

    @patch("project_sovereign.config.Path")
    @patch("project_sovereign.config.load_dotenv")
    def test_load_environment_with_env_file(self, mock_load_dotenv, mock_path_class):
        """Test loading environment from .env file."""
        # Create a mock for the path instance
        mock_env_path = mock_path_class.cwd.return_value.__truediv__.return_value
        mock_env_path.exists.return_value = True

        load_environment()

        mock_load_dotenv.assert_called_once_with(mock_env_path)

    @patch("project_sovereign.config.Path")
    @patch("project_sovereign.config.load_dotenv")
    def test_load_environment_without_env_file(self, mock_load_dotenv, mock_path_class):
        """Test loading environment without .env file."""
        # Create a mock for the path instance
        mock_env_path = mock_path_class.cwd.return_value.__truediv__.return_value
        mock_env_path.exists.return_value = False

        load_environment()

        mock_load_dotenv.assert_not_called()

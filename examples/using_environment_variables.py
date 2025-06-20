#!/usr/bin/env python3
"""Example of using environment variables to configure PROJECT SOVEREIGN.

This example demonstrates how to set environment variables to customize
the Ollama connection settings.
"""

import os
import asyncio
from project_sovereign.agents.ollama_client import OllamaClient, OllamaConfig


async def main():
    """Demonstrate environment variable configuration."""
    
    # Example 1: Using default configuration (reads from environment)
    print("=== Using Default Configuration ===")
    default_config = OllamaConfig()
    print(f"Host: {default_config.base_url}")
    print(f"Model: {default_config.default_model}")
    print(f"Timeout: {default_config.timeout}s")
    print()
    
    # Example 2: Setting environment variables programmatically
    print("=== Setting Custom Environment Variables ===")
    os.environ["OLLAMA_HOST"] = "http://192.168.1.100:11434"
    os.environ["OLLAMA_MODEL"] = "qwen2.5-coder"
    os.environ["OLLAMA_TIMEOUT"] = "60"
    
    # Need to recreate config to pick up new environment variables
    from project_sovereign.config import Config
    custom_config = Config()
    
    print(f"Custom Host: {custom_config.ollama_host}")
    print(f"Custom Model: {custom_config.ollama_model}")
    print(f"Custom Timeout: {custom_config.ollama_timeout}s")
    print()
    
    # Example 3: Using the client with custom configuration
    print("=== Testing Connection ===")
    ollama_config = OllamaConfig(
        base_url=custom_config.ollama_host,
        default_model=custom_config.ollama_model,
        timeout=custom_config.ollama_timeout
    )
    
    async with OllamaClient(ollama_config) as client:
        # Test the connection
        is_healthy = await client.health_check()
        if is_healthy:
            print("✓ Successfully connected to Ollama")
            
            # List available models
            models = await client.list_models()
            if models:
                print(f"✓ Available models: {', '.join(models)}")
            else:
                print("✗ No models found")
        else:
            print("✗ Failed to connect to Ollama")
            print("  Make sure Ollama is running at the specified host")


if __name__ == "__main__":
    print("PROJECT SOVEREIGN - Environment Variable Configuration Example")
    print("=" * 60)
    print()
    print("You can set these environment variables:")
    print("  OLLAMA_HOST - Ollama server URL (default: http://localhost:11434)")
    print("  OLLAMA_MODEL - Default model to use (default: llama3.2)")
    print("  OLLAMA_TIMEOUT - Request timeout in seconds (default: 30.0)")
    print("  OLLAMA_MAX_RETRIES - Maximum retry attempts (default: 3)")
    print("  OLLAMA_CONNECTION_POOL_SIZE - Connection pool size (default: 10)")
    print()
    print("Or create a .env file in your project root with these values.")
    print()
    
    asyncio.run(main())
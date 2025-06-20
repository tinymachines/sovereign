"""
PROJECT SOVEREIGN AI/LLM Integration Components.

This package provides integration with local LLM services via Ollama,
enabling code generation and self-improvement capabilities.
"""

from .evolution_engine import EvolutionEngine, EvolutionHistory, EvolutionResult
from .model_manager import ModelInfo, ModelManager
from .ollama_client import OllamaClient, OllamaConfig, OllamaResponse

__all__ = [
    "EvolutionEngine",
    "EvolutionHistory",
    "EvolutionResult",
    "ModelInfo",
    "ModelManager",
    "OllamaClient",
    "OllamaConfig",
    "OllamaResponse",
]

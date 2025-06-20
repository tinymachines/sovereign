"""
Model management system for PROJECT SOVEREIGN.

Handles model selection, capability tracking, and fallback strategies
for LLM operations.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class ModelCapability(Enum):
    """Capabilities that models can have."""

    CODE_GENERATION = "code_generation"
    ERROR_ANALYSIS = "error_analysis"
    INSTRUCTION_FOLLOWING = "instruction_following"
    REASONING = "reasoning"
    LONG_CONTEXT = "long_context"
    FAST_INFERENCE = "fast_inference"


@dataclass
class ModelInfo:
    """Information about an available model."""

    name: str
    size: str  # e.g., "7b", "13b", "70b"
    capabilities: set[ModelCapability] = field(default_factory=set)
    context_length: int = 4096
    preferred_temperature: float = 0.7
    description: str = ""
    priority: int = 0  # Higher priority models are preferred


class ModelManager:
    """Manages model selection and capabilities."""

    # Predefined model configurations
    KNOWN_MODELS: ClassVar[dict[str, ModelInfo]] = {
        "llama3.2": ModelInfo(
            name="llama3.2",
            size="3b",
            capabilities={
                ModelCapability.CODE_GENERATION,
                ModelCapability.INSTRUCTION_FOLLOWING,
                ModelCapability.FAST_INFERENCE,
            },
            context_length=128000,
            preferred_temperature=0.7,
            description="Latest Llama model, good for code generation",
            priority=90,
        ),
        "llama3.2:1b": ModelInfo(
            name="llama3.2:1b",
            size="1b",
            capabilities={
                ModelCapability.INSTRUCTION_FOLLOWING,
                ModelCapability.FAST_INFERENCE,
            },
            context_length=128000,
            preferred_temperature=0.7,
            description="Smallest Llama 3.2 model, very fast",
            priority=70,
        ),
        "qwen2.5-coder": ModelInfo(
            name="qwen2.5-coder",
            size="7b",
            capabilities={
                ModelCapability.CODE_GENERATION,
                ModelCapability.ERROR_ANALYSIS,
                ModelCapability.REASONING,
            },
            context_length=32768,
            preferred_temperature=0.3,
            description="Specialized for code generation and analysis",
            priority=95,
        ),
        "deepseek-coder-v2": ModelInfo(
            name="deepseek-coder-v2",
            size="16b",
            capabilities={
                ModelCapability.CODE_GENERATION,
                ModelCapability.ERROR_ANALYSIS,
                ModelCapability.LONG_CONTEXT,
            },
            context_length=128000,
            preferred_temperature=0.3,
            description="Advanced code model with long context",
            priority=85,
        ),
        "mistral": ModelInfo(
            name="mistral",
            size="7b",
            capabilities={
                ModelCapability.INSTRUCTION_FOLLOWING,
                ModelCapability.REASONING,
                ModelCapability.FAST_INFERENCE,
            },
            context_length=8192,
            preferred_temperature=0.7,
            description="General purpose model",
            priority=80,
        ),
        "codellama": ModelInfo(
            name="codellama",
            size="7b",
            capabilities={
                ModelCapability.CODE_GENERATION,
                ModelCapability.ERROR_ANALYSIS,
            },
            context_length=16384,
            preferred_temperature=0.1,
            description="Meta's code-specific model",
            priority=88,
        ),
    }

    def __init__(self, client: OllamaClient | None = None):
        self.client = client or OllamaClient()
        self._available_models: dict[str, ModelInfo] = {}
        self._initialized = False
        self._lock = asyncio.Lock()

    async def initialize(self) -> None:
        """Initialize model manager by checking available models."""
        async with self._lock:
            if self._initialized:
                return

            try:
                # Get list of installed models from Ollama
                installed_models = await self.client.list_models()

                # Match with known models
                for model_name in installed_models:
                    # Handle model variants (e.g., "llama3.2:latest" -> "llama3.2")
                    base_name = model_name.split(":")[0]

                    if base_name in self.KNOWN_MODELS:
                        self._available_models[model_name] = self.KNOWN_MODELS[
                            base_name
                        ]
                    else:
                        # Unknown model - create basic info
                        self._available_models[model_name] = ModelInfo(
                            name=model_name,
                            size="unknown",
                            capabilities={ModelCapability.INSTRUCTION_FOLLOWING},
                            description=f"Unknown model: {model_name}",
                            priority=50,
                        )

                self._initialized = True
                logger.info(
                    f"Model manager initialized with {len(self._available_models)} models"
                )

            except Exception as e:
                logger.error(f"Failed to initialize model manager: {e}")
                # Continue with empty model list
                self._initialized = True

    async def get_available_models(self) -> list[ModelInfo]:
        """Get list of available models."""
        if not self._initialized:
            await self.initialize()
        return list(self._available_models.values())

    async def select_model(
        self,
        capabilities: set[ModelCapability] | None = None,
        prefer_fast: bool = False,
        min_context: int = 4096,
    ) -> ModelInfo | None:
        """Select best model based on requirements."""
        if not self._initialized:
            await self.initialize()

        if not self._available_models:
            logger.warning("No models available")
            return None

        candidates = list(self._available_models.values())

        # Filter by required capabilities
        if capabilities:
            candidates = [
                m for m in candidates if capabilities.issubset(m.capabilities)
            ]

        # Filter by context length
        candidates = [m for m in candidates if m.context_length >= min_context]

        if not candidates:
            logger.warning(f"No models match requirements: {capabilities}")
            # Fallback to any available model
            candidates = list(self._available_models.values())

        # Sort by priority and speed preference
        if prefer_fast:
            # Prioritize fast inference models
            candidates.sort(
                key=lambda m: (
                    ModelCapability.FAST_INFERENCE in m.capabilities,
                    m.priority,
                ),
                reverse=True,
            )
        else:
            # Sort by priority only
            candidates.sort(key=lambda m: m.priority, reverse=True)

        selected = candidates[0] if candidates else None
        if selected:
            logger.info(
                f"Selected model: {selected.name} (priority: {selected.priority})"
            )

        return selected

    async def get_model_info(self, model_name: str) -> ModelInfo | None:
        """Get information about a specific model."""
        if not self._initialized:
            await self.initialize()

        # Check exact match first
        if model_name in self._available_models:
            return self._available_models[model_name]

        # Check base name match
        base_name = model_name.split(":")[0]
        for available_name, info in self._available_models.items():
            if available_name.split(":")[0] == base_name:
                return info

        return None

    def get_fallback_chain(self, primary_model: str) -> list[str]:
        """Get fallback model chain for a given primary model."""
        fallbacks = []

        # Get primary model info
        primary_info = None
        base_name = primary_model.split(":")[0]
        if base_name in self.KNOWN_MODELS:
            primary_info = self.KNOWN_MODELS[base_name]

        if primary_info:
            # Find models with similar capabilities but different priorities
            similar_models = []
            for model_name, info in self._available_models.items():
                if model_name != primary_model and info.capabilities.intersection(
                    primary_info.capabilities
                ):
                    similar_models.append((info.priority, model_name))

            # Sort by priority (descending)
            similar_models.sort(reverse=True)
            fallbacks = [name for _, name in similar_models[:3]]  # Top 3 fallbacks
        else:
            # Generic fallback chain
            all_models = sorted(
                self._available_models.items(),
                key=lambda x: x[1].priority,
                reverse=True,
            )
            fallbacks = [name for name, _ in all_models if name != primary_model][:3]

        return fallbacks

    async def test_model(self, model_name: str) -> bool:
        """Test if a model is working correctly."""
        try:
            response = await self.client.generate(
                prompt="Reply with 'OK' if you can read this.",
                model=model_name,
                max_tokens=10,
                temperature=0.1,
            )
            return not response.error and "OK" in response.response.upper()
        except Exception as e:
            logger.error(f"Model test failed for {model_name}: {e}")
            return False

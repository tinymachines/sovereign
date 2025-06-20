"""
Runtime adapter for async LLM operations in PROJECT SOVEREIGN.

Provides synchronous interface to async LLM operations for integration
with the synchronous VM execution model.
"""

import asyncio
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from .evolution_engine import EvolutionEngine, EvolutionResult
from .model_manager import ModelCapability, ModelManager
from .ollama_client import OllamaClient, OllamaConfig

logger = logging.getLogger(__name__)


class LLMRuntimeAdapter:
    """Adapter to bridge sync VM execution with async LLM operations."""

    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or OllamaConfig()
        self._client: OllamaClient | None = None
        self._model_manager: ModelManager | None = None
        self._evolution_engine: EvolutionEngine | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._initialized = False

    def _start_event_loop(self) -> None:
        """Start event loop in separate thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def initialize(self) -> None:
        """Initialize the runtime adapter."""
        if self._initialized:
            return

        # Start event loop in background thread
        self._thread = threading.Thread(target=self._start_event_loop, daemon=True)
        self._thread.start()

        # Wait for loop to start with timeout
        timeout = 5.0  # 5 second timeout
        start_time = time.time()
        while (self._loop is None or not self._loop.is_running()) and (time.time() - start_time) < timeout:
            time.sleep(0.01)  # Small sleep to avoid busy-waiting
        
        if self._loop is None or not self._loop.is_running():
            raise RuntimeError("Failed to start event loop within timeout")

        # Initialize async components
        future = asyncio.run_coroutine_threadsafe(self._async_initialize(), self._loop)
        future.result(timeout=30)  # Wait up to 30 seconds

        self._initialized = True
        logger.info("LLM runtime adapter initialized")

    async def _async_initialize(self) -> None:
        """Async initialization of components."""
        self._client = OllamaClient(self.config)
        self._model_manager = ModelManager(self._client)
        self._evolution_engine = EvolutionEngine(
            client=self._client,
            model_manager=self._model_manager,
        )

        # Initialize model manager
        await self._model_manager.initialize()

        # Check if Ollama is available
        is_healthy = await self._client.health_check()
        if not is_healthy:
            logger.warning(
                "Ollama service is not available - LLM features will be limited"
            )

    def shutdown(self) -> None:
        """Shutdown the runtime adapter."""
        if self._loop and self._loop.is_running():
            # Schedule cleanup
            asyncio.run_coroutine_threadsafe(self._async_shutdown(), self._loop).result(
                timeout=10
            )

            # Stop event loop
            self._loop.call_soon_threadsafe(self._loop.stop)

        if self._thread:
            self._thread.join(timeout=5)

        self._executor.shutdown(wait=True)
        self._initialized = False

    async def _async_shutdown(self) -> None:
        """Async cleanup of components."""
        if self._client:
            await self._client.close()

    def generate_code(
        self,
        prompt: str,
        language: str = "assembly",
        timeout: float = 30.0,
    ) -> str:
        """Generate code synchronously using LLM."""
        if not self._initialized:
            self.initialize()

        future = asyncio.run_coroutine_threadsafe(
            self._async_generate_code(prompt, language),
            self._loop,
        )

        try:
            return future.result(timeout=timeout)
        except TimeoutError as err:
            raise RuntimeError(
                f"Code generation timed out after {timeout} seconds"
            ) from err
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {e}") from e

    async def _async_generate_code(self, prompt: str, language: str) -> str:
        """Async code generation."""
        if not self._client:
            raise RuntimeError("LLM client not initialized")

        # Select best model for code generation
        model_info = await self._model_manager.select_model(
            capabilities={ModelCapability.CODE_GENERATION}
        )

        if not model_info:
            raise RuntimeError("No suitable model available for code generation")

        return await self._client.code_generate(
            prompt=prompt,
            language=language,
            model=model_info.name,
            temperature=model_info.preferred_temperature,
        )

    def evolve_code(
        self,
        code: str,
        error_context: str,
        timeout: float = 60.0,
    ) -> EvolutionResult:
        """Evolve code based on error context."""
        if not self._initialized:
            self.initialize()

        future = asyncio.run_coroutine_threadsafe(
            self._evolution_engine.evolve(code, error_context),
            self._loop,
        )

        try:
            return future.result(timeout=timeout)
        except TimeoutError as err:
            raise RuntimeError(
                f"Code evolution timed out after {timeout} seconds"
            ) from err
        except Exception as e:
            raise RuntimeError(f"Code evolution failed: {e}") from e

    def analyze_error(
        self,
        error: str,
        context: str,
        timeout: float = 30.0,
    ) -> dict[str, Any]:
        """Analyze error and get suggestions."""
        if not self._initialized:
            self.initialize()

        future = asyncio.run_coroutine_threadsafe(
            self._async_analyze_error(error, context),
            self._loop,
        )

        try:
            return future.result(timeout=timeout)
        except TimeoutError as err:
            raise RuntimeError(
                f"Error analysis timed out after {timeout} seconds"
            ) from err
        except Exception as e:
            raise RuntimeError(f"Error analysis failed: {e}") from e

    async def _async_analyze_error(self, error: str, context: str) -> dict[str, Any]:
        """Async error analysis."""
        if not self._client:
            raise RuntimeError("LLM client not initialized")

        # Select model for error analysis
        model_info = await self._model_manager.select_model(
            capabilities={ModelCapability.ERROR_ANALYSIS}
        )

        if not model_info:
            raise RuntimeError("No suitable model available for error analysis")

        return await self._client.analyze_error(
            error=error,
            context=context,
            model=model_info.name,
        )

    def get_available_models(self) -> list[str]:
        """Get list of available models."""
        if not self._initialized:
            self.initialize()

        future = asyncio.run_coroutine_threadsafe(
            self._async_get_models(),
            self._loop,
        )

        try:
            return future.result(timeout=10)
        except Exception:
            return []

    async def _async_get_models(self) -> list[str]:
        """Async get available models."""
        models = await self._model_manager.get_available_models()
        return [m.name for m in models]

    def get_evolution_stats(self) -> dict[str, Any]:
        """Get evolution statistics."""
        if not self._evolution_engine:
            return {}
        return self._evolution_engine.get_evolution_stats()


# Global singleton instance
_runtime_adapter: LLMRuntimeAdapter | None = None


def get_llm_runtime() -> LLMRuntimeAdapter:
    """Get or create the global LLM runtime adapter."""
    global _runtime_adapter
    if _runtime_adapter is None:
        _runtime_adapter = LLMRuntimeAdapter()
    return _runtime_adapter

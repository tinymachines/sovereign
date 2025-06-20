"""
Unit tests for LLM integration in PROJECT SOVEREIGN.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from project_sovereign.agents.evolution_engine import (
    ErrorCategory,
    ErrorPattern,
    EvolutionEngine,
    EvolutionHistory,
    EvolutionResult,
)
from project_sovereign.agents.model_manager import (
    ModelCapability,
    ModelInfo,
    ModelManager,
)
from project_sovereign.agents.ollama_client import (
    OllamaClient,
    OllamaConfig,
    OllamaResponse,
)
from project_sovereign.agents.runtime_adapter import LLMRuntimeAdapter
from project_sovereign.config import config


class TestOllamaClient:
    """Test Ollama client functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        # Test with custom config, using environment variables where appropriate
        ollama_config = OllamaConfig(
            base_url="http://localhost:11434",
            timeout=30.0,
            max_retries=3,
            connection_pool_size=10,
            default_model=config.ollama_model,  # Use env value
        )
        return OllamaClient(ollama_config)

    @pytest.mark.asyncio
    async def test_health_check_success(self, client):
        """Test successful health check."""
        with patch.object(client, "_ensure_session", new_callable=AsyncMock):
            client._session = MagicMock()
            mock_response = MagicMock()
            mock_response.status = 200

            client._session.get.return_value.__aenter__.return_value = mock_response

            result = await client.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self, client):
        """Test failed health check."""
        with (
            patch.object(client, "_ensure_session", new_callable=AsyncMock),
            patch(
                "aiohttp.ClientSession.get", side_effect=Exception("Connection error")
            ),
        ):
            result = await client.health_check()
            assert result is False

    @pytest.mark.asyncio
    async def test_list_models(self, client):
        """Test listing available models."""
        with patch.object(client, "_ensure_session", new_callable=AsyncMock):
            client._session = MagicMock()
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(
                return_value={
                    "models": [
                        {"name": config.ollama_model},
                        {"name": "qwen2.5-coder"},
                    ]
                }
            )

            client._session.get.return_value.__aenter__.return_value = mock_response

            models = await client.list_models()
            assert models == [config.ollama_model, "qwen2.5-coder"]

    @pytest.mark.asyncio
    async def test_generate_single_response(self, client):
        """Test single response generation."""
        with patch.object(client, "_ensure_session", new_callable=AsyncMock):
            client._session = MagicMock()
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(
                return_value={
                    "model": config.ollama_model,
                    "response": "Generated text",
                    "done": True,
                    "context": [1, 2, 3],
                    "total_duration": 1000,
                }
            )

            client._session.post.return_value.__aenter__.return_value = mock_response

            response = await client.generate("Test prompt", model=config.ollama_model)

            assert isinstance(response, OllamaResponse)
            assert response.model == config.ollama_model
            assert response.response == "Generated text"
            assert response.done is True
            assert response.context == [1, 2, 3]

    @pytest.mark.asyncio
    async def test_generate_with_retry(self, client):
        """Test generation with retry logic."""
        client.config.max_retries = 3
        client.config.retry_delay = 0.1

        with patch.object(client, "_ensure_session", new_callable=AsyncMock):
            client._session = MagicMock()
            # First two attempts fail, third succeeds
            mock_responses = [
                Exception("Connection error"),
                Exception("Timeout"),
                MagicMock(
                    status=200,
                    json=AsyncMock(
                        return_value={
                            "model": config.ollama_model,
                            "response": "Success after retries",
                            "done": True,
                        }
                    ),
                ),
            ]

            client._session.post.return_value.__aenter__.side_effect = mock_responses

            response = await client.generate("Test prompt")

            assert response.response == "Success after retries"
            assert client._session.post.call_count == 3

    @pytest.mark.asyncio
    async def test_code_generate(self, client):
        """Test code generation with prompt engineering."""
        with patch.object(client, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = OllamaResponse(
                model="qwen2.5-coder",
                response="```python\nprint('Hello')\n```",
                done=True,
            )

            code = await client.code_generate("Print hello", language="python")

            assert code == "print('Hello')"
            assert (
                "only valid python code" in mock_generate.call_args[1]["prompt"].lower()
            )

    @pytest.mark.asyncio
    async def test_analyze_error(self, client):
        """Test error analysis."""
        with patch.object(client, "generate", new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = OllamaResponse(
                model=config.ollama_model,
                response=json.dumps(
                    {
                        "error_type": "syntax",
                        "root_cause": "Missing closing bracket",
                        "fix_strategy": "Add closing bracket",
                        "code_suggestion": "print('hello')",
                    }
                ),
                done=True,
            )

            analysis = await client.analyze_error(
                "SyntaxError: unexpected EOF", "print('hello'"
            )

            assert analysis["error_type"] == "syntax"
            assert analysis["root_cause"] == "Missing closing bracket"
            assert analysis["fix_strategy"] == "Add closing bracket"
            assert analysis["code_suggestion"] == "print('hello')"


class TestModelManager:
    """Test model management functionality."""

    @pytest.fixture
    def manager(self):
        """Create test model manager."""
        client = MagicMock(spec=OllamaClient)
        return ModelManager(client)

    @pytest.mark.asyncio
    async def test_initialize(self, manager):
        """Test model manager initialization."""
        manager.client.list_models = AsyncMock(
            return_value=[
                f"{config.ollama_model}:latest",
                "qwen2.5-coder",
                "unknown-model",
            ]
        )

        await manager.initialize()

        assert manager._initialized is True
        assert len(manager._available_models) == 3
        assert f"{config.ollama_model}:latest" in manager._available_models
        assert "qwen2.5-coder" in manager._available_models
        assert "unknown-model" in manager._available_models

    @pytest.mark.asyncio
    async def test_select_model_by_capability(self, manager):
        """Test model selection by capability."""
        # Set up available models
        manager._available_models = {
            "llama3.2": ModelManager.KNOWN_MODELS["llama3.2"],
            "qwen2.5-coder": ModelManager.KNOWN_MODELS["qwen2.5-coder"],
        }
        manager._initialized = True

        # Select model for code generation
        model = await manager.select_model(
            capabilities={ModelCapability.CODE_GENERATION}
        )

        assert model is not None
        assert ModelCapability.CODE_GENERATION in model.capabilities

    @pytest.mark.asyncio
    async def test_select_model_prefer_fast(self, manager):
        """Test model selection with speed preference."""
        # Set up available models
        manager._available_models = {
            "llama3.2": ModelManager.KNOWN_MODELS["llama3.2"],
            "llama3.2:1b": ModelManager.KNOWN_MODELS["llama3.2:1b"],
        }
        manager._initialized = True

        # Select fast model
        model = await manager.select_model(prefer_fast=True)

        assert model is not None
        assert ModelCapability.FAST_INFERENCE in model.capabilities

    def test_get_fallback_chain(self, manager):
        """Test fallback chain generation."""
        manager._available_models = {
            "llama3.2": ModelManager.KNOWN_MODELS["llama3.2"],
            "qwen2.5-coder": ModelManager.KNOWN_MODELS["qwen2.5-coder"],
            "mistral": ModelManager.KNOWN_MODELS["mistral"],
        }

        fallbacks = manager.get_fallback_chain("llama3.2")

        assert len(fallbacks) > 0
        assert "llama3.2" not in fallbacks

    @pytest.mark.asyncio
    async def test_test_model(self, manager):
        """Test model health check."""
        manager.client.generate = AsyncMock(
            return_value=OllamaResponse(
                model=config.ollama_model,
                response="OK",
                done=True,
            )
        )

        result = await manager.test_model(config.ollama_model)

        assert result is True
        manager.client.generate.assert_called_once()


class TestEvolutionEngine:
    """Test evolution engine functionality."""

    @pytest.fixture
    def engine(self):
        """Create test evolution engine."""
        client = MagicMock(spec=OllamaClient)
        manager = MagicMock(spec=ModelManager)
        return EvolutionEngine(client, manager)

    def test_categorize_error(self, engine):
        """Test error categorization."""
        test_cases = [
            ("SyntaxError: invalid syntax", ErrorCategory.SYNTAX_ERROR),
            ("Stack overflow", ErrorCategory.STACK_ERROR),
            ("Memory limit exceeded", ErrorCategory.MEMORY_ERROR),
            ("TypeError: unsupported operand", ErrorCategory.TYPE_ERROR),
            ("Execution limit exceeded", ErrorCategory.RESOURCE_LIMIT),
            ("RuntimeError: undefined variable", ErrorCategory.RUNTIME_ERROR),
            ("Unknown error", ErrorCategory.UNKNOWN),
        ]

        for error_msg, expected_category in test_cases:
            category = engine._categorize_error(error_msg)
            assert category == expected_category

    def test_error_pattern_matching(self):
        """Test error pattern matching."""
        pattern = ErrorPattern(
            category=ErrorCategory.SYNTAX_ERROR,
            pattern="missing closing bracket",
        )

        assert pattern.matches("SyntaxError: missing closing bracket")
        assert pattern.matches("Error: MISSING CLOSING BRACKET")
        assert not pattern.matches("Different error")

    def test_error_pattern_similarity(self):
        """Test error pattern similarity scoring."""
        pattern = ErrorPattern(
            category=ErrorCategory.RUNTIME_ERROR,
            pattern="undefined variable foo",
        )

        # Exact match
        assert pattern.similarity_score("undefined variable foo") == 1.0

        # Partial match
        score = pattern.similarity_score("runtime error: undefined variable bar")
        assert 0 < score < 1.0

        # No match
        assert pattern.similarity_score("completely different error") < 0.5

    @pytest.mark.asyncio
    async def test_evolve_success(self, engine):
        """Test successful code evolution."""
        # Mock model selection
        engine.model_manager.select_model = AsyncMock(
            return_value=ModelInfo(
                name="qwen2.5-coder",
                size="7b",
                capabilities={ModelCapability.CODE_GENERATION},
            )
        )

        # Mock error analysis
        engine.client.analyze_error = AsyncMock(
            return_value={
                "error_type": "syntax",
                "root_cause": "Missing HALT",
                "fix_strategy": "Add HALT at end",
            }
        )

        # Mock code generation
        engine.client.code_generate = AsyncMock(return_value="PUSH #42\nHALT")

        # Mock validation
        with patch.object(
            engine, "_validate_fix", new_callable=AsyncMock
        ) as mock_validate:
            mock_validate.return_value = True

            result = await engine.evolve(
                code="PUSH #42",
                error_context="Program did not halt",
            )

            assert result.success is True
            assert result.fixed_code == "PUSH #42\nHALT"
            assert result.error_category == ErrorCategory.RUNTIME_ERROR
            assert result.confidence > 0

    @pytest.mark.asyncio
    async def test_evolve_failure(self, engine):
        """Test failed code evolution."""
        # Mock model selection
        engine.model_manager.select_model = AsyncMock(return_value=None)

        result = await engine.evolve(
            code="INVALID CODE",
            error_context="Syntax error",
        )

        assert result.success is False
        assert result.fixed_code is None

    def test_evolution_history(self):
        """Test evolution history tracking."""
        history = EvolutionHistory()

        # Add successful result
        history.add_result(
            EvolutionResult(
                success=True,
                original_error="Error 1",
            )
        )

        # Add failed result
        history.add_result(
            EvolutionResult(
                success=False,
                original_error="Error 2",
            )
        )

        assert history.total_attempts == 2
        assert history.successful_fixes == 1
        assert history.get_success_rate() == 0.5

    def test_pattern_export_import(self, engine):
        """Test pattern export and import."""
        # Add some patterns
        engine._update_patterns("Stack overflow", ErrorCategory.STACK_ERROR, True)
        engine._update_patterns("Memory error", ErrorCategory.MEMORY_ERROR, False)

        # Export patterns
        exported = engine.export_patterns()
        assert isinstance(exported, str)

        # Create new engine and import
        new_engine = EvolutionEngine()
        new_engine.import_patterns(exported)

        assert len(new_engine.history.error_patterns) == 2


class TestRuntimeAdapter:
    """Test runtime adapter functionality."""

    @pytest.fixture
    def adapter(self):
        """Create test runtime adapter."""
        return LLMRuntimeAdapter()

    def test_initialize(self, adapter):
        """Test adapter initialization."""
        with patch("threading.Thread.start"):
            adapter.initialize()

            assert adapter._initialized is True

    def test_generate_code_sync(self, adapter):
        """Test synchronous code generation."""

        # Mock async generate
        async def mock_generate(*args, **kwargs):
            return "Generated code"

        with (
            patch.object(adapter, "_async_generate_code", side_effect=mock_generate),
            patch.object(adapter, "_loop", create=True),
        ):
            adapter._loop.is_running.return_value = True
            adapter._initialized = True

            with patch("asyncio.run_coroutine_threadsafe") as mock_run:
                mock_future = MagicMock()
                mock_future.result.return_value = "Generated code"
                mock_run.return_value = mock_future

                result = adapter.generate_code("Test prompt")

                assert result == "Generated code"

    def test_evolve_code_sync(self, adapter):
        """Test synchronous code evolution."""
        # Mock async evolve
        mock_result = EvolutionResult(
            success=True,
            original_error="Test error",
            fixed_code="Fixed code",
        )

        adapter._initialized = True
        adapter._evolution_engine = MagicMock()

        with patch.object(adapter, "_loop", create=True):
            adapter._loop.is_running.return_value = True

            with patch("asyncio.run_coroutine_threadsafe") as mock_run:
                mock_future = MagicMock()
                mock_future.result.return_value = mock_result
                mock_run.return_value = mock_future

                result = adapter.evolve_code("Code", "Error")

                assert result.success is True
                assert result.fixed_code == "Fixed code"

"""
Ollama client wrapper for PROJECT SOVEREIGN.

Provides async HTTP interface to Ollama for local LLM inference,
with connection pooling, retry logic, and error handling.
"""

import asyncio
import json
import logging
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any
from urllib.parse import urljoin

import aiohttp
from aiohttp import ClientTimeout

from ..config import config

logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig:
    """Configuration for Ollama client."""

    base_url: str = config.ollama_host
    timeout: float = config.ollama_timeout
    max_retries: int = config.ollama_max_retries
    retry_delay: float = 1.0  # seconds
    connection_pool_size: int = config.ollama_connection_pool_size
    default_model: str = config.ollama_model
    temperature: float = 0.7
    max_tokens: int = 2048


@dataclass
class OllamaResponse:
    """Response from Ollama API."""

    model: str
    response: str
    done: bool = True
    context: list[int] = field(default_factory=list)
    total_duration: int = 0
    eval_count: int = 0
    eval_duration: int = 0
    prompt_eval_count: int = 0
    prompt_eval_duration: int = 0
    error: str | None = None


class OllamaClient:
    """Async client for Ollama API integration."""

    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or OllamaConfig()
        self._session: aiohttp.ClientSession | None = None
        self._connector: aiohttp.TCPConnector | None = None
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        await self._ensure_session()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def _ensure_session(self) -> None:
        """Ensure HTTP session is created."""
        async with self._lock:
            if self._session is None or self._session.closed:
                self._connector = aiohttp.TCPConnector(
                    limit=self.config.connection_pool_size,
                    limit_per_host=self.config.connection_pool_size,
                )
                timeout = ClientTimeout(total=self.config.timeout)
                self._session = aiohttp.ClientSession(
                    connector=self._connector,
                    timeout=timeout,
                )

    async def close(self) -> None:
        """Close HTTP session and cleanup resources."""
        if self._session and not self._session.closed:
            await self._session.close()
        if self._connector and not self._connector.closed:
            await self._connector.close()

    async def health_check(self) -> bool:
        """Check if Ollama service is healthy."""
        try:
            await self._ensure_session()
            url = urljoin(self.config.base_url, "/api/tags")

            async with self._session.get(url) as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def list_models(self) -> list[str]:
        """List available models."""
        await self._ensure_session()
        url = urljoin(self.config.base_url, "/api/tags")

        try:
            async with self._session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [model["name"] for model in data.get("models", [])]
                logger.error(f"Failed to list models: {response.status}")
                return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    async def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        context: list[int] | None = None,
        stream: bool = False,
    ) -> OllamaResponse | AsyncIterator[OllamaResponse]:
        """Generate response from LLM."""
        await self._ensure_session()

        model = model or self.config.default_model
        temperature = (
            temperature if temperature is not None else self.config.temperature
        )
        max_tokens = max_tokens or self.config.max_tokens

        url = urljoin(self.config.base_url, "/api/generate")
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        if context:
            payload["context"] = context

        if stream:
            return self._generate_stream(url, payload)
        return await self._generate_single(url, payload)

    async def _generate_single(
        self, url: str, payload: dict[str, Any]
    ) -> OllamaResponse:
        """Generate single response with retry logic."""
        last_error = None

        for attempt in range(self.config.max_retries):
            try:
                async with self._session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return OllamaResponse(
                            model=data["model"],
                            response=data["response"],
                            done=data["done"],
                            context=data.get("context", []),
                            total_duration=data.get("total_duration", 0),
                            eval_count=data.get("eval_count", 0),
                            eval_duration=data.get("eval_duration", 0),
                            prompt_eval_count=data.get("prompt_eval_count", 0),
                            prompt_eval_duration=data.get("prompt_eval_duration", 0),
                        )
                    error_text = await response.text()
                    last_error = f"HTTP {response.status}: {error_text}"
                    logger.error(f"Generation failed: {last_error}")

            except TimeoutError:
                last_error = "Request timed out"
                logger.error(f"Timeout on attempt {attempt + 1}")
            except Exception as e:
                last_error = str(e)
                logger.error(f"Error on attempt {attempt + 1}: {e}")

            if attempt < self.config.max_retries - 1:
                await asyncio.sleep(self.config.retry_delay * (attempt + 1))

        return OllamaResponse(
            model=payload["model"],
            response="",
            done=True,
            error=f"Failed after {self.config.max_retries} attempts: {last_error}",
        )

    async def _generate_stream(
        self, url: str, payload: dict[str, Any]
    ) -> AsyncIterator[OllamaResponse]:
        """Generate streaming responses."""
        try:
            async with self._session.post(url, json=payload) as response:
                if response.status == 200:
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line)
                                yield OllamaResponse(
                                    model=data["model"],
                                    response=data.get("response", ""),
                                    done=data["done"],
                                    context=data.get("context", []),
                                )
                            except json.JSONDecodeError:
                                logger.error(
                                    f"Failed to parse streaming response: {line}"
                                )
                else:
                    error_text = await response.text()
                    yield OllamaResponse(
                        model=payload["model"],
                        response="",
                        done=True,
                        error=f"HTTP {response.status}: {error_text}",
                    )
        except Exception as e:
            yield OllamaResponse(
                model=payload["model"],
                response="",
                done=True,
                error=str(e),
            )

    async def code_generate(
        self,
        prompt: str,
        language: str = "python",
        model: str | None = None,
        temperature: float = 0.3,  # Lower temperature for code
    ) -> str:
        """Generate code with specialized prompt engineering."""
        # Enhance prompt for code generation
        enhanced_prompt = f"""You are a code generation assistant. Generate only valid {language} code.
Do not include any explanations, markdown formatting, or comments unless specifically requested.
Return only the raw code that can be directly executed.

Request: {prompt}

Code:"""

        response = await self.generate(
            prompt=enhanced_prompt,
            model=model,
            temperature=temperature,
        )

        if response.error:
            raise RuntimeError(f"Code generation failed: {response.error}")

        # Extract code from response
        code = response.response.strip()

        # Remove common markdown code block markers if present
        if code.startswith("```"):
            lines = code.split("\n")
            # Remove first and last lines if they're code block markers
            if lines[0].startswith("```") and lines[-1] == "```":
                code = "\n".join(lines[1:-1])

        return code

    async def analyze_error(
        self,
        error: str,
        context: str,
        model: str | None = None,
    ) -> dict[str, Any]:
        """Analyze error and suggest fixes."""
        prompt = f"""Analyze the following error and provide a structured fix suggestion.

Error: {error}

Context: {context}

Provide your analysis in JSON format with the following structure:
{{
    "error_type": "type of error",
    "root_cause": "root cause analysis",
    "fix_strategy": "recommended fix approach",
    "code_suggestion": "suggested code fix if applicable"
}}"""

        response = await self.generate(
            prompt=prompt,
            model=model,
            temperature=0.2,  # Low temperature for structured output
        )

        if response.error:
            raise RuntimeError(f"Error analysis failed: {response.error}")

        try:
            # Try to parse JSON from response
            return json.loads(response.response)
        except json.JSONDecodeError:
            # Fallback to simple dict if JSON parsing fails
            return {
                "error_type": "unknown",
                "root_cause": "Failed to parse analysis",
                "fix_strategy": "Manual intervention required",
                "code_suggestion": None,
            }

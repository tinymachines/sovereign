"""
Evolution engine for PROJECT SOVEREIGN.

Implements error-driven self-improvement through sandboxed execution,
error pattern recognition, and LLM-powered fix generation.
"""

import asyncio
import hashlib
import json
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from ..core.interpreter import SovereignInterpreter
from ..core.parser import ParseError
from ..vm.virtual_machine import SovereignVM, VMConfig
from .model_manager import ModelCapability, ModelManager
from .ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class ErrorCategory(Enum):
    """Categories of errors for pattern matching."""

    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    RESOURCE_LIMIT = "resource_limit"
    TYPE_ERROR = "type_error"
    STACK_ERROR = "stack_error"
    MEMORY_ERROR = "memory_error"
    UNKNOWN = "unknown"


@dataclass
class ErrorPattern:
    """Pattern for error recognition."""

    category: ErrorCategory
    pattern: str  # Error message pattern
    frequency: int = 1
    last_seen: datetime = field(default_factory=lambda: datetime.now(UTC))
    fix_success_rate: float = 0.0

    def matches(self, error_message: str) -> bool:
        """Check if error message matches this pattern."""
        return self.pattern.lower() in error_message.lower()

    def similarity_score(self, error_message: str) -> float:
        """Calculate similarity score between error and pattern."""
        # Simple implementation - can be enhanced with better algorithms
        if self.matches(error_message):
            return 1.0

        # Calculate word overlap
        pattern_words = set(self.pattern.lower().split())
        error_words = set(error_message.lower().split())

        if not pattern_words:
            return 0.0

        overlap = len(pattern_words.intersection(error_words))
        return overlap / len(pattern_words)


@dataclass
class EvolutionResult:
    """Result of an evolution attempt."""

    success: bool
    original_error: str
    suggested_fix: str | None = None
    fixed_code: str | None = None
    error_category: ErrorCategory = ErrorCategory.UNKNOWN
    confidence: float = 0.0
    execution_time: float = 0.0
    model_used: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvolutionHistory:
    """History of evolution attempts."""

    attempts: list[EvolutionResult] = field(default_factory=list)
    error_patterns: list[ErrorPattern] = field(default_factory=list)
    successful_fixes: int = 0
    total_attempts: int = 0

    def add_result(self, result: EvolutionResult) -> None:
        """Add evolution result to history."""
        self.attempts.append(result)
        self.total_attempts += 1

        if result.success:
            self.successful_fixes += 1

    def get_success_rate(self) -> float:
        """Calculate overall success rate."""
        if self.total_attempts == 0:
            return 0.0
        return self.successful_fixes / self.total_attempts

    def find_similar_errors(
        self, error_message: str, threshold: float = 0.5
    ) -> list[ErrorPattern]:
        """Find similar error patterns."""
        similar = []
        for pattern in self.error_patterns:
            score = pattern.similarity_score(error_message)
            if score >= threshold:
                similar.append(pattern)
        return sorted(
            similar, key=lambda p: p.similarity_score(error_message), reverse=True
        )


class EvolutionEngine:
    """Engine for error-driven code evolution."""

    def __init__(
        self,
        client: OllamaClient | None = None,
        model_manager: ModelManager | None = None,
        sandbox_config: VMConfig | None = None,
    ):
        self.client = client or OllamaClient()
        self.model_manager = model_manager or ModelManager(self.client)
        self.sandbox_config = sandbox_config or VMConfig(
            max_stack_size=100,
            max_memory_size=1000,
            max_execution_steps=1000,
            max_call_depth=20,
        )
        self.history = EvolutionHistory()
        self._pattern_cache: dict[str, ErrorPattern] = {}

    async def evolve(
        self,
        code: str,
        error_context: str,
        max_attempts: int = 3,
    ) -> EvolutionResult:
        """Evolve code based on error context."""
        start_time = asyncio.get_event_loop().time()

        # Categorize error
        category = self._categorize_error(error_context)

        # Find similar patterns
        similar_patterns = self.history.find_similar_errors(error_context)

        # Select appropriate model
        model_info = await self.model_manager.select_model(
            capabilities={
                ModelCapability.CODE_GENERATION,
                ModelCapability.ERROR_ANALYSIS,
            }
        )

        if not model_info:
            return EvolutionResult(
                success=False,
                original_error=error_context,
                error_category=category,
                execution_time=asyncio.get_event_loop().time() - start_time,
            )

        # Try to generate fix
        for attempt in range(max_attempts):
            try:
                # Analyze error and generate fix
                analysis = await self.client.analyze_error(
                    error=error_context,
                    context=code,
                    model=model_info.name,
                )

                # Generate fixed code
                fix_prompt = self._create_fix_prompt(
                    code=code,
                    error=error_context,
                    analysis=analysis,
                    similar_patterns=similar_patterns,
                )

                fixed_code = await self.client.code_generate(
                    prompt=fix_prompt,
                    language="assembly",
                    model=model_info.name,
                    temperature=0.3,
                )

                # Validate fix in sandbox
                is_valid = await self._validate_fix(fixed_code)

                if is_valid:
                    # Update patterns
                    self._update_patterns(error_context, category, success=True)

                    result = EvolutionResult(
                        success=True,
                        original_error=error_context,
                        suggested_fix=analysis.get("fix_strategy", ""),
                        fixed_code=fixed_code,
                        error_category=category,
                        confidence=0.8,  # Can be refined based on validation
                        execution_time=asyncio.get_event_loop().time() - start_time,
                        model_used=model_info.name,
                        metadata={"analysis": analysis, "attempt": attempt + 1},
                    )

                    self.history.add_result(result)
                    return result

            except Exception as e:
                logger.error(f"Evolution attempt {attempt + 1} failed: {e}")

        # Evolution failed
        self._update_patterns(error_context, category, success=False)

        result = EvolutionResult(
            success=False,
            original_error=error_context,
            error_category=category,
            execution_time=asyncio.get_event_loop().time() - start_time,
            model_used=model_info.name if model_info else "none",
        )

        self.history.add_result(result)
        return result

    def _categorize_error(self, error_message: str) -> ErrorCategory:
        """Categorize error based on message content."""
        error_lower = error_message.lower()

        if "syntax" in error_lower or "parse" in error_lower:
            return ErrorCategory.SYNTAX_ERROR
        if "stack" in error_lower:
            return ErrorCategory.STACK_ERROR
        if "memory" in error_lower:
            return ErrorCategory.MEMORY_ERROR
        if "type" in error_lower:
            return ErrorCategory.TYPE_ERROR
        if "limit" in error_lower or "exceeded" in error_lower:
            return ErrorCategory.RESOURCE_LIMIT
        if any(
            keyword in error_lower for keyword in ["runtime", "execution", "undefined"]
        ):
            return ErrorCategory.RUNTIME_ERROR
        return ErrorCategory.UNKNOWN

    def _create_fix_prompt(
        self,
        code: str,
        error: str,
        analysis: dict[str, Any],
        similar_patterns: list[ErrorPattern],
    ) -> str:
        """Create prompt for fix generation."""
        prompt_parts = [
            "Fix the following PROJECT SOVEREIGN assembly code based on the error analysis.",
            "",
            f"Original Code:\n{code}",
            "",
            f"Error: {error}",
            "",
            "Analysis:",
            f"- Error Type: {analysis.get('error_type', 'unknown')}",
            f"- Root Cause: {analysis.get('root_cause', 'unknown')}",
            f"- Fix Strategy: {analysis.get('fix_strategy', 'unknown')}",
        ]

        if similar_patterns:
            prompt_parts.extend(
                [
                    "",
                    "Similar errors have been seen before:",
                ]
            )
            for pattern in similar_patterns[:3]:  # Top 3 similar
                prompt_parts.append(
                    f"- {pattern.pattern} (success rate: {pattern.fix_success_rate:.1%})"
                )

        prompt_parts.extend(
            [
                "",
                "Generate the corrected PROJECT SOVEREIGN assembly code:",
            ]
        )

        return "\n".join(prompt_parts)

    async def _validate_fix(self, code: str) -> bool:
        """Validate fix in sandboxed environment."""
        try:
            # Create sandboxed VM
            vm = SovereignVM(self.sandbox_config)
            interpreter = SovereignInterpreter(vm=vm)

            # Try to parse and execute
            interpreter.run(code)

            # If we get here, the code executed without errors
            return True

        except (ParseError, RuntimeError, Exception) as e:
            logger.debug(f"Fix validation failed: {e}")
            return False

    def _update_patterns(
        self, error: str, category: ErrorCategory, success: bool
    ) -> None:
        """Update error patterns based on evolution result."""
        # Create pattern key
        pattern_key = hashlib.md5(error.encode()).hexdigest()[:8]

        if pattern_key in self._pattern_cache:
            pattern = self._pattern_cache[pattern_key]
            pattern.frequency += 1
            pattern.last_seen = datetime.now(UTC)

            # Update success rate
            total = pattern.frequency
            if success:
                pattern.fix_success_rate = (
                    pattern.fix_success_rate * (total - 1) + 1.0
                ) / total
            else:
                pattern.fix_success_rate = (
                    pattern.fix_success_rate * (total - 1)
                ) / total
        else:
            # Create new pattern
            pattern = ErrorPattern(
                category=category,
                pattern=error[:100],  # First 100 chars
                fix_success_rate=1.0 if success else 0.0,
            )
            self._pattern_cache[pattern_key] = pattern
            self.history.error_patterns.append(pattern)

    def get_evolution_stats(self) -> dict[str, Any]:
        """Get evolution statistics."""
        category_stats = {}
        for pattern in self.history.error_patterns:
            if pattern.category not in category_stats:
                category_stats[pattern.category.value] = {
                    "count": 0,
                    "success_rate": 0.0,
                }
            stats = category_stats[pattern.category.value]
            stats["count"] += pattern.frequency

        return {
            "total_attempts": self.history.total_attempts,
            "successful_fixes": self.history.successful_fixes,
            "success_rate": self.history.get_success_rate(),
            "unique_patterns": len(self.history.error_patterns),
            "category_breakdown": category_stats,
        }

    def export_patterns(self) -> str:
        """Export learned patterns as JSON."""
        patterns_data = []
        for pattern in self.history.error_patterns:
            patterns_data.append(
                {
                    "category": pattern.category.value,
                    "pattern": pattern.pattern,
                    "frequency": pattern.frequency,
                    "success_rate": pattern.fix_success_rate,
                    "last_seen": pattern.last_seen.isoformat(),
                }
            )

        return json.dumps(patterns_data, indent=2)

    def import_patterns(self, patterns_json: str) -> None:
        """Import patterns from JSON."""
        try:
            patterns_data = json.loads(patterns_json)
            for data in patterns_data:
                pattern = ErrorPattern(
                    category=ErrorCategory(data["category"]),
                    pattern=data["pattern"],
                    frequency=data["frequency"],
                    fix_success_rate=data["success_rate"],
                    last_seen=datetime.fromisoformat(data["last_seen"]),
                )
                pattern_key = hashlib.md5(pattern.pattern.encode()).hexdigest()[:8]
                self._pattern_cache[pattern_key] = pattern
                self.history.error_patterns.append(pattern)

            logger.info(f"Imported {len(patterns_data)} error patterns")
        except Exception as e:
            logger.error(f"Failed to import patterns: {e}")

"""
Integration tests for LLM-powered opcodes in PROJECT SOVEREIGN.
"""

from unittest.mock import MagicMock, patch

import pytest

from project_sovereign.agents.evolution_engine import EvolutionResult
from project_sovereign.agents.runtime_adapter import LLMRuntimeAdapter
from project_sovereign.core.interpreter import SovereignInterpreter


class TestLLMGenOpcode:
    """Test LLMGEN opcode integration."""

    def test_llmgen_basic(self):
        """Test basic LLMGEN functionality."""
        source = """
        LLMGEN "Generate a function that adds two numbers"
        HALT
        """

        # Mock the runtime adapter
        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.generate_code.return_value = "PUSH #10\nPUSH #20\nADD\nHALT"
            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            # Check that generated code is on stack
            state = interpreter.get_vm_state()
            assert len(state["data_stack"]) == 1
            assert "ADD" in state["data_stack"][0]

    def test_llmgen_error_handling(self):
        """Test LLMGEN error handling."""
        source = """
        LLMGEN "Generate invalid code"
        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.generate_code.side_effect = RuntimeError(
                "LLM service unavailable"
            )
            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            # Check error is on stack
            state = interpreter.get_vm_state()
            assert len(state["data_stack"]) == 1
            assert "LLMGEN_ERROR" in state["data_stack"][0]

    def test_llmgen_with_memory_storage(self):
        """Test LLMGEN with result storage."""
        source = """
        LLMGEN "Generate hello world"
        STORE "generated_code"
        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.generate_code.return_value = 'PUSH "Hello World"\nHALT'
            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            # Check code is stored in memory
            state = interpreter.get_vm_state()
            assert "generated_code" in state["memory"]
            assert "Hello World" in state["memory"]["generated_code"]


class TestEvolveOpcode:
    """Test EVOLVE opcode integration."""

    def test_evolve_basic(self):
        """Test basic EVOLVE functionality."""
        source = """
        PUSH "PUSH #42"
        EVOLVE "Stack underflow error"
        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.evolve_code.return_value = EvolutionResult(
                success=True,
                original_error="Stack underflow error",
                suggested_fix="Add POP after PUSH",
                fixed_code="PUSH #42\nPOP\nHALT",
                confidence=0.9,
                model_used="qwen2.5-coder",
            )
            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            # Check fixed code is on stack
            state = interpreter.get_vm_state()
            assert len(state["data_stack"]) == 2  # Original code + fixed code
            assert "POP" in state["data_stack"][-1]

            # Check evolution metadata
            assert "_last_evolution" in state["memory"]
            assert state["memory"]["_last_evolution"]["success"] is True
            assert state["memory"]["_last_evolution"]["confidence"] == 0.9

    def test_evolve_failure(self):
        """Test EVOLVE failure handling."""
        source = """
        PUSH "Invalid code"
        EVOLVE "Complex error"
        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.evolve_code.return_value = EvolutionResult(
                success=False,
                original_error="Complex error",
                error_category="unknown",
            )
            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            # Check failure message on stack
            state = interpreter.get_vm_state()
            assert "EVOLVE_FAILED" in state["data_stack"][-1]

            # Check failure metadata
            assert state["memory"]["_last_evolution"]["success"] is False

    def test_evolve_empty_stack(self):
        """Test EVOLVE with empty stack."""
        source = """
        EVOLVE "No code context"
        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.evolve_code.return_value = EvolutionResult(
                success=False,
                original_error="No code context",
            )
            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            # Should handle gracefully
            state = interpreter.get_vm_state()
            assert len(state["data_stack"]) == 1
            assert "EVOLVE_FAILED" in state["data_stack"][0]


class TestLLMIntegrationScenarios:
    """Test complete LLM integration scenarios."""

    def test_code_generation_and_evolution(self):
        """Test generating code and then evolving it."""
        source = """
        LLMGEN "Create a loop that counts to 5"
        DUP
        STORE "original_code"
        EVOLVE "Loop never terminates"
        STORE "evolved_code"
        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)

            # First call generates buggy code
            mock_runtime.generate_code.return_value = """
            PUSH #0
            loop:
            PUSH #1
            ADD
            JMP loop
            """

            # Second call evolves to fix it
            mock_runtime.evolve_code.return_value = EvolutionResult(
                success=True,
                original_error="Loop never terminates",
                fixed_code="""
                PUSH #0
                loop:
                PUSH #1
                ADD
                DUP
                PUSH #5
                SUB
                JZ end
                JMP loop
                end:
                HALT
                """,
                confidence=0.85,
                model_used="qwen2.5-coder",
            )

            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            state = interpreter.get_vm_state()

            # Check both versions are stored
            assert "original_code" in state["memory"]
            assert "evolved_code" in state["memory"]
            assert "loop:" in state["memory"]["original_code"]
            assert "JZ end" in state["memory"]["evolved_code"]

    def test_error_driven_evolution_workflow(self):
        """Test complete error-driven evolution workflow."""
        # First, run code that will fail
        buggy_code = "PUSH #10\nPUSH #0\nDIV\nHALT"

        interpreter = SovereignInterpreter()

        # This should raise a division by zero error
        with pytest.raises(RuntimeError, match="Division by zero"):
            interpreter.run(buggy_code)

        # Now use EVOLVE to fix it
        evolution_code = 'PUSH "BUGGY_CODE"\nEVOLVE "Division by zero"\nHALT'

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)
            mock_runtime.evolve_code.return_value = EvolutionResult(
                success=True,
                original_error="Division by zero",
                suggested_fix="Check divisor before division",
                fixed_code="""
                PUSH #10
                PUSH #0
                DUP
                JZ skip_div
                DIV
                JMP end
                skip_div:
                DROP
                DROP
                PUSH #0
                end:
                HALT
                """,
                confidence=0.95,
                model_used="qwen2.5-coder",
            )
            mock_get_runtime.return_value = mock_runtime

            # Reset interpreter for clean state
            interpreter.reset()
            interpreter.run(evolution_code)

            state = interpreter.get_vm_state()

            # Check evolution succeeded
            assert "_last_evolution" in state["memory"]
            assert state["memory"]["_last_evolution"]["success"] is True
            assert "skip_div" in state["data_stack"][-1]

    def test_chained_llm_operations(self):
        """Test chaining multiple LLM operations."""
        source = """
        LLMGEN "Generate a factorial function"
        DUP
        STORE "v1"

        LLMGEN "Generate an optimized version of factorial"
        DUP
        STORE "v2"

        PUSH "Stack overflow in recursive factorial"
        EVOLVE "Stack overflow in recursive factorial"
        STORE "v3"

        HALT
        """

        with patch(
            "project_sovereign.agents.runtime_adapter.get_llm_runtime"
        ) as mock_get_runtime:
            mock_runtime = MagicMock(spec=LLMRuntimeAdapter)

            # Mock different responses
            responses = [
                # First factorial - recursive
                """
                factorial:
                DUP
                PUSH #1
                JZ base_case
                DUP
                PUSH #1
                SUB
                CALL factorial
                MUL
                RET
                base_case:
                DROP
                PUSH #1
                RET
                """,
                # Second factorial - iterative
                """
                factorial_iter:
                PUSH #1
                SWAP
                loop:
                DUP
                JZ done
                DUP
                ROT
                MUL
                SWAP
                PUSH #1
                SUB
                JMP loop
                done:
                DROP
                RET
                """,
            ]

            mock_runtime.generate_code.side_effect = responses

            # Evolution response
            mock_runtime.evolve_code.return_value = EvolutionResult(
                success=True,
                original_error="Stack overflow in recursive factorial",
                fixed_code="Use iterative approach instead",
                confidence=0.9,
                model_used="qwen2.5-coder",
            )

            mock_get_runtime.return_value = mock_runtime

            interpreter = SovereignInterpreter()
            interpreter.run(source)

            state = interpreter.get_vm_state()

            # Check all versions are stored
            assert all(key in state["memory"] for key in ["v1", "v2", "v3"])

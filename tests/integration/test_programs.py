"""
Integration tests for complete PROJECT SOVEREIGN programs.
"""

import pytest
from project_sovereign.core.interpreter import SovereignInterpreter


class TestPrograms:
    """Test complete program execution."""

    def test_simple_arithmetic(self, interpreter):
        """Test basic arithmetic program."""
        program = """
        PUSH #10
        PUSH #32
        ADD
        HALT
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        assert state["data_stack"] == [42]

    def test_stack_manipulation(self, interpreter):
        """Test stack manipulation operations."""
        program = """
        PUSH #1
        PUSH #2
        PUSH #3
        SWAP
        DUP
        HALT
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        assert state["data_stack"] == [1, 3, 2, 2]

    def test_memory_operations(self, interpreter):
        """Test memory load/store operations."""
        program = """
        PUSH #42
        STORE @100
        PUSH #0
        LOAD @100
        HALT
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        assert state["data_stack"] == [0, 42]
        assert state["memory"]["100"] == 42

    def test_control_flow_jump(self, interpreter):
        """Test jump operations."""
        program = """
        PUSH #1
        JMP end
        PUSH #2
        end:
        PUSH #3
        HALT
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        # Should skip PUSH #2
        assert state["data_stack"] == [1, 3]

    def test_function_calls(self, interpreter):
        """Test CALL and RET operations."""
        program = """
        PUSH #10
        CALL function
        PUSH #30
        HALT
        
        function:
        PUSH #20
        RET
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        assert state["data_stack"] == [10, 20, 30]

    def test_conditional_jumps(self, interpreter):
        """Test JZ and JNZ operations."""
        program = """
        PUSH #0
        JZ zero_branch
        PUSH #99
        JMP end
        
        zero_branch:
        PUSH #42
        
        end:
        HALT
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        assert state["data_stack"] == [0, 42]

    def test_complex_arithmetic(self, interpreter):
        """Test complex arithmetic expressions."""
        program = """
        ; Calculate (10 + 5) * 2 - 3
        PUSH #10
        PUSH #5
        ADD
        PUSH #2
        MUL
        PUSH #3
        SUB
        HALT
        """

        interpreter.run(program)
        state = interpreter.get_vm_state()
        assert state["data_stack"] == [27]  # (10 + 5) * 2 - 3 = 27


@pytest.mark.parametrize(
    "program,expected_stack",
    [
        # Test bitwise operations
        (
            """
    PUSH #12
    PUSH #10
    AND
    HALT
    """,
            [8],
        ),  # 12 & 10 = 8
        # Test division
        (
            """
    PUSH #20
    PUSH #4
    DIV
    HALT
    """,
            [5],
        ),  # 20 / 4 = 5
        # Test stack clear
        (
            """
    PUSH #1
    PUSH #2
    PUSH #3
    CLEAR
    PUSH #42
    HALT
    """,
            [42],
        ),
    ],
)
def test_parametrized_programs(interpreter, program, expected_stack):
    """Parametrized tests for various programs."""
    interpreter.run(program)
    state = interpreter.get_vm_state()
    assert state["data_stack"] == expected_stack

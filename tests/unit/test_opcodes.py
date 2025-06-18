"""
Tests for PROJECT SOVEREIGN opcodes.
"""

import pytest
from project_sovereign.core.opcodes import (
    OpCodeRegistry,
    OpCodeCategory,
    ExecutionContext,
    PushOp,
    PopOp,
    AddOp,
    SubOp,
    DupOp,
    SwapOp,
)


class TestOpcodes:
    """Test cases for individual opcodes."""

    def test_push_op(self):
        """Test PUSH operation."""
        op = PushOp()
        context = ExecutionContext(
            data_stack=[], control_stack=[], memory={}, program_counter=0, registers={}
        )

        op.execute(context, 42)
        assert context.data_stack == [42]

        op.execute(context, 100)
        assert context.data_stack == [42, 100]

    def test_pop_op(self):
        """Test POP operation."""
        op = PopOp()
        context = ExecutionContext(
            data_stack=[1, 2, 3],
            control_stack=[],
            memory={},
            program_counter=0,
            registers={},
        )

        result = op.execute(context)
        assert result == 3
        assert context.data_stack == [1, 2]

    def test_pop_empty_stack(self):
        """Test POP on empty stack raises error."""
        op = PopOp()
        context = ExecutionContext(
            data_stack=[], control_stack=[], memory={}, program_counter=0, registers={}
        )

        with pytest.raises(RuntimeError, match="Data stack underflow"):
            op.execute(context)

    def test_add_op(self):
        """Test ADD operation."""
        op = AddOp()
        context = ExecutionContext(
            data_stack=[10, 32],
            control_stack=[],
            memory={},
            program_counter=0,
            registers={},
        )

        op.execute(context)
        assert context.data_stack == [42]

    def test_sub_op(self):
        """Test SUB operation."""
        op = SubOp()
        context = ExecutionContext(
            data_stack=[50, 8],
            control_stack=[],
            memory={},
            program_counter=0,
            registers={},
        )

        op.execute(context)
        assert context.data_stack == [42]

    def test_dup_op(self):
        """Test DUP operation."""
        op = DupOp()
        context = ExecutionContext(
            data_stack=[42],
            control_stack=[],
            memory={},
            program_counter=0,
            registers={},
        )

        op.execute(context)
        assert context.data_stack == [42, 42]

    def test_swap_op(self):
        """Test SWAP operation."""
        op = SwapOp()
        context = ExecutionContext(
            data_stack=[1, 2],
            control_stack=[],
            memory={},
            program_counter=0,
            registers={},
        )

        op.execute(context)
        assert context.data_stack == [2, 1]


class TestOpCodeRegistry:
    """Test cases for opcode registry."""

    def test_registry_initialization(self, opcode_registry):
        """Test registry initializes with all opcodes."""
        # Should have all 32 opcodes
        all_opcodes = opcode_registry.list_opcodes()
        assert len(all_opcodes) == 32

    def test_get_opcode(self, opcode_registry):
        """Test retrieving opcodes by name."""
        push_op = opcode_registry.get_opcode("PUSH")
        assert push_op is not None
        assert push_op.name == "PUSH"

        # Case insensitive
        push_op_lower = opcode_registry.get_opcode("push")
        assert push_op_lower is not None
        assert push_op_lower.name == "PUSH"

    def test_list_by_category(self, opcode_registry):
        """Test listing opcodes by category."""
        stack_ops = opcode_registry.list_opcodes(OpCodeCategory.STACK)
        assert len(stack_ops) == 8
        assert all(op.category == OpCodeCategory.STACK for op in stack_ops)

        arithmetic_ops = opcode_registry.list_opcodes(OpCodeCategory.ARITHMETIC)
        assert len(arithmetic_ops) == 8
        assert all(op.category == OpCodeCategory.ARITHMETIC for op in arithmetic_ops)

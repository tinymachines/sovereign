"""
Tests for PROJECT SOVEREIGN virtual machine.
"""

import pytest
from project_sovereign.vm.virtual_machine import SovereignVM, VMState
from project_sovereign.core.ast_nodes import Program, Instruction, Immediate


class TestSovereignVM:
    """Test cases for the virtual machine."""

    def test_vm_initialization(self, vm):
        """Test VM initializes correctly."""
        assert len(vm.state.data_stack) == 0
        assert len(vm.state.control_stack) == 0
        assert vm.state.program_counter == 0
        assert vm.state.running is False

    def test_stack_operations(self, vm):
        """Test basic stack operations."""
        # Test push
        vm.push_data(42)
        assert vm.peek_data() == 42
        assert len(vm.state.data_stack) == 1

        # Test pop
        value = vm.pop_data()
        assert value == 42
        assert len(vm.state.data_stack) == 0

    def test_stack_underflow_error(self, vm):
        """Test stack underflow raises error."""
        with pytest.raises(RuntimeError, match="Data stack underflow"):
            vm.pop_data()

        with pytest.raises(RuntimeError, match="Data stack empty"):
            vm.peek_data()

    def test_memory_operations(self, vm):
        """Test memory get/set operations."""
        vm.set_memory("test_addr", "test_value")
        assert vm.get_memory("test_addr") == "test_value"
        assert vm.get_memory("nonexistent") is None

    def test_vm_reset(self, vm):
        """Test VM reset functionality."""
        # Modify state
        vm.push_data(42)
        vm.set_memory("addr", "value")
        vm.state.program_counter = 10

        # Reset and verify
        vm.reset()
        assert len(vm.state.data_stack) == 0
        assert len(vm.state.memory) == 0
        assert vm.state.program_counter == 0

    def test_dump_state(self, vm):
        """Test state dumping."""
        vm.push_data(42)
        vm.set_memory("addr", "value")

        state_dump = vm.dump_state()
        assert state_dump["data_stack"] == [42]
        assert state_dump["memory"]["addr"] == "value"
        assert "program_counter" in state_dump

    def test_halt_operation(self, vm):
        """Test halt stops execution."""
        vm.state.running = True
        vm.halt()
        assert vm.state.running is False


@pytest.mark.asyncio
async def test_error_handling(vm):
    """Test error handling in VM."""
    # This would test the error handling and evolution triggering
    # Implementation depends on the actual VM execution logic
    pass

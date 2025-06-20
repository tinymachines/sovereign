"""
Tests for memory limits and bounds checking in PROJECT SOVEREIGN VM.
"""

import pytest

from project_sovereign.core.ast_nodes import Immediate, Instruction, Program
from project_sovereign.vm.virtual_machine import SovereignVM, VMConfig


class TestMemoryLimits:
    """Test memory limits and bounds checking."""

    def test_vm_config_defaults(self):
        """Test default VM configuration values."""
        config = VMConfig()
        assert config.max_stack_size == 1000
        assert config.max_memory_size == 10000
        assert config.max_execution_steps == 100000
        assert config.max_call_depth == 100

    def test_vm_config_custom(self):
        """Test custom VM configuration."""
        config = VMConfig(
            max_stack_size=100,
            max_memory_size=1000,
            max_execution_steps=500,
            max_call_depth=10,
        )
        vm = SovereignVM(config)
        assert vm.config.max_stack_size == 100
        assert vm.config.max_memory_size == 1000
        assert vm.config.max_execution_steps == 500
        assert vm.config.max_call_depth == 10

    def test_data_stack_overflow(self):
        """Test data stack overflow protection."""
        config = VMConfig(max_stack_size=3)
        vm = SovereignVM(config)

        # Should work for 3 pushes
        vm.push_data(1)
        vm.push_data(2)
        vm.push_data(3)

        # 4th push should fail
        with pytest.raises(RuntimeError, match="Data stack push would exceed maximum"):
            vm.push_data(4)

    def test_control_stack_overflow(self):
        """Test control stack overflow protection."""
        config = VMConfig(max_stack_size=2, max_call_depth=2)
        vm = SovereignVM(config)

        # Should work for 2 pushes
        vm.push_control(100)
        vm.push_control(200)

        # 3rd push should fail
        with pytest.raises(
            RuntimeError, match="Control stack push would exceed maximum"
        ):
            vm.push_control(300)

    def test_call_depth_limit(self):
        """Test call depth limit."""
        config = VMConfig(max_call_depth=2)
        vm = SovereignVM(config)

        # Should work for 2 calls
        vm.push_control(100)
        vm.push_control(200)

        # 3rd call should fail due to call depth
        with pytest.raises(RuntimeError, match="Call depth would exceed maximum"):
            vm.push_control(300)

    def test_memory_usage_tracking(self):
        """Test memory usage tracking and limits."""
        config = VMConfig(max_memory_size=200)  # Small memory limit
        vm = SovereignVM(config)

        # Add some values to track usage
        vm.set_memory("addr1", 42)  # 8 bytes
        vm.set_memory("addr2", "small")  # 64 bytes

        assert vm.state.memory_usage == 72  # 8 + 64

        # Update existing memory should adjust usage
        vm.set_memory("addr1", "larger_string")  # 64 bytes (net +56)
        assert vm.state.memory_usage == 128  # 64 + 64

        # Adding more should eventually fail
        with pytest.raises(RuntimeError, match="Memory usage exceeded maximum"):
            # Try to add enough to exceed limit
            vm.set_memory("addr3", "another_long_string")
            vm.set_memory("addr4", "yet_another_string")

    def test_execution_step_limit(self):
        """Test execution step limit."""
        config = VMConfig(max_execution_steps=5)
        vm = SovereignVM(config)

        # Create a program with more than 5 instructions
        instructions = [
            Instruction("PUSH", [Immediate(1)]),
            Instruction("PUSH", [Immediate(2)]),
            Instruction("PUSH", [Immediate(3)]),
            Instruction("PUSH", [Immediate(4)]),
            Instruction("PUSH", [Immediate(5)]),
            Instruction("PUSH", [Immediate(6)]),  # This should fail
            Instruction("HALT", []),
        ]
        program = Program(instructions=instructions, labels={})

        # Execution should fail due to step limit
        with pytest.raises(RuntimeError, match="Execution exceeded maximum steps"):
            vm.execute(program)

    def test_memory_cleanup_on_pop(self):
        """Test memory usage decreases when popping values."""
        config = VMConfig()
        vm = SovereignVM(config)

        # Push values and track memory
        vm.push_data("test_string")
        vm.push_data(42)
        initial_usage = vm.state.memory_usage
        assert initial_usage > 0

        # Pop values and check memory decreases
        vm.pop_data()  # Pop integer (8 bytes)
        assert vm.state.memory_usage == initial_usage - 8

        vm.pop_data()  # Pop string (64 bytes)
        assert vm.state.memory_usage == initial_usage - 72

    def test_dump_state_includes_limits(self):
        """Test that dump_state includes memory limit information."""
        config = VMConfig(max_stack_size=100, max_memory_size=2000)
        vm = SovereignVM(config)

        vm.push_data(42)
        vm.set_memory("test", "value")

        state = vm.dump_state()

        assert "execution_steps" in state
        assert "memory_usage" in state
        assert "config" in state
        assert state["config"]["max_stack_size"] == 100
        assert state["config"]["max_memory_size"] == 2000
        assert state["memory_usage"] > 0

    def test_reset_clears_usage_counters(self):
        """Test that reset clears usage counters."""
        vm = SovereignVM()

        # Add some usage
        vm.push_data(42)
        vm.set_memory("test", "value")
        vm.state.execution_steps = 10

        assert vm.state.memory_usage > 0
        assert vm.state.execution_steps > 0

        # Reset should clear everything
        vm.reset()
        assert vm.state.memory_usage == 0
        assert vm.state.execution_steps == 0
        assert len(vm.state.data_stack) == 0
        assert len(vm.state.memory) == 0

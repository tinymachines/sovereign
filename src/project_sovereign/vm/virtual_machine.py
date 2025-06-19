"""
Virtual Machine implementation for PROJECT SOVEREIGN.

Implements stack-based execution model with dual stacks,
memory management, and instruction dispatch.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from ..core.ast_nodes import (
    Address,
    Immediate,
    Instruction,
    LabelRef,
    Program,
    Register,
    StringLiteral,
)
from ..core.opcodes import ExecutionContext, OpCodeRegistry


@dataclass
class VMConfig:
    """Configuration for the virtual machine."""

    max_stack_size: int = 1000
    max_memory_size: int = 10000
    max_execution_steps: int = 100000
    max_call_depth: int = 100


@dataclass
class VMState:
    """Complete state of the virtual machine."""

    data_stack: list[Any] = field(default_factory=list)
    control_stack: list[Any] = field(default_factory=list)
    memory: dict[str, Any] = field(default_factory=dict)
    registers: dict[str, Any] = field(default_factory=dict)
    program_counter: int = 0
    running: bool = False
    error_state: str | None = None
    execution_steps: int = 0
    memory_usage: int = 0

    def to_execution_context(self) -> ExecutionContext:
        """Convert to execution context for op-codes."""
        return ExecutionContext(
            data_stack=self.data_stack,
            control_stack=self.control_stack,
            memory=self.memory,
            program_counter=self.program_counter,
            registers=self.registers,
            error_state=self.error_state,
        )


class SovereignVM:
    """
    Virtual Machine for PROJECT SOVEREIGN.

    Implements stack-based execution with error-driven evolution
    and LLM integration capabilities.
    """

    def __init__(self, config: VMConfig | None = None):
        self.config = config or VMConfig()
        self.state = VMState()
        self.opcode_registry = OpCodeRegistry()
        self.logger = logging.getLogger(__name__)
        self.evolution_history: list[str] = []
        self.program: Program | None = None

    def load_program(self, program: Program) -> None:
        """Load program into VM memory."""
        self.program = program
        self.state.program_counter = 0
        self.state.running = False
        self.state.error_state = None

        # Validate all opcodes exist
        for instruction in program.instructions:
            if not self.opcode_registry.get_opcode(instruction.opcode):
                raise ValueError(f"Unknown opcode: {instruction.opcode}")

    def execute(self, program: Program) -> None:
        """Execute a complete program."""
        self.load_program(program)
        self.state.running = True
        self.state.program_counter = 0

        try:
            while self.state.running and self.state.program_counter < len(
                program.instructions
            ):
                # Check execution limits
                self._check_execution_limit()
                
                # Check for HALT before executing
                instruction = program.instructions[self.state.program_counter]
                if instruction.opcode == "HALT":
                    self.state.running = False
                    break

                self.execute_instruction(instruction)
                self.state.program_counter += 1

        except Exception as e:
            self.handle_runtime_error(e)

    def execute_instruction(self, instruction: Instruction) -> None:
        """Execute a single instruction."""
        self.logger.debug(f"Executing: {instruction}")

        # Get opcode implementation
        opcode = self.opcode_registry.get_opcode(instruction.opcode)
        if not opcode:
            raise RuntimeError(f"Unknown opcode: {instruction.opcode}")

        # Convert operands to appropriate values
        args = []
        for operand in instruction.operands:
            if isinstance(operand, Immediate):
                args.append(operand.value)
            elif isinstance(operand, Register):
                # Get value from register
                reg_name = str(operand)
                args.append(self.state.registers.get(reg_name, 0))
            elif isinstance(operand, Address | StringLiteral):
                args.append(operand.value)
            elif isinstance(operand, LabelRef):
                # Resolve label to instruction index
                if self.program and operand.name in self.program.labels:
                    args.append(self.program.labels[operand.name])
                else:
                    raise RuntimeError(f"Undefined label: {operand.name}")
            else:
                args.append(operand)

        # Validate arguments
        if not opcode.validate_args(*args):
            raise RuntimeError(f"Invalid arguments for {instruction.opcode}: {args}")

        # Execute opcode with current context
        context = self.state.to_execution_context()
        opcode.execute(context, *args)

        # Update program counter if it was modified by the instruction
        if context.program_counter != self.state.program_counter:
            self.state.program_counter = context.program_counter

    def handle_runtime_error(self, error: Exception) -> None:
        """Handle runtime errors with potential evolution."""
        self.logger.error(f"Runtime error: {error}")
        self.state.error_state = str(error)
        self.state.running = False

        # Re-raise the error for now
        # TODO: Implement error-driven evolution
        raise error

    def _check_stack_overflow(self, stack: list[Any], operation: str) -> None:
        """Check if stack operation would cause overflow."""
        if len(stack) >= self.config.max_stack_size:
            raise RuntimeError(
                f"{operation} would exceed maximum stack size of {self.config.max_stack_size}"
            )

    def _check_execution_limit(self) -> None:
        """Check if execution step limit would be exceeded."""
        self.state.execution_steps += 1
        if self.state.execution_steps >= self.config.max_execution_steps:
            raise RuntimeError(
                f"Execution exceeded maximum steps of {self.config.max_execution_steps}"
            )

    def _check_call_depth(self) -> None:
        """Check if call stack depth would be exceeded."""
        if len(self.state.control_stack) >= self.config.max_call_depth:
            raise RuntimeError(
                f"Call depth would exceed maximum of {self.config.max_call_depth}"
            )

    def _update_memory_usage(self, delta: int = 0) -> None:
        """Update memory usage tracking."""
        self.state.memory_usage += delta
        if self.state.memory_usage > self.config.max_memory_size:
            raise RuntimeError(
                f"Memory usage exceeded maximum of {self.config.max_memory_size} bytes"
            )

    def push_data(self, value: Any) -> None:
        """Push value onto data stack."""
        self._check_stack_overflow(self.state.data_stack, "Data stack push")
        self.state.data_stack.append(value)
        # Estimate memory usage (simplified)
        self._update_memory_usage(64 if isinstance(value, str) else 8)

    def pop_data(self) -> Any:
        """Pop value from data stack."""
        if not self.state.data_stack:
            raise RuntimeError("Data stack underflow")
        value = self.state.data_stack.pop()
        # Update memory usage
        self._update_memory_usage(-64 if isinstance(value, str) else -8)
        return value

    def peek_data(self) -> Any:
        """Peek at top of data stack without popping."""
        if not self.state.data_stack:
            raise RuntimeError("Data stack empty")
        return self.state.data_stack[-1]

    def push_control(self, value: Any) -> None:
        """Push value onto control stack."""
        self._check_stack_overflow(self.state.control_stack, "Control stack push")
        self._check_call_depth()
        self.state.control_stack.append(value)
        self._update_memory_usage(8)

    def pop_control(self) -> Any:
        """Pop value from control stack."""
        if not self.state.control_stack:
            raise RuntimeError("Control stack underflow")
        value = self.state.control_stack.pop()
        self._update_memory_usage(-8)
        return value

    def get_memory(self, address: str) -> Any:
        """Get value from memory."""
        return self.state.memory.get(address)

    def set_memory(self, address: str, value: Any) -> None:
        """Set value in memory."""
        # Calculate memory delta
        old_value = self.state.memory.get(address)
        old_size = 64 if isinstance(old_value, str) else 8 if old_value is not None else 0
        new_size = 64 if isinstance(value, str) else 8
        delta = new_size - old_size

        self._update_memory_usage(delta)
        self.state.memory[address] = value

    def halt(self) -> None:
        """Halt execution."""
        self.state.running = False

    def reset(self) -> None:
        """Reset VM to initial state."""
        self.state = VMState()
        self.program = None
        self.evolution_history.clear()

    def dump_state(self) -> dict[str, Any]:
        """Dump current VM state for debugging."""
        return {
            "data_stack": self.state.data_stack.copy(),
            "control_stack": self.state.control_stack.copy(),
            "memory": self.state.memory.copy(),
            "registers": self.state.registers.copy(),
            "program_counter": self.state.program_counter,
            "running": self.state.running,
            "error_state": self.state.error_state,
            "execution_steps": self.state.execution_steps,
            "memory_usage": self.state.memory_usage,
            "config": {
                "max_stack_size": self.config.max_stack_size,
                "max_memory_size": self.config.max_memory_size,
                "max_execution_steps": self.config.max_execution_steps,
                "max_call_depth": self.config.max_call_depth,
            },
        }

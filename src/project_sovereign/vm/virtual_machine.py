"""
Virtual Machine implementation for PROJECT SOVEREIGN.

Implements stack-based execution model with dual stacks,
memory management, and instruction dispatch.
"""

import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from ..core.opcodes import OpCodeRegistry, ExecutionContext, OpCode
from ..core.ast_nodes import (
    Program,
    Instruction,
    Immediate,
    Register,
    Address,
    StringLiteral,
    LabelRef,
)


@dataclass
class VMState:
    """Complete state of the virtual machine."""

    data_stack: List[Any] = field(default_factory=list)
    control_stack: List[Any] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    registers: Dict[str, Any] = field(default_factory=dict)
    program_counter: int = 0
    running: bool = False
    error_state: Optional[str] = None

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

    def __init__(self):
        self.state = VMState()
        self.opcode_registry = OpCodeRegistry()
        self.logger = logging.getLogger(__name__)
        self.evolution_history: List[str] = []
        self.program: Optional[Program] = None

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
            elif isinstance(operand, Address):
                args.append(operand.value)
            elif isinstance(operand, StringLiteral):
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

    def push_data(self, value: Any) -> None:
        """Push value onto data stack."""
        self.state.data_stack.append(value)

    def pop_data(self) -> Any:
        """Pop value from data stack."""
        if not self.state.data_stack:
            raise RuntimeError("Data stack underflow")
        return self.state.data_stack.pop()

    def peek_data(self) -> Any:
        """Peek at top of data stack without popping."""
        if not self.state.data_stack:
            raise RuntimeError("Data stack empty")
        return self.state.data_stack[-1]

    def push_control(self, value: Any) -> None:
        """Push value onto control stack."""
        self.state.control_stack.append(value)

    def pop_control(self) -> Any:
        """Pop value from control stack."""
        if not self.state.control_stack:
            raise RuntimeError("Control stack underflow")
        return self.state.control_stack.pop()

    def get_memory(self, address: str) -> Any:
        """Get value from memory."""
        return self.state.memory.get(address)

    def set_memory(self, address: str, value: Any) -> None:
        """Set value in memory."""
        self.state.memory[address] = value

    def halt(self) -> None:
        """Halt execution."""
        self.state.running = False

    def reset(self) -> None:
        """Reset VM to initial state."""
        self.state = VMState()
        self.program = None

    def dump_state(self) -> Dict[str, Any]:
        """Dump current VM state for debugging."""
        return {
            "data_stack": self.state.data_stack.copy(),
            "control_stack": self.state.control_stack.copy(),
            "memory": self.state.memory.copy(),
            "registers": self.state.registers.copy(),
            "program_counter": self.state.program_counter,
            "running": self.state.running,
            "error_state": self.state.error_state,
        }

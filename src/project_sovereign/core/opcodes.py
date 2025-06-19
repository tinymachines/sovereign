"""
Core op-code definitions and registry for PROJECT SOVEREIGN.

Defines the 32 base instructions across 4 categories:
- Stack Operations (8)
- Arithmetic/Logic (8)
- Control Flow (8)
- Memory/IO (8)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


class OpCodeCategory(Enum):
    """Categories of op-codes in PROJECT SOVEREIGN."""

    STACK = "stack"
    ARITHMETIC = "arithmetic"
    CONTROL = "control"
    MEMORY = "memory"


@dataclass
class ExecutionContext:
    """Context for op-code execution."""

    data_stack: list[Any]
    control_stack: list[Any]
    memory: dict[str, Any]
    program_counter: int
    registers: dict[str, Any]
    error_state: str | None = None


class OpCode(ABC):
    """Base class for all PROJECT SOVEREIGN op-codes."""

    def __init__(self, name: str, category: OpCodeCategory, description: str):
        self.name = name
        self.category = category
        self.description = description

    @abstractmethod
    def execute(self, context: ExecutionContext, *args: Any) -> None:
        """Execute the op-code with given context and arguments."""
        pass

    @abstractmethod
    def validate_args(self, *args: Any) -> bool:
        """Validate arguments before execution."""
        pass


# Stack Operations (8 ops)
class PushOp(OpCode):
    """Load value onto data stack."""

    def __init__(self):
        super().__init__("PUSH", OpCodeCategory.STACK, "Load value onto data stack")

    def execute(self, context: ExecutionContext, value: Any) -> None:
        """Push value onto data stack."""
        context.data_stack.append(value)

    def validate_args(self, *args: Any) -> bool:
        """Validate push arguments."""
        return len(args) == 1


class PopOp(OpCode):
    """Remove top stack value."""

    def __init__(self):
        super().__init__("POP", OpCodeCategory.STACK, "Remove top stack value")

    def execute(self, context: ExecutionContext) -> Any:
        """Pop value from data stack."""
        if not context.data_stack:
            raise RuntimeError("Data stack underflow")
        return context.data_stack.pop()

    def validate_args(self, *args: Any) -> bool:
        """Validate pop arguments."""
        return len(args) == 0


class DupOp(OpCode):
    """Duplicate stack top."""

    def __init__(self):
        super().__init__("DUP", OpCodeCategory.STACK, "Duplicate stack top")

    def execute(self, context: ExecutionContext) -> None:
        """Duplicate top stack value."""
        if not context.data_stack:
            raise RuntimeError("Data stack empty")
        context.data_stack.append(context.data_stack[-1])

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class SwapOp(OpCode):
    """Swap top two stack values."""

    def __init__(self):
        super().__init__("SWAP", OpCodeCategory.STACK, "Swap top two values")

    def execute(self, context: ExecutionContext) -> None:
        """Swap top two values on stack."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack to swap")
        context.data_stack[-1], context.data_stack[-2] = (
            context.data_stack[-2],
            context.data_stack[-1],
        )

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class RotOp(OpCode):
    """Rotate top three stack values."""

    def __init__(self):
        super().__init__("ROT", OpCodeCategory.STACK, "Rotate top three values")

    def execute(self, context: ExecutionContext) -> None:
        """Rotate top three values: abc -> bca."""
        if len(context.data_stack) < 3:
            raise RuntimeError("Not enough values on stack to rotate")
        a = context.data_stack.pop()
        b = context.data_stack.pop()
        c = context.data_stack.pop()
        context.data_stack.extend([a, c, b])

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class OverOp(OpCode):
    """Copy second stack value over top."""

    def __init__(self):
        super().__init__("OVER", OpCodeCategory.STACK, "Copy second value over top")

    def execute(self, context: ExecutionContext) -> None:
        """Copy second value over top: ab -> aba."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for over")
        context.data_stack.append(context.data_stack[-2])

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class DropOp(OpCode):
    """Remove top stack value without returning."""

    def __init__(self):
        super().__init__("DROP", OpCodeCategory.STACK, "Remove top value")

    def execute(self, context: ExecutionContext) -> None:
        """Drop top value from stack."""
        if not context.data_stack:
            raise RuntimeError("Data stack empty")
        context.data_stack.pop()

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class ClearOp(OpCode):
    """Clear entire data stack."""

    def __init__(self):
        super().__init__("CLEAR", OpCodeCategory.STACK, "Clear data stack")

    def execute(self, context: ExecutionContext) -> None:
        """Clear all values from data stack."""
        context.data_stack.clear()

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


# Arithmetic Operations (8 ops)
class AddOp(OpCode):
    """Add top two stack values."""

    def __init__(self):
        super().__init__("ADD", OpCodeCategory.ARITHMETIC, "Add top two stack values")

    def execute(self, context: ExecutionContext) -> None:
        """Add top two values on stack."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for addition")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        context.data_stack.append(a + b)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class SubOp(OpCode):
    """Subtract top stack value from second."""

    def __init__(self):
        super().__init__("SUB", OpCodeCategory.ARITHMETIC, "Subtract top from second")

    def execute(self, context: ExecutionContext) -> None:
        """Subtract: second - top."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for subtraction")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        context.data_stack.append(a - b)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class MulOp(OpCode):
    """Multiply top two stack values."""

    def __init__(self):
        super().__init__("MUL", OpCodeCategory.ARITHMETIC, "Multiply top two values")

    def execute(self, context: ExecutionContext) -> None:
        """Multiply top two values on stack."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for multiplication")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        context.data_stack.append(a * b)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class DivOp(OpCode):
    """Divide second stack value by top."""

    def __init__(self):
        super().__init__("DIV", OpCodeCategory.ARITHMETIC, "Divide second by top")

    def execute(self, context: ExecutionContext) -> None:
        """Divide: second / top."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for division")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        if b == 0:
            raise RuntimeError("Division by zero")
        context.data_stack.append(a // b)  # Integer division

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class AndOp(OpCode):
    """Bitwise AND of top two stack values."""

    def __init__(self):
        super().__init__("AND", OpCodeCategory.ARITHMETIC, "Bitwise AND")

    def execute(self, context: ExecutionContext) -> None:
        """Bitwise AND top two values."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for AND")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        context.data_stack.append(a & b)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class OrOp(OpCode):
    """Bitwise OR of top two stack values."""

    def __init__(self):
        super().__init__("OR", OpCodeCategory.ARITHMETIC, "Bitwise OR")

    def execute(self, context: ExecutionContext) -> None:
        """Bitwise OR top two values."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for OR")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        context.data_stack.append(a | b)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class XorOp(OpCode):
    """Bitwise XOR of top two stack values."""

    def __init__(self):
        super().__init__("XOR", OpCodeCategory.ARITHMETIC, "Bitwise XOR")

    def execute(self, context: ExecutionContext) -> None:
        """Bitwise XOR top two values."""
        if len(context.data_stack) < 2:
            raise RuntimeError("Not enough values on stack for XOR")
        b = context.data_stack.pop()
        a = context.data_stack.pop()
        context.data_stack.append(a ^ b)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class NotOp(OpCode):
    """Bitwise NOT of top stack value."""

    def __init__(self):
        super().__init__("NOT", OpCodeCategory.ARITHMETIC, "Bitwise NOT")

    def execute(self, context: ExecutionContext) -> None:
        """Bitwise NOT top value."""
        if not context.data_stack:
            raise RuntimeError("Data stack empty for NOT")
        a = context.data_stack.pop()
        context.data_stack.append(~a)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


# Control Flow Operations (8 ops)
class JumpOp(OpCode):
    """Unconditional jump."""

    def __init__(self):
        super().__init__("JMP", OpCodeCategory.CONTROL, "Unconditional jump")

    def execute(self, context: ExecutionContext, address: int) -> None:
        """Jump to specified address."""
        context.program_counter = address - 1  # -1 because PC increments after

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1 and isinstance(args[0], int)


class JumpZeroOp(OpCode):
    """Jump if top stack value is zero."""

    def __init__(self):
        super().__init__("JZ", OpCodeCategory.CONTROL, "Jump if zero")

    def execute(self, context: ExecutionContext, address: int) -> None:
        """Jump to address if top of stack is zero."""
        if not context.data_stack:
            raise RuntimeError("Data stack empty for JZ")
        if context.data_stack[-1] == 0:
            context.program_counter = address - 1

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1 and isinstance(args[0], int)


class JumpNotZeroOp(OpCode):
    """Jump if top stack value is not zero."""

    def __init__(self):
        super().__init__("JNZ", OpCodeCategory.CONTROL, "Jump if not zero")

    def execute(self, context: ExecutionContext, address: int) -> None:
        """Jump to address if top of stack is not zero."""
        if not context.data_stack:
            raise RuntimeError("Data stack empty for JNZ")
        if context.data_stack[-1] != 0:
            context.program_counter = address - 1

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1 and isinstance(args[0], int)


class CallOp(OpCode):
    """Function invocation."""

    def __init__(self):
        super().__init__("CALL", OpCodeCategory.CONTROL, "Function invocation")

    def execute(self, context: ExecutionContext, address: int) -> None:
        """Call function at address."""
        # Push return address onto control stack
        context.control_stack.append(context.program_counter + 1)
        context.program_counter = address - 1

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


class ReturnOp(OpCode):
    """Return from function."""

    def __init__(self):
        super().__init__("RET", OpCodeCategory.CONTROL, "Return from function")

    def execute(self, context: ExecutionContext) -> None:
        """Return to caller."""
        if not context.control_stack:
            raise RuntimeError("Control stack underflow on RET")
        context.program_counter = context.control_stack.pop() - 1

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class ForkOp(OpCode):
    """Parallel execution split."""

    def __init__(self):
        super().__init__("FORK", OpCodeCategory.CONTROL, "Parallel execution split")

    def execute(self, context: ExecutionContext, address: int) -> None:
        """Fork execution (placeholder for parallel execution)."""
        # TODO: Implement parallel execution
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


class JoinOp(OpCode):
    """Wait for forked paths."""

    def __init__(self):
        super().__init__("JOIN", OpCodeCategory.CONTROL, "Wait for forked paths")

    def execute(self, context: ExecutionContext) -> None:
        """Join forked execution paths."""
        # TODO: Implement join for parallel execution
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class HaltOp(OpCode):
    """Stop execution."""

    def __init__(self):
        super().__init__("HALT", OpCodeCategory.CONTROL, "Stop execution")

    def execute(self, context: ExecutionContext) -> None:
        """Halt execution."""
        # Special handling - VM checks for this
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


# Memory/IO Operations (8 ops)
class LoadOp(OpCode):
    """Read from memory address."""

    def __init__(self):
        super().__init__("LOAD", OpCodeCategory.MEMORY, "Read from memory address")

    def execute(self, context: ExecutionContext, address: str) -> None:
        """Load value from memory."""
        value = context.memory.get(address, 0)
        context.data_stack.append(value)

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


class StoreOp(OpCode):
    """Write to memory address."""

    def __init__(self):
        super().__init__("STORE", OpCodeCategory.MEMORY, "Write to memory address")

    def execute(self, context: ExecutionContext, address: str) -> None:
        """Store top stack value to memory."""
        if not context.data_stack:
            raise RuntimeError("Data stack empty for STORE")
        value = context.data_stack.pop()
        context.memory[address] = value

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


class FileOpenOp(OpCode):
    """Open file for operations."""

    def __init__(self):
        super().__init__("FOPEN", OpCodeCategory.MEMORY, "Open file")

    def execute(
        self, context: ExecutionContext, filename: str, mode: str = "r"
    ) -> None:
        """Open file and push handle to stack."""
        # TODO: Implement file operations
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) >= 1


class FileReadOp(OpCode):
    """Read from open file."""

    def __init__(self):
        super().__init__("FREAD", OpCodeCategory.MEMORY, "Read from file")

    def execute(self, context: ExecutionContext) -> None:
        """Read from file handle on stack."""
        # TODO: Implement file read
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class FileWriteOp(OpCode):
    """Write to open file."""

    def __init__(self):
        super().__init__("FWRITE", OpCodeCategory.MEMORY, "Write to file")

    def execute(self, context: ExecutionContext) -> None:
        """Write to file handle on stack."""
        # TODO: Implement file write
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class FileCloseOp(OpCode):
    """Close open file."""

    def __init__(self):
        super().__init__("FCLOSE", OpCodeCategory.MEMORY, "Close file")

    def execute(self, context: ExecutionContext) -> None:
        """Close file handle on stack."""
        # TODO: Implement file close
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


class LLMGenOp(OpCode):
    """Generate via local LLM."""

    def __init__(self):
        super().__init__("LLMGEN", OpCodeCategory.MEMORY, "Generate via local LLM")

    def execute(self, context: ExecutionContext, prompt: str) -> None:
        """Generate code using LLM."""
        # TODO: Implement LLM generation
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1 and isinstance(args[0], str)


class EvolveOp(OpCode):
    """Trigger self-improvement."""

    def __init__(self):
        super().__init__("EVOLVE", OpCodeCategory.MEMORY, "Trigger self-improvement")

    def execute(self, context: ExecutionContext, error_context: str) -> None:
        """Evolve code based on error context."""
        # TODO: Implement evolution mechanism
        pass

    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


class OpCodeRegistry:
    """Registry for all available op-codes."""

    def __init__(self):
        self._opcodes: dict[str, OpCode] = {}
        self._register_builtin_opcodes()

    def _register_builtin_opcodes(self) -> None:
        """Register all built-in op-codes."""
        opcodes = [
            # Stack operations
            PushOp(),
            PopOp(),
            DupOp(),
            SwapOp(),
            RotOp(),
            OverOp(),
            DropOp(),
            ClearOp(),
            # Arithmetic operations
            AddOp(),
            SubOp(),
            MulOp(),
            DivOp(),
            AndOp(),
            OrOp(),
            XorOp(),
            NotOp(),
            # Control flow operations
            JumpOp(),
            JumpZeroOp(),
            JumpNotZeroOp(),
            CallOp(),
            ReturnOp(),
            ForkOp(),
            JoinOp(),
            HaltOp(),
            # Memory/IO operations
            LoadOp(),
            StoreOp(),
            FileOpenOp(),
            FileReadOp(),
            FileWriteOp(),
            FileCloseOp(),
            LLMGenOp(),
            EvolveOp(),
        ]

        for opcode in opcodes:
            self._opcodes[opcode.name] = opcode

    def get_opcode(self, name: str) -> OpCode | None:
        """Get op-code by name."""
        return self._opcodes.get(name.upper())

    def register_opcode(self, opcode: OpCode) -> None:
        """Register a new op-code."""
        self._opcodes[opcode.name] = opcode

    def list_opcodes(self, category: OpCodeCategory | None = None) -> list[OpCode]:
        """List all op-codes, optionally filtered by category."""
        opcodes = list(self._opcodes.values())
        if category:
            opcodes = [op for op in opcodes if op.category == category]
        return opcodes

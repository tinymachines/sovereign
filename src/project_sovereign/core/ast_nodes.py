"""
Abstract Syntax Tree node definitions for PROJECT SOVEREIGN.

Defines the structure of parsed programs and instructions.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union


@dataclass
class ASTNode(ABC):
    """Base class for all AST nodes."""

    @abstractmethod
    def __str__(self) -> str:
        """String representation of the node."""
        pass


@dataclass
class Operand(ASTNode):
    """Base class for instruction operands."""

    pass


@dataclass
class Register(Operand):
    """Register operand (r0, r1, etc.)."""

    number: int

    def __str__(self) -> str:
        return f"r{self.number}"


@dataclass
class Immediate(Operand):
    """Immediate value operand (#42, #-10, etc.)."""

    value: int

    def __str__(self) -> str:
        return f"#{self.value}"


@dataclass
class Address(Operand):
    """Memory address operand (@FF00, etc.)."""

    value: str

    def __str__(self) -> str:
        return f"@{self.value}"


@dataclass
class StringLiteral(Operand):
    """String literal operand."""

    value: str

    def __str__(self) -> str:
        return f'"{self.value}"'


@dataclass
class LabelRef(Operand):
    """Label reference operand."""

    name: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Instruction(ASTNode):
    """Instruction with opcode and operands."""

    opcode: str
    operands: List[Operand]

    def __str__(self) -> str:
        if self.operands:
            operand_str = " " + " ".join(str(op) for op in self.operands)
        else:
            operand_str = ""
        return f"{self.opcode}{operand_str}"


@dataclass
class Label(ASTNode):
    """Label definition."""

    name: str

    def __str__(self) -> str:
        return f"{self.name}:"


@dataclass
class Program(ASTNode):
    """Complete program with instructions and labels."""

    instructions: List[Instruction]
    labels: Dict[str, int]  # Label name -> instruction index

    def __str__(self) -> str:
        lines = []
        for i, instruction in enumerate(self.instructions):
            # Add labels that point to this instruction
            for label_name, label_pos in self.labels.items():
                if label_pos == i:
                    lines.append(f"{label_name}:")
            lines.append(f"  {instruction}")
        return "\n".join(lines)

    def get_instruction_at_label(self, label: str) -> Optional[Instruction]:
        """Get instruction at specified label."""
        if label in self.labels:
            index = self.labels[label]
            if 0 <= index < len(self.instructions):
                return self.instructions[index]
        return None

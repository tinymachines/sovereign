"""
PROJECT SOVEREIGN: An Assembly-Like Agentic Programming Language

A revolutionary programming language designed for self-improving agentic systems.
Combines assembly-like simplicity with modern distributed computing patterns,
local LLM integration, and error-driven evolution.
"""

__version__ = "0.1.0"
__author__ = "PROJECT SOVEREIGN Team"

from .core.interpreter import SovereignInterpreter
from .core.opcodes import OpCode, OpCodeRegistry
from .core.parser import SovereignParser
from .vm.virtual_machine import SovereignVM

__all__ = [
    "OpCode",
    "OpCodeRegistry",
    "SovereignInterpreter",
    "SovereignParser",
    "SovereignVM",
]

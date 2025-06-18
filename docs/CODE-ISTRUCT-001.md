# PROJECT SOVEREIGN: Implementation Guide and Code Stubs

## Claude Code Initialization Prompt

```
PROJECT SOVEREIGN - Assembly-Like Agentic Programming Language Implementation

I need you to implement PROJECT SOVEREIGN, a revolutionary assembly-like programming language designed for self-improving agentic systems. The project combines minimal instruction set architecture with local LLM integration and error-driven evolution.

ARCHITECTURE OVERVIEW:
- 32 core op-codes in 4 categories (Stack, Arithmetic/Logic, Control Flow, Memory/IO)
- Stack-based execution model with dual stacks (data + control)
- Homoiconic design (code-as-data) for self-modification
- Local LLM integration via Ollama for code generation and error recovery
- Hex-based file handles for data persistence
- Error-driven evolution with sandboxed testing

IMPLEMENTATION PRIORITIES:
1. Core VM with stack-based execution
2. Parser for assembly syntax
3. Basic op-code implementations
4. LLM integration for LLMGEN and EVOLVE ops
5. CLI interface for program execution
6. Comprehensive test suite

PROJECT STRUCTURE:
```

src/project_sovereign/
├── core/           # Language implementation core
├── vm/             # Virtual machine and execution
├── agents/         # LLM integration and evolution
├── cli/            # Command-line interface
└── utils/          # Shared utilities

```
TECHNICAL REQUIREMENTS:
- Python 3.10+ with modern tooling (ruff, pyright, pytest)
- Lark parser for grammar definition
- Ollama Python client for LLM integration
- Rich for CLI output formatting
- Comprehensive error handling and logging

CODING STANDARDS:
- Type hints throughout
- Comprehensive docstrings
- Property-based testing where applicable
- Clean architecture with clear separation of concerns
- Performance considerations for interpreter loop

Start with the core VM implementation and basic op-codes, then progressively add LLM integration and evolution capabilities. Focus on reliability and correctness over performance initially.

The files below contain detailed stubs and specifications for each component.
```

## Core Project Files

### `src/project_sovereign/__init__.py`

```python
"""
PROJECT SOVEREIGN: An Assembly-Like Agentic Programming Language

A revolutionary programming language designed for self-improving agentic systems.
Combines assembly-like simplicity with modern distributed computing patterns,
local LLM integration, and error-driven evolution.
"""

__version__ = "0.1.0"
__author__ = "PROJECT SOVEREIGN Team"

from .core.interpreter import SovereignInterpreter
from .vm.virtual_machine import SovereignVM
from .core.parser import SovereignParser
from .core.opcodes import OpCode, OpCodeRegistry

__all__ = [
    "SovereignInterpreter",
    "SovereignVM", 
    "SovereignParser",
    "OpCode",
    "OpCodeRegistry",
]
```

### `src/project_sovereign/core/opcodes.py`

```python
"""
Core op-code definitions and registry for PROJECT SOVEREIGN.

Defines the 32 base instructions across 4 categories:
- Stack Operations (8)
- Arithmetic/Logic (8) 
- Control Flow (8)
- Memory/IO (8)
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol
from dataclasses import dataclass


class OpCodeCategory(Enum):
    """Categories of op-codes in PROJECT SOVEREIGN."""
    STACK = "stack"
    ARITHMETIC = "arithmetic"
    CONTROL = "control"
    MEMORY = "memory"


@dataclass
class ExecutionContext:
    """Context for op-code execution."""
    data_stack: List[Any]
    control_stack: List[Any]
    memory: Dict[str, Any]
    program_counter: int
    registers: Dict[str, Any]
    error_state: Optional[str] = None


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
        # TODO: Implement stack push operation
        pass
    
    def validate_args(self, *args: Any) -> bool:
        """Validate push arguments."""
        # TODO: Implement validation
        return len(args) == 1


class PopOp(OpCode):
    """Remove top stack value."""
    
    def __init__(self):
        super().__init__("POP", OpCodeCategory.STACK, "Remove top stack value")
    
    def execute(self, context: ExecutionContext) -> Any:
        """Pop value from data stack."""
        # TODO: Implement stack pop operation
        pass
    
    def validate_args(self, *args: Any) -> bool:
        """Validate pop arguments."""
        return len(args) == 0


class DupOp(OpCode):
    """Duplicate stack top."""
    
    def __init__(self):
        super().__init__("DUP", OpCodeCategory.STACK, "Duplicate stack top")
    
    def execute(self, context: ExecutionContext) -> None:
        """Duplicate top stack value."""
        # TODO: Implement duplication
        pass
    
    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


# Arithmetic Operations (8 ops)
class AddOp(OpCode):
    """Add top two stack values."""
    
    def __init__(self):
        super().__init__("ADD", OpCodeCategory.ARITHMETIC, "Add top two stack values")
    
    def execute(self, context: ExecutionContext) -> None:
        """Add top two values on stack."""
        # TODO: Implement addition
        pass
    
    def validate_args(self, *args: Any) -> bool:
        return len(args) == 0


# Control Flow Operations (8 ops)
class JumpOp(OpCode):
    """Unconditional jump."""
    
    def __init__(self):
        super().__init__("JMP", OpCodeCategory.CONTROL, "Unconditional jump")
    
    def execute(self, context: ExecutionContext, address: int) -> None:
        """Jump to specified address."""
        # TODO: Implement jump
        pass
    
    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1 and isinstance(args[0], int)


class CallOp(OpCode):
    """Function invocation."""
    
    def __init__(self):
        super().__init__("CALL", OpCodeCategory.CONTROL, "Function invocation")
    
    def execute(self, context: ExecutionContext, address: int) -> None:
        """Call function at address."""
        # TODO: Implement function call
        pass
    
    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


# Memory/IO Operations (8 ops)
class LoadOp(OpCode):
    """Read from memory address."""
    
    def __init__(self):
        super().__init__("LOAD", OpCodeCategory.MEMORY, "Read from memory address")
    
    def execute(self, context: ExecutionContext, address: str) -> None:
        """Load value from memory."""
        # TODO: Implement memory load
        pass
    
    def validate_args(self, *args: Any) -> bool:
        return len(args) == 1


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
        self._opcodes: Dict[str, OpCode] = {}
        self._register_builtin_opcodes()
    
    def _register_builtin_opcodes(self) -> None:
        """Register all built-in op-codes."""
        opcodes = [
            # Stack operations
            PushOp(), PopOp(), DupOp(),
            # TODO: Add remaining stack ops (SWAP, ROT, OVER, DROP, CLEAR)
            
            # Arithmetic operations  
            AddOp(),
            # TODO: Add remaining arithmetic ops (SUB, MUL, DIV, AND, OR, XOR, NOT)
            
            # Control flow operations
            JumpOp(), CallOp(),
            # TODO: Add remaining control ops (JZ, JNZ, RET, FORK, JOIN, HALT)
            
            # Memory/IO operations
            LoadOp(), LLMGenOp(), EvolveOp(),
            # TODO: Add remaining memory ops (STORE, FOPEN, FREAD, FWRITE, FCLOSE)
        ]
        
        for opcode in opcodes:
            self._opcodes[opcode.name] = opcode
    
    def get_opcode(self, name: str) -> Optional[OpCode]:
        """Get op-code by name."""
        return self._opcodes.get(name.upper())
    
    def register_opcode(self, opcode: OpCode) -> None:
        """Register a new op-code."""
        self._opcodes[opcode.name] = opcode
    
    def list_opcodes(self, category: Optional[OpCodeCategory] = None) -> List[OpCode]:
        """List all op-codes, optionally filtered by category."""
        opcodes = list(self._opcodes.values())
        if category:
            opcodes = [op for op in opcodes if op.category == category]
        return opcodes
```

### `src/project_sovereign/vm/virtual_machine.py`

```python
"""
Virtual Machine implementation for PROJECT SOVEREIGN.

Implements stack-based execution model with dual stacks,
memory management, and instruction dispatch.
"""

import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

from ..core.opcodes import OpCodeRegistry, ExecutionContext
from ..core.ast_nodes import Program, Instruction


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
            error_state=self.error_state
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
        
    def load_program(self, program: Program) -> None:
        """Load program into VM memory."""
        # TODO: Implement program loading
        # - Parse instructions
        # - Validate op-codes
        # - Set up initial state
        pass
    
    def execute(self, program: Program) -> None:
        """Execute a complete program."""
        self.load_program(program)
        self.state.running = True
        self.state.program_counter = 0
        
        try:
            while self.state.running and self.state.program_counter < len(program.instructions):
                self.execute_instruction(program.instructions[self.state.program_counter])
                self.state.program_counter += 1
        except Exception as e:
            self.handle_runtime_error(e)
    
    def execute_instruction(self, instruction: Instruction) -> None:
        """Execute a single instruction."""
        # TODO: Implement instruction execution
        # - Look up op-code
        # - Validate arguments
        # - Execute with current context
        # - Handle errors and evolution
        pass
    
    def handle_runtime_error(self, error: Exception) -> None:
        """Handle runtime errors with potential evolution."""
        self.logger.error(f"Runtime error: {error}")
        self.state.error_state = str(error)
        
        # TODO: Implement error-driven evolution
        # - Analyze error pattern
        # - Trigger EVOLVE op-code if appropriate
        # - Log evolution attempts
        pass
    
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
```

### `src/project_sovereign/core/parser.py`

```python
"""
Parser implementation for PROJECT SOVEREIGN assembly syntax.

Uses Lark for grammar definition and parsing of assembly programs
into abstract syntax trees.
"""

from lark import Lark, Transformer, Token
from typing import List, Optional, Union, Any
from dataclasses import dataclass

from .ast_nodes import Program, Instruction, Label, Operand, Register, Immediate, Address


# Grammar definition for PROJECT SOVEREIGN assembly
SOVEREIGN_GRAMMAR = """
    start: program

    program: (instruction | label | comment)*

    instruction: opcode operand*
    
    opcode: /[A-Z][A-Z0-9]*/
    
    operand: register 
           | immediate 
           | address
           | string_literal
           | label_ref
    
    register: /r[0-9]+/
    immediate: /#-?[0-9]+/
    address: /@[a-fA-F0-9]+/
    string_literal: ESCAPED_STRING
    label_ref: /[a-z_][a-z0-9_]*/
    
    label: /[a-z_][a-z0-9_]*/ ":"
    
    comment: ";" /[^\\n]*/
    
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
    %ignore comment
"""


class SovereignTransformer(Transformer):
    """Transform parse tree into AST nodes."""
    
    def program(self, items):
        """Transform program node."""
        instructions = []
        labels = {}
        
        for item in items:
            if isinstance(item, Instruction):
                instructions.append(item)
            elif isinstance(item, Label):
                labels[item.name] = len(instructions)
        
        return Program(instructions=instructions, labels=labels)
    
    def instruction(self, items):
        """Transform instruction node."""
        opcode = str(items[0])
        operands = items[1:] if len(items) > 1 else []
        return Instruction(opcode=opcode, operands=operands)
    
    def opcode(self, items):
        """Transform opcode token."""
        return str(items[0])
    
    def register(self, items):
        """Transform register operand."""
        reg_num = int(str(items[0])[1:])  # Remove 'r' prefix
        return Register(number=reg_num)
    
    def immediate(self, items):
        """Transform immediate operand."""
        value = int(str(items[0])[1:])  # Remove '#' prefix
        return Immediate(value=value)
    
    def address(self, items):
        """Transform address operand."""
        addr = str(items[0])[1:]  # Remove '@' prefix
        return Address(value=addr)
    
    def string_literal(self, items):
        """Transform string literal."""
        return str(items[0])[1:-1]  # Remove quotes
    
    def label_ref(self, items):
        """Transform label reference."""
        return str(items[0])
    
    def label(self, items):
        """Transform label definition."""
        return Label(name=str(items[0]))


class SovereignParser:
    """
    Parser for PROJECT SOVEREIGN assembly language.
    
    Converts assembly source code into abstract syntax trees
    for execution by the virtual machine.
    """
    
    def __init__(self):
        self.parser = Lark(SOVEREIGN_GRAMMAR, parser='lalr')
        self.transformer = SovereignTransformer()
    
    def parse(self, source: str) -> Program:
        """
        Parse source code into program AST.
        
        Args:
            source: Assembly source code
            
        Returns:
            Program AST ready for execution
            
        Raises:
            ParseError: If source code is invalid
        """
        try:
            parse_tree = self.parser.parse(source)
            program = self.transformer.transform(parse_tree)
            return program
        except Exception as e:
            raise ParseError(f"Failed to parse source: {e}") from e
    
    def parse_instruction(self, source: str) -> Instruction:
        """Parse a single instruction."""
        # TODO: Implement single instruction parsing
        # Useful for interactive mode and evolution
        pass
    
    def validate_syntax(self, source: str) -> bool:
        """Validate syntax without creating AST."""
        try:
            self.parser.parse(source)
            return True
        except Exception:
            return False


class ParseError(Exception):
    """Exception raised for parsing errors."""
    pass
```

### `src/project_sovereign/core/ast_nodes.py`

```python
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
```

### `src/project_sovereign/agents/ollama_interface.py`

```python
"""
Ollama LLM interface for PROJECT SOVEREIGN.

Provides integration with local LLM for code generation,
error analysis, and evolutionary improvements.
"""

import asyncio
import logging
from typing import AsyncGenerator, Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import ollama
except ImportError:
    ollama = None


@dataclass
class LLMRequest:
    """Request structure for LLM interactions."""
    context: str
    prompt: str
    model: str = "llama3.2"
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass
class LLMResponse:
    """Response structure from LLM."""
    content: str
    model: str
    tokens_used: int
    success: bool
    error: Optional[str] = None


class OllamaInterface:
    """
    Interface to Ollama for local LLM integration.
    
    Handles code generation, error analysis, and evolution
    suggestions using locally hosted language models.
    """
    
    def __init__(self, host: str = "http://localhost:11434", default_model: str = "llama3.2"):
        if ollama is None:
            raise ImportError("ollama package required for LLM integration")
        
        self.client = ollama.Client(host=host)
        self.default_model = default_model
        self.logger = logging.getLogger(__name__)
        
    async def generate_code(self, prompt: str, context: str = "") -> LLMResponse:
        """
        Generate code using LLM.
        
        Args:
            prompt: The generation request
            context: Additional context for generation
            
        Returns:
            LLM response with generated code
        """
        try:
            full_prompt = self._build_code_prompt(prompt, context)
            response = await self._chat_completion(fullrompt)
            return LLMResponse(
                content=response['message']['content'],
                model=response['model'],
                tokens_used=response.get('prompt_eval_count', 0) + response.get('eval_count', 0),
                success=True
            )
        except Exception as e:
            self.logger.error(f"Code generation failed: {e}")
            return LLMResponse(
                content="",
                model=self.default_model,
                tokens_used=0,
                success=False,
                error=str(e)
            )
    
    async def analyze_error(self, error_msg: str, code_context: str) -> LLMResponse:
        """
        Analyze runtime error and suggest fixes.
        
        Args:
            error_msg: Error message to analyze
            code_context: Code that caused the error
            
        Returns:
            Analysis and suggested fixes
        """
        try:
            prompt = self._build_error_analysis_prompt(error_msg, code_context)
            response = await self._chat_completion(prompt)
            return LLMResponse(
                content=response['message']['content'],
                model=response['model'],
                tokens_used=response.get('prompt_eval_count', 0) + response.get('eval_count', 0),
                success=True
            )
        except Exception as e:
            self.logger.error(f"Error analysis failed: {e}")
            return LLMResponse(
                content="",
                model=self.default_model,
                tokens_used=0,
                success=False,
                error=str(e)
            )
    
    async def suggest_evolution(self, performance_data: Dict[str, Any], code: str) -> LLMResponse:
        """
        Suggest code evolution based on performance data.
        
        Args:
            performance_data: Performance metrics and bottlenecks
            code: Current code implementation
            
        Returns:
            Evolution suggestions
        """
        # TODO: Implement evolution suggestion logic
        pass
    
    def _build_code_prompt(self, prompt: str, context: str) -> str:
        """Build prompt for code generation."""
        system_prompt = """You are an expert in PROJECT SOVEREIGN, an assembly-like agentic programming language.

PROJECT SOVEREIGN has 32 core opcodes:
- Stack: PUSH, POP, DUP, SWAP, ROT, OVER, DROP, CLEAR
- Arithmetic: ADD, SUB, MUL, DIV, AND, OR, XOR, NOT  
- Control: JMP, JZ, JNZ, CALL, RET, FORK, JOIN, HALT
- Memory/IO: LOAD, STORE, FOPEN, FREAD, FWRITE, FCLOSE, LLMGEN, EVOLVE

The language uses:
- Stack-based execution (data stack + control stack)
- Registers (r0, r1, r2, ...)
- Immediate values (#42, #-10)
- Memory addresses (@FF00)
- Labels (loop:, end:)
- String literals ("hello")

Generate clean, efficient PROJECT SOVEREIGN assembly code."""

        if context:
            return f"{system_prompt}\n\nContext: {context}\n\nRequest: {prompt}"
        else:
            return f"{system_prompt}\n\nRequest: {prompt}"
    
    def _build_error_analysis_prompt(self, error_msg: str, code_context: str) -> str:
        """Build prompt for error analysis."""
        return f"""Analyze this PROJECT SOVEREIGN runtime error and suggest fixes:

Error: {error_msg}

Code Context:
{code_context}

Provide:
1. Root cause analysis
2. Specific fix recommendations  
3. Alternative approaches
4. Prevention strategies"""
    
    async def _chat_completion(self, prompt: str) -> Dict[str, Any]:
        """Execute chat completion with Ollama."""
        response = await self.client.chat(
            model=self.default_model,
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            stream=False
        )
        return response
    
    def is_available(self) -> bool:
        """Check if Ollama service is available."""
        try:
            models = self.client.list()
            return True
        except Exception:
            return False
    
    def list_models(self) -> List[str]:
        """List avalable models."""
        try:
            response = self.client.list()
            return [model['name'] for model in response['models']]
        except Exception:
            return []
```

### `src/project_sovereign/agents/evolution_engine.py`

```python
"""
Evolution engine for PROJECT SOVEREIGN.

Implements error-driven evolution with sandboxed testing
and code improvement suggestions.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

from .ollama_interface import OllamaInterface, LLMResponse
from ..core.parser import SovereignParser
from ..vm.virtual_machine import SovereignVM
from ..core.ast_nodes import Program


@dataclass
class EvolutionAttempt:
    """Record of an evolution attempt."""
    timestamp: datetime
    original_code: str
    error_context: str
    generated_fix: str
    test_result: bool
    improvement_metrics: Dict[str, float]


class EvolutionEngine:
    """
    Engine for error-driven code evolution.
    
    Analyzes runtime errors, generates fixes using LLM,
    tests them in sandboxed environment, and integrates
    successful improvements.
    """
    
    def __init__(self, llm_interface: OllamaInterface):
        self.llm = llm_interface
        self.parser = SovereignParser()
        self.logger = logging.getLogger(__name__)
        self.evolution_history: List[EvolutionAttempt] = []
        
    async def evolve_on_error(self, error_msg: str, failed_code: str, context: Dict[str, Any]) -> Optional[str]:
        """
        Attempt to evolve code in response to runtime error.
        
        Args:
            error_msg: The runtime error message
            failed_code: Code that caused the error
            context: Execution context and environment data
            
        Returns:
            Improved code if evolution successful, None otherwise
        """
        self.logger.info(f"Starting evolution for error: {error_msg}")
        
        # Step 1: Analyze error with LLM
        analysis = await self.llm.analyze_error(error_msg, failed_code)
        if not analysis.success:
            self.logger.error("Failed to analyze error with LLM")
            return None
        
        # Step 2: Generate potential fixes
        fixes = await self._generate_fixes(analysis.content, failed_code, context)
        
        # Step 3: Test fixes in sandbox
        best_fix = None
        best_score = 0.0
        
        for fix in fixes:
            score = await self._test_fix_in_sandbox(fix, context)
            if score > best_score:
                best_score = score
                best_fix = fix
        
        # Step 4: Record evolution attempt
        attempt = EvolutionAttempt(
            timestamp=datetime.now(),
            original_code=failed_code,
            error_context=error_msg,
            generated_fix=best_fix or "",
            test_result=best_fix is not None,
            improvement_metrics={"score": best_score}
        )
        self.evolution_history.append(attempt)
        
        if best_fix and best_score > 0.7:  # Threshold for acceptance
            self.logger.info(f"Evolution successful with score {best_score}")
            return best_fix
        else:
            self.logger.warning("No acceptable evolution found")
            return None
    
    async def _generate_fixes(self, analysis: str, original_code: str, context: Dict[str, Any]) -> List[str]:
        """Generate multiple potential fixes."""
        # TODO: Implement fix generation
        # - Parse analysis for specific suggestions
        # - Generate multiple variations
        # - Consider context constraints
        fixes = []
        
        # For now, request a single fix from LLM
        fix_prompt = f"""Based on this analysis, generate a fixed version of the code:

Analysis: {analysis}

Original Code:
{original_code}

Generate only the corrected PROJECT SOVEREIGN assembly code, no explanations."""
        
        try:
            response = await self.llm.generate_code(fix_prompt)
           if response.success:
                fixes.append(response.content.strip())
        except Exception as e:
            self.logger.error(f"Fix generation failed: {e}")
        
        return fixes
    
    async def _test_fix_in_sandbox(self, fix_code: str, context: Dict[str, Any]) -> float:
        """
        Test a potential fix in isolated sandbox.
        
        Returns:
            Score from 0.0 to 1.0 indicating fix quality
        """
        try:
            # Parse the fix
            program = self.parser.parse(fix_code)
            
            # Create sandbox VM
            sandbox_vm = SovereignVM()
            
            # TODO: Implement sandboxed execution
            # - Set up isolated environment
            # - Execute with timeouts
            # - Monitor for errors and resource usage
            # - Calculate quality score
            
            # For now, return basic parse success score
            return 0.8 if program else 0.0
            
        except Exception as e:
            self.logger.debug(f"Sandbox test failed: {e}")
            return 0.0
    
    def get_evolution_stats(self) -> Dict[str, Any]:
        """Get evolution statistics."""
        if not self.evolution_history:
            return {"total_attempts": 0, "success_rate": 0.0}
        
        successful = sum(1 for attempt in self.evolution_history if attempt.test_result)
        total = len(self.evolution_history)
        
        return {
            "total_attempts": total,
            "successful_evolutions": successful,
            "success_rate": successful / total,
            "recent_attempts": self.evolution_history[-10:] if self.evolution_history else []
        }
```

### `src/project_sovereign/cli/main.py`

```python
"""
Command-line interface for PROJECT SOVEREIGN.

Provides interactive execution, file processing, and debugging
capabilities for the assembly language.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.prompt import Prompt

from ..core.parser import SovereignParser, ParseError
from ..vm.virtual_machine import SovereignVM
from ..agents.ollama_interface import OllamaInterface
from ..agents.evolution_engine import EvolutionEngine


console = Console()


@click.group()
@click.version_option()
def cli():
    """PROJECT SOVEREIGN - Assembly-Like Agentic Programming Language"""
    pass


@cli.command()
@click.argument('source_file', type=click.Path(exists=True, path_type=Path))
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.option('--evolution', '-e', is_flag=True, help='Enable error-driven evolution')
def run(source_file: Path, debug: bool, evolution: bool):
    """Execute a PROJECT SOVEREIGN program."""
    try:
        # Read source file
        source_code = source_file.read_text()
        
        # Display source if debug mode
        if debug:
            syntax = Syntax(source_code, "assembly", theme="monokai", line_numbers=True)
            console.print("\n[bold blue]Source Code:[/bold blue]")
            console.print(syntax)
            console.print()
        
        # Parse program
        parser = SovereignParser()
        program = parser.parse(source_code)
        
        # Set up VM and optional evolution
        vm = SovereignVM()
        if evolution:
            llm = OllamaInterface()
            if llm.is_available():
                evolution_engine = EvolutionEngine(llm)
               console.print("[green]Evolution mode enabled[/green]")
            else:
                console.print("[yellow]Warning: Ollama not available, evolution disabled[/yellow]")
                evolution = False
        
        # Execute program
        console.print("[bold green]Executing program...[/bold green]")
        vm.execute(program)
        
        # Display results
        if debug:
            display_vm_state(vm)
        
        console.print("[bold green]Execution completed successfully[/bold green]")
        
    except ParseError as e:
        console.print(f"[bold red]Parse Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Runtime Error:[/bold red] {e}")
        if evolution:
            console.print("[yellow]Attempting evolution...[/yellow]")
            # TODO: Trigger evolution on error
        sys.exit(1)


@cli.command()
def repl():
    """Start interactive REPL mode."""
    console.print("[bold blue]PROJECT SOVEREIGN Interactive REPL[/bold blue]")
    console.print("Enter instructions or 'help' for commands, 'exit' to quit\n")
    
    vm = SovereignVM()
    parser = SovereignParser()
    
    while True:
        try:
            # Get input
            line = Prompt.ask("[bold green]sovereign>[/bold green]").strip()
            
            if line.lower() in ('exit', 'quit'):
                break
            elif line.lower() == 'help':
                show_repl_help()
            elif line.lower() == 'state':
                display_vm_state(vm)
            elif line.lower() == 'reset':
                vm.reset()
                console.print("[yellow]VM state reset[/yellow]")
            elif line:
                # Parse and execute instruction
                instruction = parser.parse_instruction(line)
                vm.execute_instruction(instruction)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
    
    console.print("\n[blue]Goodbye![/blue]")


@cli.command()
@click.argument('source_file', type=click.Path(exists=True, path_type=Path))
def validate(source_file: Path):
    """Validate syntax of a PROJECT SOVEREIGN program."""
    try:
        source_code = source_file.read_text()
        parser = SovereignParser()
        
        if parser.validate_syntax(source_code):
            console.print(f"[green]✓[/green] {source_file} - Syntax valid")
        else:
            console.print(f"[red]✗[/red] {source_file} - Syntax invalid")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[red]Error validating {source_file}:[/red] {e}")
        sys.exit(1)


@cli.command()
def opcodes():
    """List all available op-codes."""
    from ..core.opcodes import OpCodeRegistry, OpCodeCategory
    
    registry = OpCodeRegistry()
    
    for category in OpCodeCategory:
        table = Table(title=f"{category.value.title()} Operations")
        table.add_column("Op-Code", style="cyan")
        table.add_column("Description", style="white")
        
        opcodes = registry.list_opcodes(category)
        for opcode in opcodes:
            table.add_row(opcode.name, opcode.description)
        
        console.print(table)
        console.print()


def display_vm_state(vm: SovereignVM):
    """Display current VM state."""
    state = vm.dump_state()
    
    table = Table(title="VM State")
    table.add_column("Component", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Data Stack", str(state['data_stack']))
    table.add_row("Control Stack", str(state['control_stack']))
    table.add_row("Program Counter", str(state['program_counter']))
    table.add_row("Running", str(state['running']))
    table.add_row("Memory Items", str(len(state['memory'])))
    
    if state['error_state']:
        table.add_row("Error", f"[red]{state['error_state']}[/red]")
    
    console.print(table)


def show_repl_help():
    """Show REPL help information."""
    help_text = """
[bold lue]REPL Commands:[/bold blue]
  help    - Show this help
  state   - Display VM state  
  reset   - Reset VM state
  exit    - Exit REPL

[bold blue]Instructions:[/bold blue]
  Enter any PROJECT SOVEREIGN instruction to execute immediately
  Examples: PUSH #42, ADD, POP, HALT
  
[bold blue]Op-codes:[/bold blue]
  Run 'sovereign opcodes' for complete list
"""
    console.print(help_text)


if __name__ == '__main__':
    cli()
```

### `tests/conftest.py`

```python
"""
Pytest configuration and fixtures for PROJECT SOVEREIGN tests.
"""

import pytest
from pathlib import Path

from project_sovereign.core.parser import SovereignParser
from project_sovereign.vm.virtual_machine import SovereignVM
from project_sovereign.core.opcodes import OpCodeRegistry


@pytest.fixture
def parser():
    """Provide parser instance for tests."""
    return SovereignParser()


@pytest.fixture
def vm():
    """Provide VM instance for tests."""
    return SovereignVM()


@pytest.fixture
def opcode_registry():
    """Provide opcode registry for tests."""
    return OpCodeRegistry()


@pytest.fixture
def sample_program():
    """Provide sample program for testing."""
    return """
    ; Simple test program
    PUSH #42
    PUSH #10  
    ADD
    POP
    HALT
    """


@pytest.fixture
def test_data_dir():
    """Provide test data directory."""
    return Path(__file__).parent / "data"
```

### `tests/test_parser.py`

```python
"""
Tests for PROJECT SOVEREIGN parser.
"""

import pytest
from project_sovereign.core.parser import SovereignParser, ParseError
from project_sovereign.core.ast_nodes import Program, Instruction, Register, Immediate


class TestSovereignParser:
    """Test cases for the parser."""
    
    def test_parse_simple_instruction(self, parser):
        """Test parsing a simple instruction."""
        source = "PUSH #42"
        program = parser.parse(source)
        
        assert len(program.instructions) == 1
        instruction = program.instructions[0]
        assert instruction.opcode == "PUSH"
        assert len(instruction.operands) == 1
        assert isinstance(instruction.operands[0], Immediate)
        assert instruction.operands[0].value == 42
    
    def test_parse_multiple_instructions(self, parser):
        """Test parsing multiple instructions."""
        source = """
        PUSH #10
        PUSH #20
        ADD
        """
        program = parser.parse(source)
        
        assert len(program.instructions) == 3
        assert program.instructions[0].opcode == "PUSH"
        assert program.instructions[1].opcode == "PUSH" 
        assert program.instructions[2].opcode == "ADD"
    
    def test_parse_with_labels(self, parser):
        """Test parsing with labels."""
        source = """
        loop:
        PUSH #1
        JMP loop
        """
        program = parser.parse(source)
        
        assert "loop" in program.labels
        assert program.labels["loop"] == 0
    
    def test_parse_registers(self, parser):
        """Test parsing register operands."""
        source = "LOAD r5"
        program = parser.parse(source)
        
        operand = program.instructions[0].operands[0]
        assert isinstance(operand, Register)
        assert operand.number == 5
    
    def test_invalid_syntax_raises_error(self, parser):
        """Test that invalid syntax raises ParseError."""
        with pytest.raises(ParseError):
            parser.parse("INVALID SYNTAX $$")
    
    def test_validate_syntax(self, parser):
        """Test syntax validation."""
        valid_source = "PUSH #42\nHALT"
        inalid_source = "INVALID $$"
        
        assert parser.validate_syntax(valid_source) is True
        assert parser.validate_syntax(invalid_source) is False


@pytest.mark.parametrize("source,expected_opcodes", [
    ("PUSH #1\nPOP", ["PUSH", "POP"]),
    ("ADD\nSUB\nMUL", ["ADD", "SUB", "MUL"]),
    ("JMP loop\nloop:\nHALT", ["JMP", "HALT"]),
])
def test_parse_instruction_types(parser, source, expected_opcodes):
    """Parametrized test for different instruction types."""
    program = parser.parse(source)
    actual_opcodes = [inst.opcode for inst in program.instructions]
    assert actual_opcodes == expected_opcodes
```

### `tests/test_vm.py`

```python
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
```

### `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "project-sovereign"
version = "0.1.0"
description = "An assembly-like agentic programming language implementation"
authors = [{name = "PROJECT SOVEREIGN Team"}]
license = {text  "MIT"}
readme = "README.md"
requires-python = ">=3.10"
keywords = ["assembly", "language", "ai", "agents", "llm"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License", 
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Interpreters",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

dependencies = [
    "lark>=1.1.0",
    "ollama>=0.3.0", 
    "click>=8.0.0",
    "rich>=10.0.0",
    "dataclasses-json>=0.6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "hypothesis>=6.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
    "nox>=2023.0.0",
    "pre-commit>=3.0.0",
]

docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.23.0",
]

performance = [
    "pytest-benchmark>=4.0.0",
    "memory-profiler>=0.60.0",
]

[project.scripts]
sovereign = "project_sovereign.cli.main:cli"

[project.urls]
Homepage = "https://github.com/your-org/project-sovereign"
Documentation = "https://project-sovereign.readthedocs.io"
Repository = "https://github.com/your-org/project-sovereign"
Issues = "https://github.com/your-org/project-sovereign/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
project_sovereign = ["py.typed"]

[tool.ruff]
line-length = 88
target-version = "py310"
extend-select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "B",   # flake8-bugbear
    "S",   # flake8-bandit
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG", # flake8-unused-arguments
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.10"
include = ["src"]
exclude = ["**/__pycache__"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config", 
    "--cov=project_sovereign",
    "--cov-report=term-missing",
    "--cov-report=html",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "llm: marks tests that require LLM connectivity",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError", 
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Implementation Notes for Claude Code

### Priority Implementation Order

1. **Core VM and Stack Operations** - Implement basic stack manipulation and execution context
2. **Parser and AST** - Get basic parsing working with Lark grammar
1. **Basic Op-codes** - Implement fundamental operations (PUSH, POP, ADD, etc.)
3. **CLI Interface** - Create working command-line interface for testing
4. **LLM Integration** - Add Ollama interface for LLMGEN op-code
5. **Evolution Engine** - Implement error-driven evolution with sandboxing
6. **Advanced Features** - Add distributed execution, optimization, etc.

### Key Design Decisions

- **Type Safety**: Use comprehensive type hints and enable strict type checking
- **Error Handling**: Implement robust error handling with detailed error messages
- **Testing**: Focus on comprehensive test coverage including property-based testing
- **Performance**: Optimize the interpreter loop while maintaining readability
- **Extensibility**: Design for easy addition of new op-codes and features

### Development Workflow

1. Start each component with comprehensive tests
2. Implement core functionality with proper error handling
3. Add comprehensive logging for debugging
4. Document all public API thoroughly
5. Use property-based testing for complex logic
6. Profile performance bottlenecks early

This implementation guide provides a complete foundation for PROJECT SOVEREIGN while maintaining clean architecture and comprehensive testing throughout the development process.

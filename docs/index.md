# PROJECT SOVEREIGN Documentation

Welcome to PROJECT SOVEREIGN, an assembly-like agentic programming language designed for self-improving systems.

## What is PROJECT SOVEREIGN?

PROJECT SOVEREIGN is a revolutionary programming language that combines:
- **Assembly-like simplicity** with a minimal 32-instruction set
- **Stack-based execution** with dual stacks (data + control)
- **Local LLM integration** for code generation and evolution
- **Error-driven evolution** for self-improvement
- **Homoiconic design** enabling code-as-data manipulation

## Quick Start

```bash
# Install PROJECT SOVEREIGN
git clone https://github.com/tinymachines/sovereign.git
cd sovereign
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run a program
sovereign run program.sov

# Start interactive REPL
sovereign repl

# List all opcodes
sovereign opcodes
```

## Example Program

```assembly
; Calculate 42 (the answer to everything)
PUSH #32
PUSH #10
ADD
DUP
STORE @result
HALT
```

## Documentation Structure

- **[Language Reference](reference/index.md)** - Complete language specification
- **[Opcodes Reference](reference/opcodes.md)** - All 32 operations explained
- **[Tutorials](tutorials/index.md)** - Step-by-step guides
- **[Development Guide](development/index.md)** - Contributing and architecture

## Key Features

### 32 Core Operations
The language provides exactly 32 operations across 4 categories:
- **Stack Operations** (8) - Data manipulation
- **Arithmetic/Logic** (8) - Computations
- **Control Flow** (8) - Program flow control
- **Memory/IO** (8) - Storage and external interaction

### Self-Improvement Capabilities
- **LLMGEN** - Generate code using local LLM
- **EVOLVE** - Trigger self-improvement based on errors
- **Error-driven evolution** - Learn from failures

### Modern Development
- Written in Python 3.13 with experimental features
- High-performance tooling (Ruff, uv, Pyright)
- Comprehensive test suite
- Clean, extensible architecture

## Getting Started

1. **[Installation Guide](tutorials/installation.md)** - Set up your environment
2. **[Your First Program](tutorials/first-program.md)** - Write and run code
3. **[Understanding Stacks](tutorials/stacks.md)** - Core execution model
4. **[Using the REPL](tutorials/repl.md)** - Interactive development

## Project Status

- **Phase 1**: Core Infrastructure ✅ COMPLETED
- **Phase 2**: LLM Integration ✅ COMPLETED  
- **Phase 3**: CLI/UX Development 🚧 IN PROGRESS
- **Phase 4**: Advanced Features 📋 PLANNED

## Community

- **GitHub**: [Repository Issues](https://github.com/tinymachines/sovereign/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tinymachines/sovereign/discussions)
- **Contributing**: See [Development Guide](development/contributing.md)

## License

PROJECT SOVEREIGN is released under the MIT License. See LICENSE file for details.
# PROJECT SOVEREIGN

An assembly-like agentic programming language that integrates traditional assembly concepts with modern AI capabilities through local LLM integration via Ollama.

## Features

- Assembly-like syntax with modern programming constructs
- Local LLM integration via Ollama for AI-powered operations
- Built with Python 3.13 (free-threading/no-GIL and JIT compiler support)
- Comprehensive testing with property-based testing
- High-performance tooling (Ruff, Pyright, uv)

## Installation

### Prerequisites

- Python 3.13+
- Ollama (for LLM integration)

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd project-sovereign

# Create and activate virtual environment
uv venv .venv --python 3.13
source .venv/bin/activate

# Install development dependencies
uv pip install -e ".[dev]"
```

## Development

### Running Tests

```bash
# Run all tests
nox -s tests

# Run specific test file
pytest tests/unit/test_new_instruction.py

# Run with coverage
nox -s coverage
```

### Code Quality

```bash
# Format code
ruff format src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
pyright src/
```

### Documentation

```bash
# Serve documentation locally
mkdocs serve
```

## Architecture

- `src/project_sovereign/core/` - Language implementation (lexer, parser, AST, interpreter)
- `src/project_sovereign/compiler/` - Compilation components (codegen, optimizer)
- `src/project_sovereign/agents/` - AI/LLM integration (ollama_interface, agent_runtime)
- `src/project_sovereign/cli/` - Command-line interface

## License

MIT License - see LICENSE file for details.
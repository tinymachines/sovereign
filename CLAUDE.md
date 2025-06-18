# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PROJECT SOVEREIGN is an assembly-like agentic programming language that integrates traditional assembly concepts with modern AI capabilities through local LLM integration via Ollama. The project uses Python 3.13.x with experimental features (free-threading/no-GIL and JIT compiler).

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment with Python 3.13
uv venv .venv --python 3.13
source .venv/bin/activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Core Development Commands
```bash
# Run tests
pytest tests/unit/test_new_instruction.py  # Single test file
nox -s tests                               # Full test suite

# Code quality checks
ruff format src/ tests/                    # Format code
ruff check src/ tests/                     # Lint code
pyright src/                               # Type checking

# Documentation
mkdocs serve                               # Local documentation server
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-instruction

# Commit with conventional message format
git commit -m "feat: add new instruction type"
# Use prefixes: feat:, fix:, docs:, test:, refactor:, perf:, chore:

# Create changelog entry
towncrier create 123.feature.md --content "Add new instruction type"
```

## Project Architecture

### Directory Structure
```
project-sovereign/
├── src/project_sovereign/
│   ├── core/           # Language implementation (lexer, parser, AST, interpreter)
│   ├── compiler/       # Compilation components (codegen, optimizer)
│   ├── agents/         # AI/LLM integration (ollama_interface, agent_runtime)
│   └── cli/            # Command-line interface
├── tests/              # Unit, integration, property-based tests
├── docs/               # Documentation (MkDocs with Material theme)
├── examples/           # Example programs and corpus
└── tools/              # Development utilities
```

### Key Technologies
- **Parser**: Lark parser generator (balance of power, performance, ease of use)
- **LLM Integration**: Ollama for local AI capabilities
- **Testing**: pytest with Hypothesis for property-based testing
- **Code Quality**: Ruff (30x faster than Black) and Pyright (3-5x faster than mypy)
- **Package Management**: uv (10-100x faster than pip)
- **Task Automation**: Nox for cross-platform task running

## Important Development Notes

### When Adding New Instructions
1. Implement in `src/project_sovereign/core/instructions.py`
2. Add parser rules in the Lark grammar
3. Create comprehensive tests including edge cases
4. Use property-based testing with Hypothesis
5. Update documentation with instruction reference

### Security Considerations
- Always validate input for source code parsing
- Implement resource limits (execution timeouts, memory limits)
- Sandbox execution environments
- Validate LLM inputs/outputs
- Follow OWASP guidelines for LLM applications

### Performance Path
1. Start with AST interpretation (current focus)
2. Add bytecode compilation layer
3. Implement JIT with llvmlite
4. Add caching (AST and bytecode)
5. Explore Python 3.13 free-threading for concurrency

### Testing Strategy
- Unit tests for individual components
- Integration tests for language features
- Property-based tests with Hypothesis
- Corpus-based testing (examples/corpus/valid and examples/corpus/invalid)
- Performance benchmarks with pytest-benchmark
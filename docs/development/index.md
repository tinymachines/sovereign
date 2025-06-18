# Development Guide

Contributing to PROJECT SOVEREIGN development.

## Table of Contents

1. [Architecture Overview](architecture.md)
2. [Contributing Guidelines](contributing.md)
3. [Testing Strategy](testing.md)
4. [Parser Development](parser.md)
5. [VM Internals](vm-internals.md)
6. [LLM Integration](llm-integration.md)

## Quick Start for Contributors

### 1. Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/project-sovereign.git
cd project-sovereign
git remote add upstream https://github.com/original/project-sovereign.git
```

### 2. Development Setup

```bash
# Create development environment
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### 3. Run Tests

```bash
# All tests
nox -s tests

# Specific tests
pytest tests/unit/test_vm.py -v

# With coverage
nox -s coverage
```

### 4. Code Quality

```bash
# Format code
ruff format src/ tests/

# Lint
ruff check src/ tests/

# Type check
pyright src/
```

## Project Structure

```
project-sovereign/
├── src/project_sovereign/
│   ├── core/           # Language core (parser, opcodes, AST)
│   ├── vm/             # Virtual machine implementation
│   ├── agents/         # LLM integration
│   ├── cli/            # Command-line interface
│   └── utils/          # Shared utilities
├── tests/
│   ├── unit/           # Unit tests
│   ├── integration/    # Integration tests
│   ├── property/       # Property-based tests
│   └── benchmarks/     # Performance tests
├── docs/               # Documentation (you are here)
├── examples/           # Example programs
└── tools/              # Development utilities
```

## Key Components

### Core Language (`src/project_sovereign/core/`)
- `ast_nodes.py` - AST node definitions
- `opcodes.py` - All 32 opcode implementations
- `parser.py` - Lark-based parser
- `interpreter.py` - High-level interpreter

### Virtual Machine (`src/project_sovereign/vm/`)
- `virtual_machine.py` - Stack-based VM implementation
- Dual stack architecture
- Memory management
- Error handling

### LLM Integration (`src/project_sovereign/agents/`)
- `ollama_interface.py` - Ollama API wrapper
- `evolution_engine.py` - Self-improvement logic
- Prompt engineering
- Context management

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/new-opcode
```

### 2. Implement with Tests

```python
# First write the test
def test_new_opcode():
    op = NewOp()
    context = ExecutionContext(...)
    op.execute(context)
    assert context.data_stack == [expected]

# Then implement
class NewOp(OpCode):
    def execute(self, context, *args):
        # Implementation
```

### 3. Document Changes

- Update relevant .md files
- Add docstrings
- Update CHANGELOG

### 4. Submit PR

```bash
git push origin feature/new-opcode
# Create PR on GitHub
```

## Design Principles

### 1. Simplicity First
- Minimal instruction set (exactly 32)
- Clear, predictable behavior
- No hidden complexity

### 2. Stack-Based Purity
- All operations via stack
- No hidden registers
- Explicit memory access

### 3. Error-Driven Evolution
- Errors are learning opportunities
- Fail gracefully
- Enable self-improvement

### 4. Type Safety
- Full type hints
- Strict pyright checking
- Runtime validation

## Performance Considerations

### Hot Paths
1. VM instruction dispatch loop
2. Stack push/pop operations
3. Parser tokenization

### Optimization Strategy
1. Profile first (pytest-benchmark)
2. Optimize algorithms before micro-optimizations
3. Consider PyPy for production

## Testing Philosophy

### Test Pyramid
```
        /\
       /  \  E2E Tests (few)
      /    \
     /------\ Integration Tests
    /        \
   /----------\ Unit Tests (many)
```

### Property-Based Testing
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_stack_operations(values):
    vm = SovereignVM()
    for v in values:
        vm.push_data(v)
    for v in reversed(values):
        assert vm.pop_data() == v
```

## Common Tasks

### Adding a New Opcode

1. Define in `opcodes.py`:
```python
class NewOp(OpCode):
    def __init__(self):
        super().__init__("NEW", OpCodeCategory.CATEGORY, "Description")
    
    def execute(self, context, *args):
        # Implementation
    
    def validate_args(self, *args):
        return True  # Validation logic
```

2. Register in `OpCodeRegistry._register_builtin_opcodes()`

3. Add tests in `test_opcodes.py`

4. Update documentation

### Modifying Parser Grammar

1. Edit grammar in `parser.py`
2. Update transformer methods
3. Add parser tests
4. Test with example programs

### Debugging VM Execution

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use VM dump_state()
vm = SovereignVM()
# ... execute ...
print(vm.dump_state())
```

## Release Process

1. Update version in `__init__.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Create git tag
5. Build and publish to PyPI

## Getting Help

- Read existing code and tests
- Check [Architecture Overview](architecture.md)
- Ask in GitHub Discussions
- Join development chat

## Code of Conduct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/). Be kind, be helpful, be constructive.
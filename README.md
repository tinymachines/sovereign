# PROJECT SOVEREIGN

An assembly-like agentic programming language that integrates traditional assembly concepts with modern AI capabilities through local LLM integration via Ollama.

## 🚀 Project Status

- **Phase 1**: Core Infrastructure ✅ COMPLETED
- **Phase 2**: LLM Integration ✅ COMPLETED  
- **Phase 3**: CLI/UX Development 🚧 IN PROGRESS
- **Phase 4**: Advanced Features 📋 PLANNED

**Latest Updates** (2025-06-20):
- ✅ Fixed test lockup issues in RuntimeAdapter tests
- ✅ Resolved linting and formatting issues
- ✅ Enhanced development workflow with reliable test suite
- ✅ Improved async event loop handling with proper timeouts

## ✨ Features

- **Assembly-like syntax** with modern programming constructs
- **Local LLM integration** via Ollama for AI-powered operations
- **Self-evolving code** through error-driven evolution engine
- **Comprehensive instruction set** including arithmetic, control flow, and I/O
- **Advanced opcodes**: LLMGEN for code generation, EVOLVE for self-improvement
- **Built with Python 3.13** (free-threading/no-GIL and JIT compiler support)
- **Production-ready async architecture** with thread-safe LLM operations
- **Comprehensive testing** with property-based testing via Hypothesis
- **High-performance tooling** (Ruff 30x faster than Black, Pyright 3-5x faster than mypy, uv 10-100x faster than pip)

## Installation

## 📋 Prerequisites

- Python 3.13+ (with free-threading/no-GIL and JIT support)
- [Ollama](https://ollama.ai/) (for local LLM integration)
- uv (recommended) or pip for package management

## 🔧 Installation

### Quick Start

```bash
# Clone the repository
git clone https://github.com/tinymachines/sovereign.git
cd sovereign

# Create and activate virtual environment with Python 3.13
uv venv .venv --python 3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"

# Start Ollama service (in another terminal)
ollama serve

# Pull a model for LLM features
ollama pull codellama:7b
```

## 📝 Example Programs

### Basic Arithmetic
```assembly
; examples/simple.sov
PUSH #10
PUSH #32
ADD
DUP
HALT
```

### LLM-Powered Code Generation
```assembly
; Generate code using AI
LLMGEN "Create a bubble sort implementation"
STORE "bubble_sort_code"
HALT
```

### Self-Evolving Code
```assembly
; Fix buggy code automatically
PUSH "PUSH #10\nPUSH #0\nDIV"  ; Division by zero
EVOLVE "Division by zero error"
STORE "fixed_code"
HALT
```

## 🛠️ Development

### Quick Development Setup

```bash
# Automated setup script
./scripts/dev-setup.sh

# Manual setup alternative
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with convenience script
./scripts/run-tests.sh

# Run all tests with nox
nox -s tests

# Run specific test file
pytest tests/unit/test_config.py

# Run with coverage
nox -s coverage
```

### Running Examples

```bash
# Run all examples
./scripts/run-examples.sh

# Run specific example
./scripts/run-examples.sh hello
sovereign run examples/hello.sov
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

## 🏗️ Architecture

### Core Components

```
project-sovereign/
├── src/project_sovereign/
│   ├── core/           # Language implementation
│   │   ├── lexer.py         # Tokenization
│   │   ├── parser.py        # Lark-based parser
│   │   ├── ast_.py          # Abstract syntax tree
│   │   ├── interpreter.py   # Stack-based VM
│   │   └── instructions.py  # Opcode implementations
│   ├── compiler/       # Compilation components
│   │   ├── codegen.py       # Code generation
│   │   └── optimizer.py     # AST optimization
│   ├── agents/         # AI/LLM integration
│   │   ├── ollama_client.py # Async Ollama client
│   │   ├── model_manager.py # Model selection
│   │   ├── evolution.py     # Self-improvement engine
│   │   └── runtime_adapter.py # Sync-async bridge
│   └── cli/            # Command-line interface
├── tests/              # Comprehensive test suite
├── docs/               # Documentation
└── examples/           # Example programs
```

### Key Technologies

- **Parser**: Lark parser generator for balance of power and performance
- **LLM Backend**: Ollama for local, private AI capabilities
- **Async Architecture**: aiohttp with thread-safe sync-async bridge
- **Testing**: pytest + Hypothesis for property-based testing
- **Type Safety**: Full Python 3.13 type annotations with Pyright
- **Code Quality**: Ruff for ultra-fast linting and formatting

## 🛠️ Advanced Features

### LLM Integration Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   VM Opcodes    │    │  Runtime Adapter │    │  Ollama Client  │
│  (LLMGEN/EVOLVE)│───▶│  (Sync-Async)    │───▶│  (Async HTTP)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Evolution Engine
- **Error Pattern Recognition**: ML-inspired pattern matching
- **Sandboxed Execution**: Safe testing with resource limits
- **Learning System**: Tracks fix success rates over time
- **Model Selection**: Chooses optimal model for each task

## 🔧 Troubleshooting

### Common Issues

**Test lockups or hanging**: Fixed as of 2025-06-20. If you encounter test timeouts:
```bash
# Should complete quickly now
pytest tests/unit/test_llm_integration.py::TestRuntimeAdapter::test_initialize -v
```

**Environment variable configuration**: Tests now respect `OLLAMA_MODEL` environment variable:
```bash
export OLLAMA_MODEL=codellama:7b  # or your preferred model
pytest tests/
```

**Import/formatting issues**: Use the development scripts:
```bash
./scripts/quality-check.sh  # Runs formatting, linting, and type checking
```

### Bug Reports

Known issues and their resolutions are documented in [docs/bugs/](docs/bugs/).

## 📚 Documentation

- [Phase 1 Status](docs/PHASE-I-STATUS.md) - Core infrastructure
- [Phase 2 Status](docs/PHASE-II-STATUS.md) - LLM integration  
- [Development Plans](docs/development/) - Detailed phase documentation
- [Language Reference](docs/reference/) - Syntax and opcodes
- [Bug Reports](docs/bugs/) - Known issues and fixes

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) and check the [development documentation](docs/development/).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by [Ollama](https://ollama.ai/) for local LLM capabilities
- Built with modern Python tooling ecosystem
- Inspired by assembly languages and AI-driven development
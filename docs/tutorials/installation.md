# Installation Guide

Get PROJECT SOVEREIGN up and running on your system.

## Prerequisites

- Python 3.13 or higher
- Git
- 100MB free disk space

## Quick Install

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/project-sovereign.git
cd project-sovereign
```

### 2. Set Up Python Environment

Using pyenv (recommended):
```bash
# Install Python 3.13 if needed
pyenv install 3.13.3
pyenv local 3.13.3

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Or using uv (faster):
```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment with Python 3.13
uv venv .venv --python 3.13
source .venv/bin/activate
```

### 3. Install PROJECT SOVEREIGN

Development install (recommended):
```bash
pip install -e ".[dev]"
```

Or using uv:
```bash
uv pip install -e ".[dev]"
```

### 4. Verify Installation

```bash
sovereign --version
sovereign opcodes  # Should list 32 operations
```

## Platform-Specific Instructions

### Linux/macOS

The default instructions work perfectly. For better performance:

```bash
# Enable Python 3.13 free-threading (optional)
python -X gil=0 -m sovereign ...
```

### Windows

Use PowerShell or WSL2 (recommended):

```powershell
# PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

### Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install -e .
ENTRYPOINT ["sovereign"]
```

Build and run:
```bash
docker build -t sovereign .
docker run -it sovereign repl
```

## Optional Components

### Ollama for LLM Integration

For LLMGEN and EVOLVE opcodes:

1. Install Ollama:
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve
```

2. Pull a model:
```bash
ollama pull llama3.2
```

3. Verify integration:
```python
from project_sovereign.agents.ollama_interface import OllamaInterface
llm = OllamaInterface()
print(llm.is_available())  # Should print True
```

### Development Tools

For contributing:

```bash
# Install all development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/ tests/

# Run type checking
pyright src/

# Format code
ruff format src/ tests/
```

## Environment Variables

Optional configuration:

```bash
# Ollama configuration
export OLLAMA_HOST="http://localhost:11434"
export OLLAMA_MODEL="llama3.2"

# Development settings
export SOVEREIGN_DEBUG=1
export SOVEREIGN_LOG_LEVEL=DEBUG
```

## Troubleshooting

### Common Issues

**Import Error: No module named 'project_sovereign'**
```bash
# Ensure you're in the project directory
cd project-sovereign
# Reinstall in development mode
pip install -e .
```

**Command 'sovereign' not found**
```bash
# Check if installed
pip list | grep sovereign
# Ensure .venv/bin is in PATH
export PATH="$PATH:$(pwd)/.venv/bin"
```

**Parser Error: Zero-width terminal**
```bash
# Known issue with multi-line parsing
# Use single instructions for now
echo "PUSH #42" | sovereign run -
```

### Python Version Issues

Ensure Python 3.13:
```bash
python --version  # Should show 3.13.x
```

If not available:
```bash
# Using pyenv
pyenv install 3.13.3
pyenv local 3.13.3

# Using conda
conda create -n sovereign python=3.13
conda activate sovereign
```

### Performance Optimization

For better performance:

1. **Enable JIT** (Python 3.13):
```bash
python -X jit=1 -m sovereign run program.sov
```

2. **Disable GIL** (experimental):
```bash
python -X gil=0 -m sovereign run program.sov
```

3. **Use PyPy** (alternative):
```bash
pypy3 -m pip install -e .
pypy3 -m sovereign run program.sov
```

## IDE Setup

### VS Code

1. Install Python extension
2. Create `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "python.languageServer": "Pylance",
    "[sovereign]": {
        "editor.rulers": [80]
    }
}
```

3. Add syntax highlighting for .sov files:
   - Install "Assembly" extension
   - Associate .sov with assembly

### PyCharm

1. Mark `src` as Sources Root
2. Configure interpreter to use .venv
3. Enable type checking with pyright

## Next Steps

Installation complete! Now:

1. Read [Your First Program](first-program.md) to start coding
2. Explore [example programs](../examples/) 
3. Check [Language Reference](../reference/index.md) for details

For issues, visit [GitHub Issues](https://github.com/your-org/project-sovereign/issues).
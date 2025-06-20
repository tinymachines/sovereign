#!/bin/bash

# Development environment setup for PROJECT SOVEREIGN

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setting up PROJECT SOVEREIGN Development Environment${NC}"
echo "=================================================="

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | grep -oP '3\.\d+')
required_version="3.13"

if [[ "$python_version" != "$required_version" ]]; then
    echo -e "${RED}❌ Python $required_version required, but $python_version found${NC}"
    echo "Please install Python 3.13 before continuing"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version detected${NC}"

# Check if uv is installed
echo -e "\n${YELLOW}Checking for uv...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv not found${NC}"
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi
echo -e "${GREEN}✓ uv is installed${NC}"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [[ -d ".venv" ]]; then
    echo -e "${YELLOW}Virtual environment already exists, skipping creation${NC}"
else
    uv venv .venv --python 3.13
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
uv pip install -e ".[dev]"
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check Ollama installation
echo -e "\n${YELLOW}Checking Ollama installation...${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
    
    # Check if Ollama is running
    if ollama list &> /dev/null; then
        echo -e "${GREEN}✓ Ollama service is running${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama is installed but not running${NC}"
        echo "Start Ollama with: ollama serve"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not found${NC}"
    echo "For AI features, install Ollama from: https://ollama.ai"
fi

# Run initial checks
echo -e "\n${YELLOW}Running initial checks...${NC}"

# Format check
echo -e "${BLUE}Format check:${NC}"
ruff format --check src/ tests/ || {
    echo -e "${YELLOW}⚠️  Code formatting issues found. Run: ruff format src/ tests/${NC}"
}

# Lint check
echo -e "${BLUE}Lint check:${NC}"
ruff check src/ tests/ || {
    echo -e "${YELLOW}⚠️  Linting issues found. Run: ruff check src/ tests/${NC}"
}

# Type check
echo -e "${BLUE}Type check:${NC}"
pyright src/ || {
    echo -e "${YELLOW}⚠️  Type checking issues found${NC}"
}

echo -e "\n${GREEN}🎉 Development environment setup complete!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Run tests: ./scripts/run-tests.sh"
echo "3. Run examples: ./scripts/run-examples.sh"
echo "4. Start documentation server: mkdocs serve"
#!/bin/bash

# Run tests for PROJECT SOVEREIGN

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧪 Running PROJECT SOVEREIGN Tests${NC}"
echo "================================"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated. Activating...${NC}"
    source .venv/bin/activate || {
        echo -e "${RED}❌ Failed to activate virtual environment${NC}"
        echo "Please ensure you have created a virtual environment with: uv venv .venv --python 3.13"
        exit 1
    }
fi

# Run different test suites based on argument
case "${1:-all}" in
    unit)
        echo -e "${GREEN}Running unit tests...${NC}"
        pytest tests/unit/ -v
        ;;
    integration)
        echo -e "${GREEN}Running integration tests...${NC}"
        pytest tests/integration/ -v
        ;;
    property)
        echo -e "${GREEN}Running property-based tests...${NC}"
        pytest tests/ -v -k "property" --hypothesis-show-statistics
        ;;
    coverage)
        echo -e "${GREEN}Running tests with coverage...${NC}"
        pytest tests/ --cov=src/project_sovereign --cov-report=html --cov-report=term
        ;;
    single)
        if [[ -z "$2" ]]; then
            echo -e "${RED}❌ Please specify a test file${NC}"
            echo "Usage: $0 single tests/unit/test_file.py"
            exit 1
        fi
        echo -e "${GREEN}Running single test: $2${NC}"
        pytest "$2" -v
        ;;
    nox)
        echo -e "${GREEN}Running full test suite with nox...${NC}"
        nox -s tests
        ;;
    all)
        echo -e "${GREEN}Running all tests...${NC}"
        pytest tests/ -v
        ;;
    *)
        echo -e "${RED}Unknown test suite: $1${NC}"
        echo "Available options: unit, integration, property, coverage, single, nox, all"
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Tests completed!${NC}"
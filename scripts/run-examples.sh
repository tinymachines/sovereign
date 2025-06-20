#!/bin/bash

# Run examples for PROJECT SOVEREIGN

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Running PROJECT SOVEREIGN Examples${NC}"
echo "===================================="

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated. Activating...${NC}"
    source .venv/bin/activate || {
        echo -e "${RED}❌ Failed to activate virtual environment${NC}"
        echo "Please ensure you have created a virtual environment with: uv venv .venv --python 3.13"
        exit 1
    }
fi

# Function to run an example
run_example() {
    local example_file=$1
    echo -e "\n${GREEN}Running: $example_file${NC}"
    echo "----------------------------"
    
    if [[ -f "$example_file" ]]; then
        python -m project_sovereign run "$example_file" || {
            echo -e "${RED}❌ Failed to run $example_file${NC}"
            return 1
        }
    else
        echo -e "${RED}❌ Example file not found: $example_file${NC}"
        return 1
    fi
}

# Run specific example or all examples
case "${1:-all}" in
    hello)
        run_example "examples/hello.sov"
        ;;
    simple)
        run_example "examples/simple.sov"
        ;;
    list)
        echo -e "${BLUE}Available examples:${NC}"
        if [[ -d "examples" ]]; then
            find examples -name "*.sov" -type f | sort | while read -r file; do
                echo "  - $(basename "$file" .sov)"
            done
        else
            echo -e "${YELLOW}No examples directory found${NC}"
        fi
        ;;
    all)
        echo -e "${GREEN}Running all examples...${NC}"
        if [[ -d "examples" ]]; then
            find examples -name "*.sov" -type f | sort | while read -r example; do
                run_example "$example"
            done
        else
            echo -e "${YELLOW}No examples directory found${NC}"
        fi
        ;;
    corpus)
        echo -e "${GREEN}Running corpus examples...${NC}"
        if [[ -d "examples/corpus/valid" ]]; then
            for example in examples/corpus/valid/*.sov; do
                run_example "$example"
            done
        else
            echo -e "${YELLOW}No corpus examples found${NC}"
        fi
        ;;
    *)
        if [[ -f "$1" ]]; then
            run_example "$1"
        else
            echo -e "${RED}Unknown example or file not found: $1${NC}"
            echo "Usage: $0 [hello|simple|list|all|corpus|<file.sov>]"
            exit 1
        fi
        ;;
esac

echo -e "\n${GREEN}✅ Examples completed!${NC}"
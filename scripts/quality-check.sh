#!/bin/bash

# Code quality checks for PROJECT SOVEREIGN

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Running Code Quality Checks${NC}"
echo "=============================="

# Track if any checks fail
FAILED=0

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated. Activating...${NC}"
    source .venv/bin/activate || {
        echo -e "${RED}❌ Failed to activate virtual environment${NC}"
        exit 1
    }
fi

# Function to run a check
run_check() {
    local check_name=$1
    local check_command=$2
    
    echo -e "\n${YELLOW}Running $check_name...${NC}"
    if eval "$check_command"; then
        echo -e "${GREEN}✓ $check_name passed${NC}"
    else
        echo -e "${RED}✗ $check_name failed${NC}"
        FAILED=1
    fi
}

# Run checks based on argument
case "${1:-all}" in
    format)
        run_check "Code formatting" "ruff format --check src/ tests/"
        ;;
    lint)
        run_check "Linting" "ruff check src/ tests/"
        ;;
    type)
        run_check "Type checking" "pyright src/"
        ;;
    security)
        run_check "Security scan" "bandit -r src/ -ll"
        ;;
    test)
        run_check "Tests" "pytest tests/ -q"
        ;;
    all)
        run_check "Code formatting" "ruff format --check src/ tests/"
        run_check "Linting" "ruff check src/ tests/"
        run_check "Type checking" "pyright src/"
        
        # Optional checks (continue even if they fail)
        echo -e "\n${YELLOW}Running optional checks...${NC}"
        
        # Security check
        if command -v bandit &> /dev/null; then
            bandit -r src/ -ll || echo -e "${YELLOW}⚠️  Security issues found (non-blocking)${NC}"
        else
            echo -e "${YELLOW}⚠️  bandit not installed, skipping security check${NC}"
        fi
        
        # Complexity check
        if command -v radon &> /dev/null; then
            echo -e "\n${BLUE}Cyclomatic complexity:${NC}"
            radon cc src/ -a -nb || true
        fi
        ;;
    fix)
        echo -e "${GREEN}Fixing code issues...${NC}"
        echo -e "\n${YELLOW}Formatting code...${NC}"
        ruff format src/ tests/
        echo -e "\n${YELLOW}Fixing linting issues...${NC}"
        ruff check --fix src/ tests/
        echo -e "${GREEN}✓ Code fixes applied${NC}"
        ;;
    *)
        echo -e "${RED}Unknown check: $1${NC}"
        echo "Available options: format, lint, type, security, test, all, fix"
        exit 1
        ;;
esac

# Summary
echo -e "\n${BLUE}Summary:${NC}"
if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
else
    echo -e "${RED}❌ Some checks failed${NC}"
    echo -e "${YELLOW}Run './scripts/quality-check.sh fix' to auto-fix formatting and linting issues${NC}"
    exit 1
fi
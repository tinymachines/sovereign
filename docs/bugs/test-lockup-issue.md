# Test Suite Lockup Issue

## Issue Description
The test suite experiences a lockup/timeout when running all tests via `./scripts/run-tests.sh all`.

## Symptoms
- Test execution begins normally
- Progress reaches approximately 48% (37/78 tests)
- Test hangs at `tests/unit/test_llm_integration.py::TestRuntimeAdapter::test_initialize`
- Command times out after 60 seconds
- One test failure noted: `tests/unit/test_llm_integration.py::TestEvolutionEngine::test_evolve_success FAILED`

## Environment
- Working directory: `/home/bisenbek/projects/sovereign`
- Platform: Linux 6.8.0-60-generic
- Python version: 3.13.3
- Test runner: pytest-8.4.1

## Reproduction Steps
1. Navigate to project root
2. Run: `./scripts/run-tests.sh all`
3. Test suite will hang at approximately test 37/78

## Last Test Output Before Hang
```
tests/unit/test_llm_integration.py::TestEvolutionEngine::test_evolve_success FAILED [ 44%]
tests/unit/test_llm_integration.py::TestEvolutionEngine::test_evolve_failure PASSED [ 46%]
tests/unit/test_llm_integration.py::TestEvolutionEngine::test_evolution_history PASSED [ 47%]
tests/unit/test_llm_integration.py::TestEvolutionEngine::test_pattern_export_import PASSED [ 48%]
tests/unit/test_llm_integration.py::TestRuntimeAdapter::test_initialize
```

## Potential Causes
1. **LLM Integration Issue**: The lockup occurs in LLM-related tests, suggesting possible:
   - Ollama connection timeout
   - Infinite loop in mock/test setup
   - Resource deadlock
   
2. **RuntimeAdapter Initialization**: The specific test that hangs is `test_initialize`, which might be:
   - Waiting for external service
   - Stuck in initialization logic
   - Threading/async issue

## Recommended Investigation
1. Run the specific test in isolation: `pytest tests/unit/test_llm_integration.py::TestRuntimeAdapter::test_initialize -vvs`
2. Check if Ollama service is required and running
3. Review the failed test: `test_evolve_success`
4. Add timeout decorators to LLM-related tests
5. Check for any blocking I/O operations in the RuntimeAdapter initialization

## Workaround
Run tests selectively:
- Unit tests only: `./scripts/run-tests.sh unit`
- Skip LLM integration tests temporarily
- Use pytest markers to exclude problematic tests
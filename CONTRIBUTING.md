# Contributing to PROJECT SOVEREIGN

Thank you for your interest in contributing to PROJECT SOVEREIGN! We welcome contributions from the community.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/sovereign.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Set up development environment:
   ```bash
   uv venv .venv --python 3.13
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

## Development Workflow

### Before You Start
- Check existing issues and pull requests
- For major changes, open an issue first to discuss
- Ensure you have Python 3.13 with free-threading/no-GIL support

### Making Changes
1. Write clean, documented code following project style
2. Add comprehensive tests for new features
3. Update documentation as needed
4. Run quality checks:
   ```bash
   # Format code
   ruff format src/ tests/
   
   # Lint code
   ruff check src/ tests/
   
   # Type checking
   pyright src/
   
   # Run tests
   pytest
   ```

### Commit Messages
Use conventional commit format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `chore:` Maintenance tasks

Example: `feat: add LLMGEN opcode for code generation`

### Pull Request Process
1. Update README.md if needed
2. Ensure all tests pass
3. Update documentation
4. Submit PR with clear description
5. Address review feedback

## Code Style

- Follow PEP 8 with Ruff formatting
- Use type hints (Python 3.13 style)
- Write descriptive docstrings
- Keep functions focused and small
- Prefer composition over inheritance

## Testing

- Write unit tests for all new code
- Use Hypothesis for property-based testing
- Maintain or improve test coverage
- Test edge cases and error conditions

## Documentation

- Update relevant .md files
- Add docstrings to functions/classes
- Include examples where helpful
- Keep CLAUDE.md updated for AI assistance

## Questions?

- Open an issue for bugs/features
- Use discussions for questions
- Check existing issues first

Thank you for contributing to PROJECT SOVEREIGN!
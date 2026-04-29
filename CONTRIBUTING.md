# Contributing to jpath

Thank you for your interest in contributing to jpath!

## Development Setup

```bash
# Clone the repository
git clone https://github.com/izag8216/jpath.git
cd jpath

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jpath --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py -v
```

## Coding Standards

- **Style:** Follow [PEP 8](https://pep8.org/) conventions
- **Type hints:** Use `typing` module for all public functions
- **Docstrings:** Google-style docstrings for all public APIs
- **Line length:** 100 characters maximum
- **Imports:** Grouped and sorted (stdlib, third-party, local)

### Linting

```bash
# Run linter
ruff check src/jpath/ tests/

# Auto-fix linting issues
ruff check --fix src/jpath/ tests/
```

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature or bugfix
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. **Write tests** for new functionality
4. **Ensure all tests pass** with good coverage
5. **Commit** with conventional commit format:
   ```
   feat: add CSV output format support
   fix: handle empty JSON input gracefully
   docs: update API reference examples
   ```
6. **Push** and open a Pull Request
7. **Wait for review** and address any feedback

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, no logic change) |
| `refactor` | Code refactoring |
| `test` | Test additions or changes |
| `chore` | Build process or auxiliary tool changes |

## Reporting Issues

When reporting issues, please include:

- Python version (`python --version`)
- jpath version (`jpath --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Sample JSON file (if applicable)

## License

By contributing to jpath, you agree that your contributions will be licensed under the MIT License.

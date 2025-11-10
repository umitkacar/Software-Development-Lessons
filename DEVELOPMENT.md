# 🛠️ Development Guide

This guide will help you set up the development environment and contribute to the Software Development Lessons project.

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** installed
- **Git** for version control
- **Hatch** for project management (recommended) or pip

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/umitkacar/Software-Development-Lessons.git
cd Software-Development-Lessons
```

2. **Install Hatch** (if not already installed):

```bash
pip install hatch
```

3. **Create and activate environment:**

```bash
# Hatch automatically creates and manages virtual environments
hatch shell
```

4. **Install dependencies:**

```bash
# Install all development dependencies
pip install -e ".[dev]"

# Or install all optional dependencies
pip install -e ".[all]"
```

5. **Install pre-commit hooks:**

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

## 📦 Project Structure

```
Software-Development-Lessons/
├── src/
│   └── software_development_lessons/
│       ├── __init__.py          # Package initialization
│       ├── cli.py               # CLI application
│       ├── core/                # Core modules
│       │   ├── __init__.py
│       │   ├── resource_manager.py
│       │   └── learning_tracker.py
│       └── utils/               # Utility functions
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── .github/
│   └── workflows/              # GitHub Actions CI/CD
├── pyproject.toml              # Project configuration
├── .pre-commit-config.yaml     # Pre-commit hooks
└── README.md
```

## 🔧 Development Tools

### Hatch Commands

```bash
# Run tests
hatch run test

# Run tests with coverage
hatch run test-cov

# Run linter (ruff)
hatch run lint

# Fix linting issues
hatch run lint-fix

# Format code (black)
hatch run format

# Check formatting
hatch run format-check

# Type checking (mypy)
hatch run typecheck

# Run all quality checks
hatch run check

# Fix all auto-fixable issues
hatch run fix
```

### Manual Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=software_development_lessons --cov-report=html

# Run specific test file
pytest tests/unit/test_resource_manager.py

# Run tests with specific marker
pytest -m "not slow"

# Run linter
ruff check .

# Fix linting issues
ruff check --fix .

# Format code
black .

# Type check
mypy src/software_development_lessons
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test class
pytest tests/unit/test_resource_manager.py::TestResourceManager

# Run specific test method
pytest tests/unit/test_resource_manager.py::TestResourceManager::test_add_resource

# Run tests in parallel
pytest -n auto

# Run only unit tests
pytest tests/unit

# Run only integration tests
pytest tests/integration
```

### Coverage

```bash
# Generate HTML coverage report
pytest --cov=software_development_lessons --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Test Markers

```python
# Slow tests
@pytest.mark.slow
def test_slow_operation():
    pass

# Integration tests
@pytest.mark.integration
def test_full_workflow():
    pass

# Unit tests
@pytest.mark.unit
def test_single_function():
    pass
```

Run specific markers:

```bash
pytest -m "slow"           # Run only slow tests
pytest -m "not slow"       # Skip slow tests
pytest -m "integration"    # Run only integration tests
```

## 📝 Code Quality

### Linting with Ruff

Ruff is a super-fast Python linter that replaces multiple tools (flake8, isort, pyupgrade, etc.).

```bash
# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Check specific file
ruff check src/software_development_lessons/core/resource_manager.py
```

### Formatting with Black

```bash
# Format all files
black .

# Check formatting without changes
black --check .

# Format specific file
black src/software_development_lessons/cli.py
```

### Type Checking with Mypy

```bash
# Check all source files
mypy src/software_development_lessons

# Check specific file
mypy src/software_development_lessons/core/resource_manager.py

# Show error codes
mypy --show-error-codes src/
```

## 🎯 Pre-commit Hooks

Pre-commit hooks run automatically before each commit to ensure code quality.

### Setup

```bash
# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

### Manual Execution

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run black --all-files
pre-commit run mypy --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

### Hooks Included

- ✅ **ruff**: Fast linting and auto-fixing
- ✅ **black**: Code formatting
- ✅ **mypy**: Type checking
- ✅ **pytest**: Run tests
- ✅ **prettier**: YAML/Markdown formatting
- ✅ **codespell**: Spell checking
- ✅ **bandit**: Security linting
- ✅ **File checks**: Trailing whitespace, EOF, merge conflicts, etc.

### Skipping Hooks

```bash
# Skip all hooks (use sparingly!)
git commit --no-verify -m "message"

# Skip specific hook
SKIP=pytest git commit -m "message"
```

## 🏗️ Building the Package

```bash
# Build distribution
hatch build

# This creates:
# - dist/software_development_lessons-1.0.0.tar.gz
# - dist/software_development_lessons-1.0.0-py3-none-any.whl
```

## 📊 Code Style Guidelines

### General Principles

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all functions
- Write descriptive docstrings (Google style)
- Keep functions small and focused
- Prefer composition over inheritance

### Type Hints

```python
from typing import Any

def process_data(
    data: list[dict[str, Any]],
    threshold: float = 0.5,
) -> dict[str, int]:
    """Process data and return statistics.

    Args:
        data: List of data dictionaries.
        threshold: Minimum threshold value.

    Returns:
        Dictionary containing statistics.

    Raises:
        ValueError: If threshold is not between 0 and 1.
    """
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers.

    This function takes a list of floating-point numbers and returns
    their arithmetic mean.

    Args:
        numbers: A list of numbers to average.

    Returns:
        The arithmetic mean of the input numbers.

    Raises:
        ValueError: If the input list is empty.

    Examples:
        >>> calculate_average([1.0, 2.0, 3.0])
        2.0
        >>> calculate_average([10.0, 20.0])
        15.0
    """
    if not numbers:
        msg = "Cannot calculate average of empty list"
        raise ValueError(msg)

    return sum(numbers) / len(numbers)
```

### Error Messages

Use clear, actionable error messages:

```python
# Bad
raise ValueError("Invalid input")

# Good
msg = f"Temperature must be between -273.15 and 1000, got {temperature}"
raise ValueError(msg)
```

## 🔄 Git Workflow

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Examples:**

```bash
git commit -m "feat(core): add resource filtering by tags"
git commit -m "fix(tracker): correct time calculation for sessions"
git commit -m "docs: update installation instructions"
git commit -m "test(manager): add tests for resource validation"
```

### Branch Naming

```
<type>/<short-description>

Examples:
- feature/add-resource-tags
- fix/time-tracking-bug
- docs/update-readme
- refactor/resource-manager
```

## 🐛 Debugging

### VS Code Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

### Debugging Tips

```python
# Add breakpoint in code
import pdb; pdb.set_trace()

# Or use built-in breakpoint()
breakpoint()

# pytest with debugger
pytest --pdb  # Drop into debugger on failure
pytest --pdb --maxfail=1  # Stop at first failure
```

## 📚 Additional Resources

- [Hatch Documentation](https://hatch.pypa.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Pre-commit Documentation](https://pre-commit.com/)

## ❓ FAQ

### How do I add a new dependency?

Edit `pyproject.toml` and add to the appropriate section:

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "your-new-package>=1.0.0",
]
```

Then reinstall:

```bash
pip install -e ".[dev]"
```

### How do I skip a pre-commit hook?

```bash
# Skip all hooks
git commit --no-verify

# Skip specific hook
SKIP=pytest git commit -m "message"
```

### How do I run tests in watch mode?

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw
```

### My IDE shows import errors

Make sure you've installed the package in editable mode:

```bash
pip install -e ".[dev]"
```

And configure your IDE to use the correct Python interpreter from the virtual environment.

## 🤝 Getting Help

- 📖 Read the [Contributing Guide](CONTRIBUTING.md)
- 🐛 [Open an issue](https://github.com/umitkacar/Software-Development-Lessons/issues)
- 💬 Start a [discussion](https://github.com/umitkacar/Software-Development-Lessons/discussions)

---

<div align="center">

**Happy Coding! 🚀**

</div>

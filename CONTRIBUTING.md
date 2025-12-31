# Contributing to Switchblade

First off, thank you for considering contributing to Switchblade! It's people like you that make Switchblade such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include Python version and OS details**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain the behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fork the repo and create your branch from `main`
* If you've added code that should be tested, add tests
* If you've changed APIs, update the documentation
* Ensure the test suite passes
* Make sure your code follows the existing style
* Issue that pull request!

## Development Setup

1. Fork and clone the repository
```bash
git clone git@github.com:YOUR_USERNAME/switchblade.git
cd switchblade
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

4. Install development dependencies
```bash
pip install pytest pytest-asyncio pytest-cov black mypy flake8
```

## Coding Standards

* Follow PEP 8 style guidelines
* Use type hints wherever possible
* Write docstrings for all public functions and classes
* Keep functions small and focused
* Write meaningful variable names

### Code Formatting

We use `black` for code formatting:

```bash
black src/ tests/ examples/
```

### Type Checking

We use `mypy` for type checking:

```bash
mypy src/
```

### Linting

We use `flake8` for linting:

```bash
flake8 src/ tests/ examples/
```

## Testing

* Write tests for all new features
* Ensure all tests pass before submitting PR
* Aim for high code coverage

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Documentation

* Update README.md if needed
* Add docstrings to new functions and classes
* Update examples if you change the API

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example:
```
Add support for WebSocket connections

- Implement WebSocket server handler
- Add client WebSocket support
- Update tests for WebSocket functionality

Fixes #123
```

## Project Structure

```
switchblade/
├── src/              # Source code
│   ├── server/       # Server implementation
│   └── client/       # Client implementation
├── tests/            # Test files
├── examples/         # Example scripts
└── docs/             # Documentation (future)
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉

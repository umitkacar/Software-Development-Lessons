.PHONY: help install dev test lint format typecheck clean build publish

.DEFAULT_GOAL := help

help: ## Show this help message
	@echo '📚 Software Development Lessons - Development Commands'
	@echo ''
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package in development mode
	pip install -e .
	@echo '✅ Package installed in development mode'

dev: ## Install all development dependencies
	pip install -e ".[dev]"
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo '✅ Development environment ready!'

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=software_development_lessons --cov-report=html --cov-report=term

test-watch: ## Run tests in watch mode (requires pytest-watch)
	ptw

lint: ## Run linter (ruff)
	ruff check .

lint-fix: ## Fix linting issues automatically
	ruff check --fix .

format: ## Format code with black
	black .

format-check: ## Check code formatting
	black --check .

typecheck: ## Run type checker (mypy)
	mypy src/software_development_lessons

check: format-check lint typecheck test-cov ## Run all quality checks

fix: format lint-fix ## Fix all auto-fixable issues

clean: ## Clean build artifacts and cache files
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	@echo '✨ Cleaned all build artifacts and cache files'

build: clean ## Build distribution packages
	hatch build
	@echo '📦 Build complete! Check dist/ directory'

docs: ## Build documentation
	hatch run docs:build

docs-serve: ## Serve documentation locally
	hatch run docs:serve

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	pre-commit autoupdate

publish-test: build ## Publish to TestPyPI
	twine upload --repository testpypi dist/*

publish: build ## Publish to PyPI
	twine upload dist/*

shell: ## Open hatch shell
	hatch shell

stats: ## Show project statistics
	@echo '📊 Project Statistics:'
	@echo ''
	@echo 'Lines of Code:'
	@find src -name '*.py' -exec wc -l {} + | tail -1
	@echo ''
	@echo 'Test Files:'
	@find tests -name 'test_*.py' | wc -l
	@echo ''
	@echo 'Dependencies:'
	@pip list --format=freeze | wc -l

requirements: ## Generate requirements.txt files
	pip-compile --output-file=requirements.txt pyproject.toml
	pip-compile --extra=dev --output-file=requirements-dev.txt pyproject.toml

upgrade: ## Upgrade all dependencies
	pip install --upgrade pip hatch
	pre-commit autoupdate
	@echo '⬆️  Dependencies upgraded!'

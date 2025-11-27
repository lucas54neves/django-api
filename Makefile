.PHONY: help install install-dev test lint format clean coverage

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

test: ## Run all tests
	python manage.py test --verbosity=2

test-coverage: ## Run tests with coverage report
	coverage run --source='.' manage.py test
	coverage report
	coverage html
	@echo "HTML report generated at htmlcov/index.html"

lint: ## Run all linting checks
	@echo "==> Running Black..."
	black --check --diff .
	@echo "\n==> Running isort..."
	isort --check-only --diff .
	@echo "\n==> Running Flake8..."
	flake8 .
	@echo "\n==> Running Pylint..."
	pylint --disable=all --enable=E,F --ignore=migrations,venv **/*.py

format: ## Format code automatically
	@echo "==> Formatting with Black..."
	black .
	@echo "\n==> Organizing imports with isort..."
	isort .
	@echo "\n✅ Code formatted!"

lint-fix: format ## Alias for format (fix formatting issues)

check: lint test ## Run lint and tests (same as CI checks)

clean: ## Remove temporary and cache files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf *.egg-info
	@echo "✅ Temporary files removed!"

run: ## Start development server
	python manage.py runserver

migrate: ## Run database migrations
	python manage.py migrate

makemigrations: ## Create new migrations
	python manage.py makemigrations

shell: ## Open Django shell
	python manage.py shell

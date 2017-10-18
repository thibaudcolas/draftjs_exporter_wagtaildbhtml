.PHONY: clean-pyc init help test-ci
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

init: clean-pyc ## Install dependencies and initialise for development.
	pip install -r requirements.txt

lint: ## Lint the project.
	flake8 tests example.py
	isort --check-only --diff --recursive tests example.py

test: ## Test the project.
	python -m unittest discover

test-watch: ## Restarts the tests whenever a file changes.
	nodemon -q -e py -w tests  -x "clear && make test -s || true"

test-coverage: ## Run the tests while generating test coverage data.
	coverage run -m unittest discover && coverage report && coverage html

test-ci: ## Continuous integration test suite.
	tox

dev: ## Restarts the example whenever a file changes.
	nodemon -q -e py -w tests -w example.py  -x "clear && python example.py || true"

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

.PHONY: test format check

test:
	@pytest --cov=./scanapi --cov-report=xml

check:
	@black -l 80 --check . --exclude=.venv

format:
	@black -l . --exclude=.venv

install:
	@poetry install
	@pre-commit install
.PHONY: test format check install sh run

test:
	@pytest --cov=./scanapi --cov-report=xml

check:
	@black -l 80 --check . --exclude=.venv

format:
	@black -l . --exclude=.venv

install:
	@poetry install
	@pre-commit install

sh:
	@poetry shell

run:
	@poetry run scanapi

bandit:
	@bandit -r scanapi


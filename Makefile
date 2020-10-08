.PHONY: test format check install sh run

test:
	@pytest --cov=./scanapi --cov-report=xml

check:
	@black -l 80 --check . --exclude=.venv

change-version:
	@poetry version prerelease

format:
	@black -l 80 . --exclude=.venv

install:
	@poetry install
	@pre-commit install

sh:
	@poetry shell

run:
	@poetry run scanapi

bandit:
	@bandit -r scanapi


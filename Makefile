timestamp = `date -u +'%Y.%m.%d.%H%M%S'`

test:
	@pytest --cov=./scanapi --cov-report=xml

black:
	@poetry run black -l 80 --check . --exclude=.venv

flake8:
	@poetry run flake8 --ignore=E501,W501,E231,W503

check: black flake8

change-version:
	@poetry version `poetry version -s | cut -f-3 -d.`.dev$(timestamp)

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

.PHONY: test black flake8 check change-version format install sh run bandit

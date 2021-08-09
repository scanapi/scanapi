timestamp = `date -u +'%Y%m%d%H%M%S'`

test:
	@pytest --cov=./scanapi --cov-report=xml

black:
	@poetry run black -l 80 --check . --exclude=.venv

flake8:
	@poetry run flake8 --ignore=E501,W501,E231,W503

mypy:
	@poetry run mypy scanapi

check: black flake8 mypy gitlint

change-version:
	@poetry version `poetry version -s | cut -f-3 -d.`.dev$(timestamp)

format:
	@black -l 80 . --exclude=.venv

install:
	@poetry install
	@pre-commit install -f -t pre-commit --hook-type commit-msg

sh:
	@poetry shell

run:
	@poetry run scanapi

bandit:
	@bandit -r scanapi

gitlint:
	@poetry run gitlint --ignore-stdin

.PHONY: test black flake8 mypy check change-version format install sh run bandit gitlint

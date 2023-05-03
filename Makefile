timestamp = `date -u +'%Y%m%d%H%M%S'`

.PHONY: test
test:
	@poetry run pytest --cov=./scanapi --cov-report=xml

.PHONY: black
black:
	@echo "running black"
	@poetry run black -l 80 --check . --exclude=.venv

.PHONY: flake8
flake8:
	@echo "running flake8"
	@poetry run flake8 --ignore=E501,W501,E231,W503

.PHONY: mypy
mypy:
	@echo "running mypy"
	@poetry run mypy scanapi

.PHONY: check
check: black flake8 mypy gitlint

.PHONY: change-version
change-version:
	@poetry version `poetry version -s | cut -f-3 -d.`.dev$(timestamp)

.PHONY: format
format:
	@black -l 80 . --exclude=.venv

.PHONY: install
install:
	@poetry install
	@pre-commit install -f -t pre-commit --hook-type commit-msg

.PHONY: sh
sh:
	@poetry shell

.PHONY: run
run:
	@poetry run scanapi

.PHONY: bandit
bandit:
	@bandit -r scanapi

.PHONY: gitlint
gitlint:
	@echo "running gitlint"
	@poetry run gitlint --ignore-stdin

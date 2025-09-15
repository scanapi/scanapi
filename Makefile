timestamp = `date -u +'%Y%m%d%H%M%S'`

.PHONY: test
test:
	@uv run pytest --cov=./scanapi --cov-report=xml

.PHONY: mypy
mypy:
	@echo "running mypy"
	@uv run mypy scanapi

check:
	@echo "running ruff format (apply)"
	@uvx ruff format .
	@echo "running ruff check"
	@uvx ruff check
	@echo "running mypy"
	@uv run mypy scanapi

.PHONY: change-version
change-version:
	@current_version=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	base_version=$$(echo $$current_version | cut -f-3 -d.); \
	new_version="$$base_version.dev$(timestamp)"; \
	sed -i.bak 's/^version = .*/version = "'$$new_version'"/' pyproject.toml && rm pyproject.toml.bak; \
	echo "Updated version to $$new_version"

.PHONY: format
format:
	@uv run black -l 80 . --exclude=.venv

.PHONY: install
install:
	@uv sync --extra dev
	@uv run pre-commit install -f -t pre-commit --hook-type commit-msg

.PHONY: sh
sh:
	@echo "Use 'uv shell' to activate the virtual environment"
	@uv shell

.PHONY: run
run:
	@uv run scanapi

.PHONY: bandit
bandit:
	@uv run bandit -r scanapi


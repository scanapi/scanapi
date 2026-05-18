timestamp = `date -u +'%Y%m%d%H%M%S'`

.PHONY: test
test:
	@uv run pytest --cov=./scanapi --cov-report=xml

.PHONY: lint
lint:
	@echo "running ruff check"
	@uv run ruff check .

.PHONY: mypy
mypy:
	@echo "running mypy"
	@uv run mypy scanapi

.PHONY: check
check: lint mypy

.PHONY: change-version
change-version:
	@current_version=$$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'); \
	base_version=$$(echo $$current_version | cut -f-3 -d.); \
	new_version="$$base_version.dev$(timestamp)"; \
	sed -i.bak 's/^version = .*/version = "'$$new_version'"/' pyproject.toml && rm pyproject.toml.bak; \
	echo "Updated version to $$new_version"

.PHONY: format
format:
	@uv run ruff check --fix .
	@uv run ruff format .

.PHONY: install
install:
	@uv sync --extra dev
	@uv run pre-commit install -f -t pre-commit --hook-type commit-msg

.PHONY: run
run:
	@uv run scanapi

.PHONY: bandit
bandit:
	@uv run bandit -r scanapi

.PHONY: docs-install
docs-install:
	@echo "Installing docs dev dependencies"
	@uv sync --extra dev

.PHONY: docs-serve
docs-serve:
	@echo "Starting mkdocs server (hot-reload)"
	@uv run mkdocs serve

.PHONY: docs-build
docs-build:
	@echo "Building MkDocs site into ./site"
	@uv run mkdocs build

.PHONY: docs-clean
docs-clean:
	@echo "Cleaning generated site directory"
	@rm -rf site

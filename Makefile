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

.PHONY: bump-major-version
bump-major-version:
	@uv version --bump major

# Calculate the next development version from Git tags.
#
# Examples:
#   v2.13.2 + no dev tags        -> 2.13.3.dev0
#   v2.13.2 + v2.13.3.dev0       -> 2.13.3.dev1
#   v2.13.2 + v2.13.3.dev46      -> 2.13.3.dev47
#
# The stable release determines the next patch version, while the latest
# development tag determines the development release number.
.PHONY: next-dev-version
next-dev-version:
	@last_release=$$(git tag --list 'v*' --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$$' | head -n 1); \
	test -n "$$last_release" || { echo "No stable release tag found" >&2; exit 1; }; \
	base_version=$${last_release#v}; \
	next_version=$$(echo "$$base_version" | awk -F. '{print $$1 "." $$2 "." ($$3 + 1)}'); \
	last_dev=$$(git tag --list "v$${next_version}.dev*" --sort=-v:refname | head -n 1); \
	if [ -z "$$last_dev" ]; then \
		dev_number=0; \
	else \
		dev_number=$$(echo "$$last_dev" | sed -E 's/.*\.dev([0-9]+)$$/\1/'); \
		dev_number=$$((dev_number + 1)); \
	fi; \
	echo "$${next_version}.dev$$dev_number"

.PHONY: bump-dev-version
bump-dev-version:
	@version=$$(make --no-print-directory next-dev-version); \
	echo "Setting development version to $$version"; \
	uv version "$$version"

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
	@uv run bandit -r scanapi -v

.PHONY: bandit-report
bandit-report:
	@uv run bandit -r scanapi -f json -o bandit-report.json

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

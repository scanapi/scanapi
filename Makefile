.PHONY: test format check

test:
	@pytest --cov=./scanapi --cov-report=xml

check:
	@black -l 80 --check . --exclude=.venv
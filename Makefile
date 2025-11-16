.PHONY: init-dev format test

init-dev:
	uv venv || true
	uv pip install .[dev]

format:
	uv run black .

test:
	rm -f cov.xml ||:
	uv run pytest -s --cov=otterai \
		--cov-report=lcov:lcov.info \
		--cov-report=xml:cov.xml \
		tests/
	rm -f lcov.info .coverage ||:

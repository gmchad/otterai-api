.PHONY: init-dev format test

init-dev:
    uv venv || true
	uv pip install .[dev]

format:
	uv run black .

test:
	uv run pytest
.PHONY: init-dev format test

init-dev:
	uv pip install .[dev]

format:
	uv run black .

test:
	uv run pytest
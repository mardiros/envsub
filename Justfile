develop:
  uv run maturin develop



test: develop
    uv run pytest -sxv

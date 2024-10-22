default_testsuite:='tests'

develop:
  uv run maturin develop

test testsuite=default_testsuite: develop
    uv run pytest -sxv {{testsuite}}

lf:
    uv run pytest --lf -vvv

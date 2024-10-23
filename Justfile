default_testsuite:='tests'

develop:
  uv run maturin develop

test testsuite=default_testsuite: develop
    uv run pytest -sxv {{testsuite}}

lf:
    uv run pytest --lf -vvv


release: && changelog
    $EDITOR pyproject.toml
    uv sync

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(poetry version -s)"
    poetry build
    poetry publish
    git push
    git tag "$(poetry version -s)"
    git push origin "$(poetry version -s)"

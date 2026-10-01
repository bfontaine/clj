#! /bin/bash -ex
[ ! -f pyproject.toml ] && exit 0

COV_ARGS=""

if [ -n "$HTMLCOV" ]; then
  COV_ARGS="$COV_ARGS --cov-report=html"
fi
if [ -n "$BRANCHCOV" ]; then
  COV_ARGS="$COV_ARGS --cov-branch"
fi

uv run ruff check clj
uv run mypy --strict --check-untyped-defs ./*.py clj/*.py
uv run pytest --cov=. $COV_ARGS tests/

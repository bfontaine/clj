# Contributing to clj

## Run the tests

    poetry run mypy clj tests
    poetry run python tests/test.py

## Release a new version

1. Update the Changelog
2. Bump the version in `clj/__init__.py` and in `pyproject.toml`
3. Ensure the tests pass
4. Commit and tag
5. Wait for the CI job to finish


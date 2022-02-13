# Contributing to clj

## Run the tests

    python3 tests/test.py

## Release a new version

1. Update the Changelog
2. Bump the version in `clj/__init__.py`
3. Ensure the tests pass
4. Commit and tag
5. `rm -rf dist/*`
6. `poetry run python setup.py sdist bdist_wheel`
7. `poetry run twine check dist/*`
8. `poetry run twine upload dist/*`

[More info here](https://packaging.python.org/tutorials/packaging-projects/).

# Contributing to clj

## Run the tests

    python2 tests/test.py
    python3 tests/test.py

## Release a new version

1. Update the Changelog
2. Bump the version in `clj/__init__.py`
3. Ensure the tests pass
4. Commit and tag
5. `python3 setup.py sdist bdist_wheel`
6. `twine upload dist/clj-<version>*`

[More info here](https://packaging.python.org/tutorials/packaging-projects/).

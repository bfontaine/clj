# clj Changelog

No change is breaking unless explicitly stated.

## Unreleased

* Add `clj.partition_by`
* Add `clj.seq_gen` as an equivalent of `seq` that returns a generator rather than a sequence

## 0.3.0 (2022/05/22)

### Breaking change

* `nth` no longer accepts negative indices (this mimicks the Clojure function).

### Other changes

* `nth` doesn’t try to consume its argument if a negative index is given.
  The type hint of the parameter `not_found` is now correct.
* Ensure `clj/py.typed` is included in the package
* Eliminate an internal function call in `is_odd`
* Improve some type hints
* Remove deprecated `setup.py`

## 0.2.1 (2022/02/14)

* Add `clj/py.typed` to indicate we support type checking (PEP 561)
* Fix the version in `pyproject.toml`

## 0.2.0 (2022/02/14)

### Breaking changes

* Drop support for Python 2.x
* Drop support for Python 3.6 and below
* No longer accept `None` as a valid parameter for `first`

### Other changes

* Add type hints to most functions
* Add `is_even` and `is_odd`
* Make `shuffle` work on all iterables, not just lists
* Document the behavior of `last` on empty iterables
* Add `pyproject.toml` to the package

## 0.1.6 (2021/04/09)

* Add `partition` (partial implementation)
* Remove deprecation notices.

## 0.1.5 (2020/08/21)

* Add `dedupe` (contributed by @jaihindhreddy)

## 0.1.4 (2020/07/14)

* Add `reverse`

## 0.1.3 (2019/07/04)

* Add lazy implementations of `map` and `filter` in Python 2
* Fix `split_at` and `split_with` that would try (and fail) to consume twice
  their input.

## 0.1.2 (2019/03/08)

* Add `seqs.tree_seq`, `seqs.empty`
* Import everything in `clj` as well so one can use `clj.inc` or `clj.first`;
  no need to import sub-modules anymore.

## 0.1.1 (2018/01/12)

* Add `fns.juxt`, `fns.inc`, `fns.dec`
* Fix an infinite loop in `seqs.cycle` when a generator was passed
* Fix `setup.py` issues when `LANG` isn’t set (contributed by @tdhopper)

## 0.1.0 (2016/09/08)

Initial release.

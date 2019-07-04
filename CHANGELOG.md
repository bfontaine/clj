# clj Changelog

No change is breaking unless explicitely stated.

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

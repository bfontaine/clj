# clj

`clj` is a Python module for those times when you did too much Clojure and
came back to Python thinking where are all these `distinct`, `drop-while`,
`cycle`, `first`, etc.

## Install

    pip install clj

## Usage

Functions on sequences are in `clj.seqs`; functions that operate on functions
are in `clj.fns`.

### Example

```clojure
;; Clojure
(println (count (distinct (filter even? (map inc coll)))))
```

```python
# Python
from clj.seqs import count, distinct
from clj.fns import inc

even = lambda e: ~e&1

print(count(distinct(filter(even, map(inc, coll)))))
```

Note that `count()` works on both sequences in generators; in the latter case
it doesn’t load everything in memory like e.g. `len(list(g))` would do.

## Core Ideas

* Lazy by default. All functions should work on arbitrary iterators and
  return generators.
* This is Python. We keep Python’s semantics instead of trying to reproduce
  Clojure in Python (e.g. `0` and `[]` are logically true in Clojure but false
  in Python; `None` is not equivalent to an empty collection).
* Don’t Reinvent the Wheel. Python already provides things like `map` and
  `filter`. We don’t reimplement them unless they miss something (e.g. Python’s
  `range` can’t be called without argument to yield an infinite sequence).

## Support

### Sequences (`clj.seqs`)

`clj.seqs` aims to implement all Clojure functions that operate on sequences
(see [the list here][seqs]).
They all work on iterables and return generators by default (Python’s closest
equivalent of lazy seqs). We don’t support transducers.

[seqs]: http://clojure.org/reference/sequences

| Clojure           | `clj.seqs`      | Comment                          |
|-------------------|:----------------|----------------------------------|
| `distinct`        | `distinct`      |                                  |
| `filter`          | -               | Use Python’s built-in `filter`.  |
| `remove`          | `remove`        |                                  |
| `for`             | -               | Use `for … in`.                  |
| `keep`            | `keep`          |                                  |
| `keep-indexed`    | `keep_indexed`  |                                  |
| `cons`            | `cons`          |                                  |
| `concat`          | `concat`        |                                  |
| `lazy-cat`        | -               | Use `concat`.                    |
| `mapcat`          | `mapcat`        |                                  |
| `cycle`           | `cycle`         |                                  |
| `interleave`      | `interleave`    |                                  |
| `interpose`       | `interpose`     |                                  |
| `rest`            | `rest`          |                                  |
| `next`            | -               | Use `rest`.                      |
| `fnext`           | -               | Use `second`.                    |
| `nnext`           | -               | Use `rest(rest(…))`              |
| `drop`            | `drop`          |                                  |
| `drop-while`      | `drop_while`    |                                  |
| `nthnext`         | -               |                                  |
| `take`            | `take`          |                                  |
| `take-nth`        | `take_nth`      |                                  |
| `take-while`      | `take_while`    |                                  |
| `butlast`         | `butlast`       |                                  |
| `drop-last`       | `drop_last`     |                                  |
| `flatten`         | `flatten`       |                                  |
| `reverse`         | -               | Use Python’s `reversed`.         |
| `sort`            | -               | Use Python’s built-in `sort`.    |
| `sort-by`         | -               | Use `sort(…, key=your_function)`.|
| `shuffle`         | `shuffle`       |                                  |
| `split-at`        | `split_at`      |                                  |
| `split-with`      | `split_with`    |                                  |
| `partition`       |                 |                                  |
| `partition-all`   |                 |                                  |
| `partition-by`    |                 |                                  |
| `map`             | -               | Use Python’s built-in `map`.     |
| `pmap`            | -               |                                  |
| `replace`         | `replace`       |                                  |
| `reductions`      | `reductions`    | `(reductions f i c)` becomes `reductions(f, c, i)` |
| `map-indexed`     | `map_indexed`   |                                  |
| `seque`           | -               |                                  |
| `first`           | `first`         |                                  |
| `ffirst`          | `ffirst`        |                                  |
| `nfirst`          | `nfirst`        |                                  |
| `second`          | `second`        |                                  |
| `nth`             | `nth`           |                                  |
| `when-first`      | -               | (macro)                          |
| `last`            | `last`          |                                  |
| `rand-nth`        | -               | Use Python’s `random.choice`.    |
| `zipmap`          | `zipmap`        |                                  |
| `into`            | -               |                                  |
| `reduce`          | -               | Use Python’s built-in `reduce`.  |
| `set`             | -               | Use Python’s `set`.              |
| `vec`             | -               | Use Python’s `list`.             |
| `into-array`      | -               | Use Python’s `list`.             |
| `to-array-2d`     | -               |                                  |
| `frequencies`     | -               | Use Python’s `collections.Counter`.|
| `group-by`        | `group_by`      |                                  |
| `apply`           | -               | Use the `f(*args)` construct.    |
| `not-empty`       | -               |                                  |
| `some`            | `some`          |                                  |
| `seq?`            | `is_seq`        |                                  |
| `every?`          | `every`         |                                  |
| `not-every?`      | `not_every`     |                                  |
| `not-any?`        | `not_any`       |                                  |
| `empty?`          | -               |                                  |
| `doseq`           | -               | Use `for … in`                   |
| `dorun`           | `dorun`         |                                  |
| `doall`           | -               | Use Python’s `list`.             |
| `realized?`       | -               |                                  |
| `seq`             | -               |                                  |
| `vals`            | -               | Use Python’s `dict.values`.      |
| `keys`            | -               | Use Python’s `dict.keys`.        |
| `rseq`            | -               |                                  |
| `subseq`          |                 |                                  |
| `rsubseq`         |                 |                                  |
| `lazy-seq`        | -               | (macro)                          |
| `repeatedly`      | `repeatedly`    |                                  |
| `iterate`         | `iterate`       |                                  |
| `repeat`          | `repeat`        | `(repeat n x)` becomes `repeat(x, n)`.|
| `range`           | `range`         | Prefer Python’s `range` for everything but infinite generators.|
| `line-seq`        | -               | Loop over an `io.BufferedReader`.|
| `resultset-seq`   | -               |                                  |
| `re-seq`          | -               | Use Python’s `re.finditer`.      |
| `tree-seq`        | -               |                                  |
| `file-seq`        | -               |                                  |
| `xml-seq`         | -               |                                  |
| `iterator-seq`    | -               |                                  |
| `enumeration-seq` | -               |                                  |

We also implemented `count`, which uses Python’s `len` when possible and
fallbacks on a `for` loop for other cases.

### Functions (`clj.fns`)

`clj.fns` defines miscellaneous functions as well as functions that work on
functions.

| Clojure           | `clj.fns`       | Comment                          |
|-------------------|:----------------|----------------------------------|
| `identity`        | `identity`      |                                  |
| `partial`         | -               | Use Python’s `functools.partial` |
| `comp`            | `comp`          |                                  |
| `complement`      | `complement`    |                                  |
| `constantly`      | `constantly`    |                                  |
| `juxt`            | `juxt`          |                                  |

| Clojure           | `clj.fns`       | Comment                          |
|-------------------|:----------------|----------------------------------|
| `inc`             | `inc`           |                                  |
| `dec`             | `dec`           |                                  |

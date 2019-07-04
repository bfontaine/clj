# clj

`clj` is a Python module for those times when you did too much Clojure and
came back to Python thinking where are all these `distinct`, `drop-while`,
`cycle`, `first`, etc.

## Install

    pip install clj

## Usage

### Example

```clojure
;; Clojure
(println (count (distinct (filter even? (map inc coll)))))
```

```python
# Python
from clj import count, distinct, filter, inc, map

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
* Don’t Reinvent the Wheel. We don’t reimplement built-in functions
  unless they miss something: `range` because it can’t be called without
  argument to yield an infinite sequence; `map` and `filter` in Python 2
  because they aren’t lazy.

## Support

The general naming scheme is: use underscores instead of hyphens; start the
function with `is_` if its Clojure counterparts ends with a `?`.

### Sequences

We aim to implement all Clojure functions that operate on sequences
(see [the list here][seqs]).
They all work on iterables and return generators by default (Python’s closest
equivalent of lazy seqs). We don’t support transducers.

[seqs]: http://clojure.org/reference/sequences

| Clojure           | `clj`           | Comment                          |
|-------------------|:----------------|----------------------------------|
| `distinct`        | `distinct`      |                                  |
| `filter`          | `filter`        |                                  |
| `remove`          | `remove`        |                                  |
| `keep`            | `keep`          |                                  |
| `keep-indexed`    | `keep_indexed`  |                                  |
| `cons`            | `cons`          |                                  |
| `concat`          | `concat`        | Deprecated. Use Python’s `itertools.chain` |
| `lazy-cat`        | -               | Use Python’s `itertools.chain`   |
| `mapcat`          | `mapcat`        |                                  |
| `cycle`           | `cycle`         |                                  |
| `interleave`      | `interleave`    |                                  |
| `interpose`       | `interpose`     |                                  |
| `rest`            | `rest`          |                                  |
| `next`            | -               | Use `rest`.                      |
| `fnext`           | -               | Use `second`.                    |
| `nnext`           | -               | Use `rest(rest(…))`              |
| `drop`            | `drop`          |                                  |
| `drop-while`      | `drop_while`    | Deprecated. Use Python’s `itertools.dropwhile` |
| `nthnext`         | -               | Use `drop`.                      |
| `take`            | `take`          |                                  |
| `take-nth`        | `take_nth`      |                                  |
| `take-while`      | `take_while`    | Deprecated. Use Python’s `itertools.takewhile` |
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
| `map`             | `map`           |                                  |
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
| `empty`           | `empty`         |                                  |
| `doseq`           | -               | Use `for … in`.                  |
| `dorun`           | `dorun`         |                                  |
| `doall`           | -               | Use Python’s `list`.             |
| `realized?`       | -               |                                  |
| `seq`             | -               |                                  |
| `vals`            | -               | Use Python’s `dict.values`.      |
| `keys`            | -               | Use Python’s `dict.keys`.        |
| `rseq`            | -               |                                  |
| `subseq`          |                 |                                  |
| `rsubseq`         |                 |                                  |
| `repeatedly`      | `repeatedly`    |                                  |
| `iterate`         | `iterate`       |                                  |
| `repeat`          | `repeat`        | `(repeat n x)` becomes `repeat(x, n)`.|
| `range`           | `range`         | Prefer Python’s `range` for everything but infinite generators.|
| `line-seq`        | -               | Loop over an `io.BufferedReader`.|
| `resultset-seq`   | -               |                                  |
| `re-seq`          | -               | Use Python’s `re.finditer`.      |
| `tree-seq`        | `tree_seq`      |                                  |
| `file-seq`        | -               | Use Python’s `os.walk`.          |
| `xml-seq`         | -               |                                  |
| `iterator-seq`    | -               |                                  |
| `enumeration-seq` | -               |                                  |
| `hash-map`        | -               | Use Python’s `dict`.             |
| `array-map`       | -               | Use Python’s `dict`.             |
| `sorted-map`      | -               | Use `collections.OrderedDict`.   |
| `sorted-map-by`   |                 |                                  |
| `hash-set`        | -               | Use Python’s `set`.              |
| `set`             | -               | Use Python’s `set`.              |
| `sorted-set`      |                 |                                  |
| `sorted-set-by`   |                 |                                  |
| `dedupe`          |                 |                                  |

We also implemented `count`, which uses Python’s `len` when possible and
fallbacks on a `for` loop for other cases.

### Functions

We also provide miscellaneous functions as well as functions that work on
functions.

| Clojure           | `clj`           | Comment                          |
|-------------------|:----------------|----------------------------------|
| `identity`        | `identity`      |                                  |
| `partial`         | -               | Use Python’s `functools.partial` |
| `comp`            | `comp`          |                                  |
| `complement`      | `complement`    |                                  |
| `constantly`      | `constantly`    |                                  |
| `juxt`            | `juxt`          |                                  |
| `distinct?`       | `is_distinct`   |                                  |

| Clojure           | `clj`           | Comment                          |
|-------------------|:----------------|----------------------------------|
| `inc`             | `inc`           |                                  |
| `dec`             | `dec`           |                                  |

# clj

`clj` is a Python module for those times when you did too much Clojure and
came back to Python thinking where are all these `distinct`, `drop-while`,
`cycle`, `first`, etc.

## Core Ideas

* This is Python. We keep Python’s semantics instead of trying to reproduce
  Clojure in Python (e.g. `0` and `[]` are logically true in Clojure but false
  in Python).
* Don’t Reinvent the Wheel. Python already provides things like `map` and
  `filter`. We don’t reimplement them unless they miss something (e.g. Python’s
  `range` can’t be called without argument to yield an infinite sequence).

## Support

### Sequences (`clj.seqs`)

`clj.seqs` aim to implement all Clojure functions that operate on sequences
(see [the list here][seqs]).
They all work on iterables and return generators by default (Python’s closest
equivalent of lazy seqs).

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
| `drop-last`       | `drop_last`     | Use `butlast` if `n` is 1.       |
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
| `replace`         |                 |                                  |
| `reductions`      |                 |                                  |
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
| `frequencies`     | `frequencies`   |                                  |
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
| `repeat`          | `repeat`        | `(repeat n x)` becomes `repeat(x, n)`|
| `range`           |                 |                                  |
| `line-seq`        |                 |                                  |
| `resultset-seq`   | -               |                                  |
| `re-seq`          |                 |                                  |
| `tree-seq`        |                 |                                  |
| `file-seq`        | -               |                                  |
| `xml-seq`         | -               |                                  |
| `iterator-seq`    | -               |                                  |
| `enumeration-seq` | -               |                                  |

### Functions (`clj.fns`)

`clj.fns` defines functions that work on functions.

| Clojure           | `clj.fns`       | Comment                          |
|-------------------|:----------------|----------------------------------|
| `partial`         | -               | Use Python’s `functools.partial` |
| `comp`            | `comp`          |                                  |
| `complement`      | `complement`    |                                  |
| `constantly`      | `constantly`    |                                  |

# cljseqs

`cljseqs` is a Python module for those times when you did too much Clojure and
came back to Python thinking where are all these `group_by`, `first`, `take`,
etc.

| Clojure           | `cljseq`  | Remark   |
|-------------------|:---------:|----------|
| `distinct`        |           |          |
| `filter`          |           |          |
| `remove`          |           |          |
| `for`             | -         |          |
| `keep`            |           |          |
| `keep-indexed`    |           |          |
| `cons`            |           |          |
| `concat`          |           |          |
| `lazy-cat`        |           |          |
| `mapcat`          |           |          |
| `cycle`           |           |          |
| `interleave`      |           |          |
| `interpose`       |           |          |
| `rest`            |           |          |
| `next`            |           |          |
| `fnext`           |           |          |
| `nnext`           |           |          |
| `drop`            |           |          |
| `drop-while`      |           |          |
| `nthnext`         |           |          |
| `take`            |           |          |
| `take-nth`        |           |          |
| `take-while`      |           |          |
| `butlast`         |           |          |
| `drop-last`       |           |          |
| `flatten`         |           |          |
| `reverse`         |           |          |
| `sort`            | -         | Use Python’s built-in `sort`. |
| `sort-by`         | -         | Use Python’s built-in `sort` with a `key`. |
| `shuffle`         |           |          |
| `split-at`        |           |          |
| `split-with`      |           |          |
| `partition`       |           |          |
| `partition-all`   |           |          |
| `partition-by`    |           |          |
| `map`             | -         | Use Python’s built-in `map`. |
| `pmap`            |           |          |
| `mapcat`          |           |          |
| `replace`         |           |          |
| `reductions`      |           |          |
| `map-indexed`     |           |          |
| `seque`           |           |          |
| `first`           | `first`   |          |
| `ffirst`          |           |          |
| `nfirst`          |           |          |
| `second`          | `second`  |          |
| `nth`             | `nth`     |          |
| `when-first`      |           |          |
| `last`            | `last`    |          |
| `rand-nth`        |           |          |
| `zipmap`          |           |          |
| `into`            |           |          |
| `reduce`          |           |          |
| `set`             |           |          |
| `vec`             |           |          |
| `into-array`      |           |          |
| `to-array-2d`     |           |          |
| `frequencies`     |           |          |
| `group-by`        | `group_by`|          |
| `apply`           |           |          |
| `not-empty`       |           |          |
| `some`            |           |          |
| `reduce`          |           |          |
| `seq?`            |           |          |
| `every?`          |           |          |
| `not-every?`      |           |          |
| `not-any?`        |           |          |
| `empty?`          |           |          |
| `some`            |           |          |
| `filter`          |           |          |
| `doseq`           |           |          |
| `dorun`           |           |          |
| `doall`           |           |          |
| `realized?`       |           |          |
| `seq`             |           |          |
| `vals`            |           |          |
| `keys`            | `keys`    |          |
| `rseq`            |           |          |
| `subseq`          |           |          |
| `rsubseq`         |           |          |
| `lazy-seq`        |           |          |
| `repeatedly`      |           |          |
| `iterate`         |           |          |
| `repeat`          |           |          |
| `range`           |           |          |
| `line-seq`        |           |          |
| `resultset-seq`   |           |          |
| `re-seq`          |           |          |
| `tree-seq`        |           |          |
| `file-seq`        |           |          |
| `xml-seq`         |           |          |
| `iterator-seq`    |           |          |
| `enumeration-seq` |           |          |

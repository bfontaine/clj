# cljseqs

`cljseqs` is a Python module for those times when you did too much Clojure and
came back to Python thinking where are all these `distinct`, `drop-while`,
`cycle`, `first`, etc.

## Support

| Clojure           | `cljseq`        | Remark                                     |
|-------------------|:----------------|--------------------------------------------|
| `distinct`        | `distinct`      |                                            |
| `filter`          | -               | Use Python’s built-in `filter`.            |
| `remove`          | `remove`        |                                            |
| `for`             | -               | Use `for … in`.                            |
| `keep`            | `keep`          |                                            |
| `keep-indexed`    | `keep_indexed`  |                                            |
| `cons`            | `cons`          |                                            |
| `concat`          | `concat`        |                                            |
| `lazy-cat`        | -               | Use `concat`.                              |
| `mapcat`          | `mapcat`        |                                            |
| `cycle`           | `cycle`         |                                            |
| `interleave`      | `interleave`    |                                            |
| `interpose`       | `interpose`     |                                            |
| `rest`            | `rest`          |                                            |
| `next`            | -               | Use `rest`.                                |
| `fnext`           | -               | Use `second`.                              |
| `nnext`           | -               | Use `rest(rest(…))`                        |
| `drop`            | `drop`          |                                            |
| `drop-while`      | `drop_while`    |                                            |
| `nthnext`         | -               |                                            |
| `take`            | `take`          |                                            |
| `take-nth`        | `take_nth`      |                                            |
| `take-while`      | `take_while`    |                                            |
| `butlast`         | `butlast`       |                                            |
| `drop-last`       | `drop_last`     | Use `butlast` if `n` is 1.                 |
| `flatten`         |                 |                                            |
| `reverse`         |                 |                                            |
| `sort`            | -               | Use Python’s built-in `sort`.              |
| `sort-by`         | -               | Use Python’s built-in `sort` with a `key`. |
| `shuffle`         |                 |                                            |
| `split-at`        |                 |                                            |
| `split-with`      |                 |                                            |
| `partition`       |                 |                                            |
| `partition-all`   |                 |                                            |
| `partition-by`    |                 |                                            |
| `map`             | -               | Use Python’s built-in `map`.               |
| `pmap`            |                 |                                            |
| `mapcat`          |                 |                                            |
| `replace`         |                 |                                            |
| `reductions`      |                 |                                            |
| `map-indexed`     |                 |                                            |
| `seque`           |                 |                                            |
| `first`           | `first`         |                                            |
| `ffirst`          |                 |                                            |
| `nfirst`          |                 |                                            |
| `second`          | `second`        |                                            |
| `nth`             | `nth`           |                                            |
| `when-first`      |                 |                                            |
| `last`            | `last`          |                                            |
| `rand-nth`        |                 |                                            |
| `zipmap`          |                 |                                            |
| `into`            |                 |                                            |
| `reduce`          |                 |                                            |
| `set`             |                 |                                            |
| `vec`             |                 |                                            |
| `into-array`      |                 |                                            |
| `to-array-2d`     |                 |                                            |
| `frequencies`     |                 |                                            |
| `group-by`        | `group_by`      |                                            |
| `apply`           |                 |                                            |
| `not-empty`       |                 |                                            |
| `some`            |                 |                                            |
| `reduce`          |                 |                                            |
| `seq?`            |                 |                                            |
| `every?`          |                 |                                            |
| `not-every?`      |                 |                                            |
| `not-any?`        |                 |                                            |
| `empty?`          |                 |                                            |
| `some`            |                 |                                            |
| `filter`          |                 |                                            |
| `doseq`           |                 |                                            |
| `dorun`           |                 |                                            |
| `doall`           |                 |                                            |
| `realized?`       |                 |                                            |
| `seq`             |                 |                                            |
| `vals`            | -               | Use Python’s `dict.values`                 |
| `keys`            | -               | Use Python’s `dict.keys`                   |
| `rseq`            |                 |                                            |
| `subseq`          |                 |                                            |
| `rsubseq`         |                 |                                            |
| `lazy-seq`        |                 |                                            |
| `repeatedly`      |                 |                                            |
| `iterate`         |                 |                                            |
| `repeat`          |                 |                                            |
| `range`           |                 |                                            |
| `line-seq`        |                 |                                            |
| `resultset-seq`   |                 |                                            |
| `re-seq`          |                 |                                            |
| `tree-seq`        |                 |                                            |
| `file-seq`        |                 |                                            |
| `xml-seq`         |                 |                                            |
| `iterator-seq`    |                 |                                            |
| `enumeration-seq` |                 |                                            |

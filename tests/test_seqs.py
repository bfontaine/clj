import re
from collections import OrderedDict, Counter, deque, defaultdict
from typing import Iterable, Any, cast, Union

import pytest

import clj as c

IntNode = Union[int, list["IntNode"]]
StrNode = Union[str, list["StrNode"]]


def infinite_range_fn():
    """
    Test generator that fails if its 10k-th element is consumed.
    """
    n = 0
    while True:
        yield n
        n += 1
        assert n <= 10000


def list_(x: Any) -> list:
    # Fix a typing warning from IntelliJ when using map(list, ...)
    return list(x)


@pytest.fixture(scope="session")
def infinite_range():
    return infinite_range_fn


def test_distinct():
    assert c.distinct(infinite_range_fn()) is not None
    assert list(c.distinct([])) == []
    assert list(c.distinct([1])) == [1]
    assert list(c.distinct([1, 2, 3, 4])) == [1, 2, 3, 4]
    assert list(c.distinct([2, 1, 3, 1, 2, 3])) == [2, 1, 3]


def test_filter():
    assert c.filter(lambda _: True, infinite_range_fn()) is not None


def test_remove():
    assert c.remove(lambda _: False, infinite_range_fn()) is not None
    assert list(c.remove(lambda _: True, [])) == []
    assert list(c.remove(lambda _: True, [1, 2, 3, 4])) == []
    assert list(c.remove(lambda _: False, [1, 2, 3])) == [1, 2, 3]
    assert list(c.remove(lambda x: x == 2, [1, 2, 3])) == [1, 3]


def test_keep():
    assert c.keep(lambda _: False, infinite_range_fn()) is not None
    assert list(c.keep(lambda _: True, [])) == []
    assert list(c.keep(lambda _: None, [])) == []
    assert list(c.keep(lambda _: None, [1, 2, 3])) == []
    assert list(c.keep(lambda _: False, [1, 2])) == [False, False]
    assert list(c.keep(lambda x: x, [1, None, 2])) == [1, 2]


def test_keep_indexed():
    assert c.keep_indexed(lambda a, b: False, infinite_range_fn()) is not None

    def f(i, e): return e if i % 2 == 0 else None

    assert list(c.keep_indexed(f, ["a", "b", "c", "d"])) \
           == ["a", "c"]


def test_cons():
    assert c.cons(1, infinite_range_fn()) is not None
    assert c.first(c.cons(1, infinite_range_fn())) == 1
    assert list(c.cons(1, [])) == [1]
    assert list(c.cons([], [])) == [[]]
    assert list(c.cons(5, [1])) == [5, 1]


def test_concat():
    assert c.concat(infinite_range_fn()) is not None
    assert c.concat(infinite_range_fn(), infinite_range_fn()) is not None
    assert list(c.concat()) == []
    assert list(c.concat([])) == []
    assert list(c.concat([], [], [], [])) == []
    assert list(c.concat([1, 2], [])) == [1, 2]
    assert list(c.concat([1, 2], [3])) == [1, 2, 3]


def test_map():
    assert c.map(lambda e: e, infinite_range_fn()) is not None
    assert list(c.map(lambda e: e + 1, range(3))) == [1, 2, 3]

    def plus(*xs):
        return sum(xs)

    assert list(c.map(plus, [1, 2, 3], [2, 3, 4, 5], [6, 7])) == [9, 12]


def test_mapcat():
    def f(s): return s.split(",")

    assert list(c.mapcat(f, ["a,b", "c,d"])) \
           == ["a", "b", "c", "d"]

    g = c.mapcat(reversed, [[3, 2, 1, 0], [6, 5, 4], [9, 8, 7]])
    assert list(g) == list(range(10))
    assert c.mapcat(lambda _: infinite_range_fn(), [1, 2, 3]) is not None


def test_cycle():
    assert list(c.take(8, c.cycle([1, 2, 3]))) \
           == [1, 2, 3, 1, 2, 3, 1, 2]
    assert list(c.take(4, c.cycle(x for x in range(1, 3)))) \
           == [1, 2, 1, 2]
    assert c.cycle(infinite_range_fn()) is not None


def test_interleave():
    assert c.interleave(infinite_range_fn(), infinite_range_fn()) is not None
    assert list(c.take(7,
                       c.interleave(c.repeat(1),
                                    c.repeat(2),
                                    c.repeat(3)))) \
           == [1, 2, 3, 1, 2, 3, 1]

    assert list(c.interleave(range(2), range(500, 1000))) \
           == [0, 500, 1, 501]

    assert list(c.interleave(range(500, 1000), range(2))) \
           == [500, 0, 501, 1]


def test_interpose():
    assert c.interpose(42, infinite_range_fn()) is not None
    assert list(c.interpose(",", [])) == []
    assert list(c.interpose(",", ["foo"])) == ["foo"]
    assert list(c.interpose(", ", ["foo", "bar"])) \
           == ["foo", ", ", "bar"]


def test_rest():
    assert c.rest(infinite_range_fn()) is not None
    assert list(c.rest([])) == []
    assert list(c.rest([1])) == []
    assert list(c.rest([1, 2, 3, 4])) == [2, 3, 4]


def test_drop():
    assert c.drop(10, infinite_range_fn()) is not None
    assert list(c.drop(10, cast(Iterable, None))) == []
    assert list(c.drop(0, [])) == []
    assert list(c.drop(1000, [])) == []
    assert list(c.drop(1000, [1, 2, 3, 4])) == []
    assert list(c.drop(0, [1, 2, 3, 4])) == [1, 2, 3, 4]
    assert list(c.drop(-3, [1, 2, 3, 4])) == [1, 2, 3, 4]
    assert list(c.drop(3, [1, 2, 3, 4])) == [4]


def test_drop_while():
    assert c.drop_while(lambda _: True, infinite_range_fn()) is not None
    assert list(c.drop_while(lambda _: True, [])) == []
    assert list(c.drop_while(lambda _: True, [1, 2, 3])) == []
    assert list(c.drop_while(lambda n: n < 3, [1, 2, 3, 1])) \
           == [3, 1]


def test_take():
    assert c.take(int(1e12), infinite_range_fn()) is not None
    assert list(c.take(40, [])) == []
    assert list(c.take(0, [1, 2, 3])) == []
    assert list(c.take(2, [1, 2, 3])) == [1, 2]
    assert list(c.take(3, [1, 2, 3])) == [1, 2, 3]
    assert list(c.take(4, [1, 2, 3])) == [1, 2, 3]

    els = []

    def _gen():
        for x in range(10):
            els.append(x)
            yield x

    c.dorun(c.take(0, _gen()))
    assert els == []

    assert list(c.take(5, _gen())) == els


def test_take_nth():
    ls = [42, 25, 17, 1, 34, 87]
    assert list(c.take(3, c.take_nth(0, [1, 2]))) == [1, 1, 1]
    assert list(c.take(3, c.take_nth(-1, [1, 2]))) == [1, 1, 1]
    assert list(c.take_nth(1, ls)) == ls
    assert list(c.take_nth(2, c.interleave(ls, range(20)))) == ls


def test_take_while():
    assert c.take_while(lambda _: True, infinite_range_fn()) is not None
    assert list(c.take_while(lambda _: True, [])) == []
    assert list(c.take_while(lambda _: False, [1, 2, 3])) == []
    assert list(c.take_while(lambda n: n < 3, [1, 2, 3, 1])) == [1, 2]


def test_butlast():
    assert c.butlast(infinite_range_fn()) is not None
    assert list(c.butlast([])) == []
    assert list(c.butlast([1])) == []
    assert list(c.butlast([1, 2])) == [1]
    assert list(c.butlast([1, 2, 3, 4])) == [1, 2, 3]


def test_drop_last():
    assert list(c.drop_last(0, [])) == []
    assert list(c.drop_last(1, [])) == []
    assert list(c.drop_last(1000, [])) == []
    assert list(c.drop_last(-1, [1, 2])) == [1, 2]
    assert list(c.drop_last(-5, [1, 2])) == [1, 2]
    assert list(c.drop_last(2, [1, 2])) == []
    assert list(c.drop_last(3, [1, 2, 3, 4, 5])) == [1, 2]


@pytest.mark.parametrize("xs, expected", [
    ([], []),
    ((), []),
    ({}, []),
    (set(), []),
    ([[], [[[[], []], []]]], []),
    ([1], [1]),
    ([1, 2], [1, 2]),
    ([[], [1]], [1]),
    ([[], [1, [[[], [2, 3]], []], 4]], [1, 2, 3, 4]),
    ([1, (n for n in range(2, 3 + 1)), 4], [1, 2, 3, 4]),
    ([(), 1, [2, [3, 4], 5, []], 6, 7], [1, 2, 3, 4, 5, 6, 7]),
    ([c.range(2) for _ in range(3)] + [2], [0, 1, 0, 1, 0, 1, 2]),
    (["foo", "bar"], ["foo", "bar"]),
    (["a", ["bc", 3, ["d"], "e"], False], ["a", "bc", 3, "d", "e", False]),
])
def test_flatten(xs, expected):
    assert list(c.flatten(xs)) == expected


def test_flatten_infinite_generators():
    assert list(c.take(3, c.flatten(c.range()))) == [0, 1, 2], \
        "infinite generator"
    assert list(c.take(3, c.flatten(c.range() for _ in c.range()))) == [0, 1, 2], \
        "infinite generator of infinite generators"
    assert list(c.take(3, c.flatten([[1], c.range(), 42, c.range()]))) == [1, 0, 1], \
        "mix of single elements and infinite generators"


def test_flatten_deep_list():
    deep_list: list[Any] = ["foo"]
    for _ in range(200):
        deep_list = [[[[[deep_list]]]]]

    assert list(c.flatten(deep_list)) == ["foo"]


def test_reverse():
    assert list(c.reverse([])) == []
    assert list(c.reverse([1, 2, 3])) == [3, 2, 1]
    assert list(c.reverse(c.range(3))) == [2, 1, 0]


def test_shuffle():
    assert list(c.shuffle([])) == []
    assert list(c.shuffle(c.range(0))) == []
    assert sorted(list(c.shuffle({1, 2, 3}))) == [1, 2, 3]

    ls = [1, 2, 3, 4]
    ls_orig = ls[:]
    assert list(sorted(c.shuffle(ls))) == ls
    assert ls == ls_orig  # ensure it's not modified


def test_split_at():
    assert list(map(list_, c.split_at(0, []))) == [[], []]
    assert list(map(list_, c.split_at(1, []))) == [[], []]
    assert list(map(list_, c.split_at(1, [1, 2, 3]))) == [[1], [2, 3]]

    gen = (e for e in range(1, 7))
    assert list(map(list_, c.split_at(3, gen))) == [[1, 2, 3], [4, 5, 6]]
    assert list(c.split_at(2, infinite_range_fn())[0]) == [0, 1]


def test_split_with():
    assert list(map(list_, c.split_with(lambda _: True, []))) \
           == [[], []]
    assert list(map(list_, c.split_with(lambda _: False, []))) \
           == [[], []]
    assert list(map(list_, c.split_with(lambda n: n < 3,
                                        [1, 2, 3, 4, 3, 2, 1]))) \
           == [[1, 2], [3, 4, 3, 2, 1]]

    gen = (e for e in range(1, 5))
    assert list(map(list_, c.split_with(lambda n: n % 2 == 1, gen))) \
           == [[1], [2, 3, 4]]

    assert list(c.split_with(lambda n: n < 2,
                             infinite_range_fn())[0]) == [0, 1]


def test_replace():
    assert c.replace({0: 1}, infinite_range_fn()) is not None
    assert list(c.replace({}, [])) == []
    assert list(c.replace({"a": "b"}, [])) == []
    assert list(c.replace({"a": "b"}, ["b"])) == ["b"]
    assert list(c.replace({"a": "b"}, ["a"])) == ["b"]
    assert list(c.replace({"a": "b"}, ["c"])) == ["c"]
    assert list(c.replace({"a": "b",
                           "b": "c"}, ["a"])) == ["b"]


def test_map_indexed():
    assert c.map_indexed(lambda i, e: e, infinite_range_fn()) is not None
    assert list(c.map_indexed(lambda i, e: 42, [])) == []
    assert list(c.map_indexed(lambda i, e: i, [5, 3, 1])) \
           == [0, 1, 2]
    assert list(c.map_indexed(lambda i, e: i + e, [5, 3, 1])) \
           == [5, 4, 3]


def test_first():
    assert c.first([]) is None
    assert c.first([42]) == 42
    assert c.first([42, 1, 2, 3]) == 42
    assert c.first(infinite_range_fn()) == 0


def test_ffirst():
    assert c.ffirst([]) is None
    assert c.ffirst([[]]) is None
    assert c.ffirst([[42, 1], [3]]) == 42


def test_nfirst():
    assert list(c.nfirst([])) == []
    assert list(c.nfirst([[]])) == []
    assert list(c.nfirst([[1, 2, 3], [4]])) == [2, 3]


def test_second():
    assert c.second([]) is None
    assert c.second([42]) is None
    assert c.second([42, 1, 2, 3]) == 1
    assert c.second(infinite_range_fn()) == 1


def test_nth():
    nope = object()
    assert c.nth([], 0, nope) == nope
    assert c.nth([1, 2, 3, 4], -1, nope) == nope
    assert c.nth(c.range(999999999), -2, nope) == nope
    assert c.nth([], 1, nope) == nope

    assert c.nth([42, 1, 2, 3], 1) == 1
    assert c.nth([42, 1, 2, 3], 6, 7) == 7

    assert c.nth(infinite_range_fn(), 20) == 20


def test_last():
    assert c.last([]) is None
    assert c.last([1]) == 1
    assert c.last([1, 2]) == 2


def test_zipmap():
    assert c.zipmap([], []) == {}
    assert c.zipmap([], infinite_range_fn()) == {}
    assert c.zipmap(infinite_range_fn(), []) == {}
    assert c.zipmap(("a",), [1]) == {"a": 1}
    assert c.zipmap(["b", "a"], [2, 1]) \
           == {"a": 1, "b": 2}


def test_group_by():
    assert c.group_by(lambda e: e % 10, []) == {}
    assert c.group_by(lambda e: e % 10, [1]) == {1: [1]}
    assert c.group_by(lambda e: e % 10, [1, 5001, 3]) \
           == {1: [1, 5001], 3: [3]}


def test_some():
    assert c.some(lambda e: True, []) is None
    assert c.some(lambda e: False, []) is None
    assert c.some({5}, []) is None
    assert c.some(lambda e: False, [1, 2, 3]) is None
    assert c.some({4, 5, 6}, [1, 2, 3]) is None
    assert c.some({4, 5, 6, 2}, [1, 2, 3]) == 2
    assert c.some(lambda e: e > 4, [1, 2, 3]) is None
    assert c.some(lambda e: e > 1, [1, 2, 3]) == 2


def test_is_seq():
    assert not c.is_seq(None)
    assert not c.is_seq(42)
    assert not c.is_seq(True)

    assert not c.is_seq({42})
    assert not c.is_seq({42: 1})
    assert not c.is_seq(infinite_range_fn())

    assert c.is_seq([])
    assert c.is_seq(())


def test_every():
    assert c.every(lambda e: e < 5, [])
    assert c.every(lambda e: e < 5, [1, 2, 3, 4])
    assert not c.every(lambda e: e < 5, [1, 2, 3, 4, 5])

    assert c.every({1, 2, 3}, [1, 1, 3, 2, 3, 1, 2])
    assert not c.every({1, 2, 3}, [1, 1, 3, 4, 3, 1, 2])


def test_not_every():
    assert not c.not_every(lambda e: e < 5, [])
    assert not c.not_every(lambda e: e < 5, [1, 2, 3, 4])
    assert c.not_every(lambda e: e < 5, [1, 2, 3, 4, 5])

    assert not c.not_every({1, 2, 3}, [1, 1, 3, 2, 3, 1, 2])
    assert c.not_every({1, 2, 3}, [1, 1, 3, 4, 3, 1, 2])


def test_not_any():
    assert c.not_any(lambda e: e < 5, [])
    assert c.not_any(lambda e: e < 5, [6, 7, 8])
    assert not c.not_any(lambda e: e < 5, [6, 7, 8, 1])


def test_dorun():
    els = []

    def _gen():
        for x in range(10):
            els.append(x)
            yield x

    assert [] == els
    assert c.dorun(_gen()) is None  # type: ignore[func-returns-value]
    assert list(range(10)) == els


def test_repeatedly():
    els = []

    def add_el():
        els.append(42)

    c.dorun(c.take(3, c.repeatedly(add_el)))
    assert els == [42] * 3

    els = []
    c.dorun(c.repeatedly(add_el, 2))
    assert els == [42] * 2


def test_repeatedly_nf():
    els = []

    def add_el():
        els.append(42)

    c.dorun(c.repeatedly(3, add_el))
    assert els == [42] * 3


def test_iterate():
    def inc(x): return x + 1

    assert c.nth(c.iterate(inc, 0), 10) == 10


def test_repeat():
    assert list(c.take(3, c.repeat(2))) == [2, 2, 2]
    assert list(c.repeat(2, 3)) == [2, 2, 2]
    assert list(c.repeat(2, 0)) == []
    assert list(c.repeat(2, -1)) == []


def test_range():
    assert list(c.range(2, 1)) == []
    assert list(c.range(2, 1, -1)) == [2]
    assert list(c.range(4)) == [0, 1, 2, 3]
    assert list(c.take(4, infinite_range_fn())) == [0, 1, 2, 3]


def test_count():
    assert c.count("qwertyuiop") == 10
    assert c.count([]) == 0
    assert c.count(()) == 0
    assert c.count({}) == 0
    assert c.count({"foo": "bar"}) == 1
    assert c.count(c.take(10, infinite_range_fn())) == 10

    class NotIterable:
        def __iter__(self):
            raise RuntimeError("boom!")

        def __len__(self):
            return 42

    assert c.count(NotIterable()) == 42


def test_tree_seq_no_children():
    def boom(_):
        raise RuntimeError("boom!")

    assert list(c.tree_seq(lambda _: False, boom, 42)) \
           == [42]


def test_tree_seq1():
    def get_children(x: IntNode):
        return cast(list[IntNode], x)

    t: IntNode = [[1, 2, [3]], [4]]
    assert list(c.tree_seq(c.is_seq, get_children, t)) \
           == [t, [1, 2, [3]], 1, 2, [3], 3, [4], 4]


def test_tree_seq2():
    t: StrNode = ["C", ["l", ["o"], ["j"]], ["u", ["r"]], ["e"]]
    assert list(map(c.first, c.tree_seq(c.rest, c.rest, t))) \
           == ["C", "l", "o", "j", "u", "r", "e"]


def test_dedupe():
    assert list(c.dedupe([])) == []
    assert list(c.dedupe([1])) == [1]
    assert list(c.dedupe([1, 2])) == [1, 2]
    assert list(c.dedupe([1, 1])) == [1]
    assert list(c.dedupe([1, 1, 1])) == [1]
    assert list(c.dedupe([1, 1, 2, 2, 1])) == [1, 2, 1]


@pytest.mark.parametrize("x", (0, 42, None, True, False, lambda: 1, re))
def test_empty_none(x):
    assert c.empty(x) is None


def test_empty():
    assert c.empty([]) == []
    assert c.empty([1, 2, 3]) == []
    assert c.empty(()) == ()
    assert c.empty((1, 2, 3)) == ()
    assert c.empty({}) == {}
    assert c.empty({"a": 42}) == {}
    assert c.empty(set()) == set()
    assert c.empty({1, 2}) == set()

    e: Iterable
    for e in ([], (), {}, set(), defaultdict(), deque(), Counter(),
              OrderedDict()):
        assert c.empty(e) == e


def test_partition():
    for n in (1, 2, 1000, -3, 0):
        assert list(c.partition([], n)) == []

    for n in (0, -1, -200):
        assert list(c.partition([1, 2, 3, 4], n)) == []

    assert list((c.partition([1, 2, 3], 1))) == [[1], [2], [3]]
    assert list((c.partition([1, 2, 3], 2))) == [[1, 2]]
    assert list((c.partition([1, 2, 3, 4], 2))) == [[1, 2], [3, 4]]
    assert list((c.partition([1, 2, 3], 3))) == [[1, 2, 3]]

    # pad
    assert list((c.partition([1, 2, 3], 1, pad=[4]))) == [[1], [2], [3]]
    assert list((c.partition([1, 2, 3], 2, pad=[4]))) == [[1, 2], [3, 4]]
    assert list((c.partition([1, 2, 3, 4], 2, pad=[5]))) == [[1, 2], [3, 4]]
    assert list((c.partition([1, 2, 3], 3, pad=[4]))) == [[1, 2, 3]]

    assert list((c.partition([1, 2, 3, 4], 3, pad=[5]))) == [[1, 2, 3], [4, 5]]
    assert list((c.partition([1, 2, 3, 4], 3, pad=[5, 6]))) == [[1, 2, 3], [4, 5, 6]]


def test_partition_by():
    assert list(c.partition_by(c.is_odd, [])) == []
    assert list(c.partition_by(c.identity, [{"a": 2}, False])) == [[{"a": 2}], [False]]

    # From the examples on https://clojuredocs.org/clojure.core/partition-by
    # (partition-by #(= 3 %) [1 2 3 4 5]) ; => ((1 2) (3) (4 5))
    assert list(c.partition_by(lambda x: x == 3, [1, 2, 3, 4, 5])) \
           == [[1, 2], [3], [4, 5]]

    # (partition-by odd? [1 1 1 2 2 3 3])  ; => ((1 1 1) (2 2) (3 3))
    assert list(c.partition_by(c.is_odd, [1, 1, 1, 2, 2, 3, 3])) \
           == [[1, 1, 1], [2, 2], [3, 3]]

    # (partition-by even? [1 1 1 2 2 3 3]) ; => ((1 1 1) (2 2) (3 3))
    assert list(c.partition_by(c.is_even, [1, 1, 1, 2, 2, 3, 3])) \
           == [[1, 1, 1], [2, 2], [3, 3]]

    # (partition-by identity "Leeeeeerrroyyy") ; => ((\L) (\e \e \e \e \e \e) (\r \r \r) (\o) (\y \y \y))
    assert list(c.partition_by(c.identity, "Leeeeeerrroyyy")) \
           == [["L"], ["e"] * 6, ["r"] * 3, ["o"], ["y"] * 3]

    # (partition-by identity "ABBA") ; => ((\A) (\B \B) (\A))
    assert list(c.partition_by(c.identity, "ABBA")) == [["A"], ["B", "B"], ["A"]]


@pytest.mark.parametrize("coll", ([], {}, (0 for _ in range(0))))
def test_seq_gen_none(coll):
    assert c.seq_gen(coll) is None


def test_seq_gen():
    def gen(n):
        for i in range(n):
            yield f"gen-{i}"

    for coll, expected in (
            ([1], [1]),
            ([1, 2], [1, 2]),
            ([1, 2, 3], [1, 2, 3]),
            (gen(1), ["gen-0"]),
            (gen(2), ["gen-0", "gen-1"]),
            (gen(3), ["gen-0", "gen-1", "gen-2"]),
    ):
        it = c.seq_gen(coll)
        assert it is not None
        assert list(it) == expected

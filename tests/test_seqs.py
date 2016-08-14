# -*- coding: UTF-8 -*-

import unittest

from clj import seqs as s

class TestSeqs(unittest.TestCase):

    def test_distinct(self):
        self.assertEquals([], list(s.distinct([])))
        self.assertEquals([1], list(s.distinct([1])))
        self.assertEquals([1, 2, 3, 4], list(s.distinct([1, 2, 3, 4])))
        self.assertEquals([2, 1, 3], list(s.distinct([2, 1, 3, 1, 2, 3])))

    def test_remove(self):
        self.assertEquals([], list(s.remove(lambda _: True, [])))
        self.assertEquals([], list(s.remove(lambda _: True, [1, 2, 3, 4])))
        self.assertEquals([1, 2, 3], list(s.remove(lambda _: False, [1, 2, 3])))
        self.assertEquals([1, 3], list(s.remove(lambda x: x==2, [1, 2, 3])))

    def test_keep(self):
        self.assertEquals([], list(s.keep(lambda _: True, [])))
        self.assertEquals([], list(s.keep(lambda _: None, [])))
        self.assertEquals([], list(s.keep(lambda _: None, [1, 2, 3])))
        self.assertEquals([False, False], list(s.keep(lambda _: False, [1, 2])))
        self.assertEquals([1, 2], list(s.keep(lambda x: x, [1, None, 2])))

    def test_keep_indexed(self):
        f = lambda i,e: e if i % 2 == 0 else None
        self.assertEquals(["a", "c"],
                          list(s.keep_indexed(f, ["a", "b", "c", "d"])))

    def test_cons(self):
        self.assertEquals([1], list(s.cons(1, [])))
        self.assertEquals([[]], list(s.cons([], [])))
        self.assertEquals([5, 1], list(s.cons(5, [1])))

    def test_concat(self):
        self.assertEquals([], list(s.concat()))
        self.assertEquals([], list(s.concat([])))
        self.assertEquals([], list(s.concat([], [], [], [])))
        self.assertEquals([1, 2], list(s.concat([1, 2], [])))
        self.assertEquals([1, 2, 3], list(s.concat([1, 2], [3])))

    def test_mapcat(self):
        f = lambda s: s.split(",")
        self.assertEquals(["a", "b", "c", "d"],
                          list(s.mapcat(f, ["a,b", "c,d"])))

        g = s.mapcat(reversed, [[3, 2, 1, 0], [6, 5, 4], [9, 8, 7]])
        self.assertEquals(list(range(10)), list(g))

    def test_cycle(self):
        self.assertEqual([1, 2, 3, 1, 2, 3, 1, 2],
                         list(s.take(8, s.cycle([1, 2, 3]))))

    def test_interleave(self):
        self.assertEqual([1, 2, 3, 1, 2, 3, 1],
                         list(s.take(7,
                                     s.interleave(s.repeat(1),
                                                  s.repeat(2),
                                                  s.repeat(3)))))

        self.assertEquals([0, 500, 1, 501],
                          list(s.interleave(range(2), range(500, 1000))))

        self.assertEquals([500, 0, 501, 1],
                          list(s.interleave(range(500, 1000), range(2))))

    def test_interpose(self):
        self.assertEqual([], list(s.interpose(",", [])))
        self.assertEqual(["foo"], list(s.interpose(",", ["foo"])))
        self.assertEqual(["foo", ", ", "bar"],
                         list(s.interpose(", ", ["foo", "bar"])))

    def test_rest(self):
        self.assertEquals([], list(s.rest([])))
        self.assertEquals([], list(s.rest([1])))
        self.assertEquals([2, 3, 4], list(s.rest([1, 2, 3, 4])))

    def test_drop(self):
        self.assertEquals([], list(s.drop(0, [])))
        self.assertEquals([], list(s.drop(1000, [])))
        self.assertEquals([], list(s.drop(1000, [1, 2, 3, 4])))
        self.assertEquals([1, 2, 3, 4], list(s.drop(0, [1, 2, 3, 4])))
        self.assertEquals([1, 2, 3, 4], list(s.drop(-3, [1, 2, 3, 4])))
        self.assertEquals([4], list(s.drop(3, [1, 2, 3, 4])))

    def test_drop_while(self):
        self.assertEquals([], list(s.drop_while(lambda _: True, [])))
        self.assertEquals([], list(s.drop_while(lambda _: True, [1, 2, 3])))
        self.assertEquals([3, 1],
                          list(s.drop_while(lambda n: n < 3, [1, 2, 3, 1])))

    def test_take(self):
        self.assertEquals([], list(s.take(40, [])))
        self.assertEquals([], list(s.take(0, [1, 2, 3])))
        self.assertEquals([1, 2], list(s.take(2, [1, 2, 3])))
        self.assertEquals([1, 2, 3], list(s.take(3, [1, 2, 3])))
        self.assertEquals([1, 2, 3], list(s.take(4, [1, 2, 3])))

        els = []
        def _gen():
            for x in range(10):
                els.append(x)
                yield x

        s.dorun(s.take(0, _gen()))
        self.assertEquals([], els)

        self.assertEquals(els, list(s.take(5, _gen())))

    def test_take_nth(self):
        ls = [42, 25, 17, 1, 34, 87]
        self.assertEquals([1, 1, 1], list(s.take(3, s.take_nth(0, [1, 2]))))
        self.assertEquals([1, 1, 1], list(s.take(3, s.take_nth(-1, [1, 2]))))
        self.assertEquals(ls, list(s.take_nth(1, ls)))
        self.assertEquals(ls, list(s.take_nth(2, s.interleave(ls, range(20)))))

    def test_take_while(self):
        self.assertEquals([], list(s.take_while(lambda _: True, [])))
        self.assertEquals([], list(s.take_while(lambda _: False, [1, 2, 3])))
        self.assertEquals([1, 2],
                          list(s.take_while(lambda n: n < 3, [1, 2, 3, 1])))

    def test_butlast(self):
        self.assertEquals([], list(s.butlast([])))
        self.assertEquals([], list(s.butlast([1])))
        self.assertEquals([1], list(s.butlast([1, 2])))
        self.assertEquals([1, 2, 3], list(s.butlast([1, 2, 3, 4])))

    def test_drop_last(self):
        self.assertEquals([], list(s.drop_last(0, [])))
        self.assertEquals([], list(s.drop_last(1, [])))
        self.assertEquals([], list(s.drop_last(1000, [])))
        self.assertEquals([1, 2], list(s.drop_last(-1, [1, 2])))
        self.assertEquals([1, 2], list(s.drop_last(-5, [1, 2])))
        self.assertEquals([], list(s.drop_last(2, [1, 2])))
        self.assertEquals([1, 2], list(s.drop_last(3, [1, 2, 3, 4, 5])))

    def test_flatten(self):
        self.assertEquals([], list(s.flatten([])))
        self.assertEquals([], list(s.flatten([[], [[[[], []], []]]])))
        self.assertEquals([1, 2, 3, 4],
                          list(s.flatten([[], [1, [[[], [2, 3]], []], 4]])))
        self.assertEquals(["foo", "bar"], list(s.flatten(["foo", "bar"])))

    def test_shuffle(self):
        self.assertEquals([], list(s.shuffle([])))

        ls = [1, 2, 3, 4]
        ls_orig = ls[:]
        self.assertEquals(ls, list(sorted(s.shuffle(ls))))
        self.assertEquals(ls_orig, ls)  # ensure it's not modified

    def test_split_at(self):
        self.assertEquals([[], []], list(map(list, s.split_at(0, []))))
        self.assertEquals([[], []], list(map(list, s.split_at(1, []))))
        self.assertEquals([[1], [2, 3]], list(map(list, s.split_at(1, [1, 2, 3]))))

    def test_split_with(self):
        self.assertEquals([[], []],
                          list(map(list, s.split_with(lambda _: True, []))))
        self.assertEquals([[], []],
                          list(map(list, s.split_with(lambda _: False, []))))
        self.assertEquals([[1, 2], [3, 4, 3, 2, 1]],
                          list(map(list, s.split_with(lambda n: n<3,
                                                      [1, 2, 3, 4, 3, 2, 1]))))

    def test_replace(self):
        self.assertEquals([], list(s.replace({}, [])))
        self.assertEquals([], list(s.replace({"a": "b"}, [])))
        self.assertEquals(["b"], list(s.replace({"a": "b"}, ["b"])))
        self.assertEquals(["b"], list(s.replace({"a": "b"}, ["a"])))
        self.assertEquals(["c"], list(s.replace({"a": "b"}, ["c"])))
        self.assertEquals(["b"], list(s.replace({"a": "b",
                                                 "b": "c"}, ["a"])))

    def test_map_indexed(self):
        self.assertEquals([], list(s.map_indexed(lambda i, e: 42, [])))
        self.assertEquals([0, 1, 2],
                          list(s.map_indexed(lambda i, e: i, [5, 3, 1])))
        self.assertEquals([5, 4, 3],
                          list(s.map_indexed(lambda i, e: i+e, [5, 3, 1])))

    def test_first(self):
        self.assertEquals(None, s.first(None))
        self.assertEquals(None, s.first([]))
        self.assertEquals(42, s.first([42]))
        self.assertEquals(42, s.first([42, 1, 2, 3]))

    def test_ffirst(self):
        self.assertEquals(None, s.ffirst(None))
        self.assertEquals(None, s.ffirst([None]))
        self.assertEquals(None, s.ffirst([]))
        self.assertEquals(None, s.ffirst([[]]))
        self.assertEquals(42, s.ffirst([[42, 1], 2]))

    def test_nfirst(self):
        self.assertEquals([], list(s.nfirst(None)))
        self.assertEquals([], list(s.nfirst([])))
        self.assertEquals([], list(s.nfirst([None])))
        self.assertEquals([], list(s.nfirst([[]])))
        self.assertEquals([2, 3], list(s.nfirst([[1, 2, 3], 4])))

    def test_second(self):
        self.assertEquals(None, s.second(None))
        self.assertEquals(None, s.second([]))
        self.assertEquals(None, s.second([42]))
        self.assertEquals(1, s.second([42, 1, 2, 3]))

    def test_nth(self):
        nope = object()
        self.assertEquals(nope, s.nth([], 0, nope))
        self.assertEquals(nope, s.nth([], -1, nope))
        self.assertEquals(nope, s.nth([], 1, nope))

        self.assertEquals(1, s.nth([42, 1, 2, 3], 1))
        self.assertEquals(7, s.nth([42, 1, 2, 3], 6, 7))

        self.assertEquals(20, s.nth(s.range(), 20))

    def test_last(self):
        self.assertEquals(None, s.last([]))
        self.assertEquals(1, s.last([1]))
        self.assertEquals(2, s.last([1, 2]))

    def test_zipmap(self):
        self.assertEquals({}, s.zipmap([], []))
        self.assertEquals({}, s.zipmap([], s.range()))
        self.assertEquals({}, s.zipmap(s.range(), []))
        self.assertEquals({"a": 1}, s.zipmap(("a",), [1]))
        self.assertEquals({"a": 1, "b": 2},
                          s.zipmap(["b", "a"], [2, 1]))

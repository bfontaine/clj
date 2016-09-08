# -*- coding: UTF-8 -*-

import unittest

from clj import fns as f

class TestFns(unittest.TestCase):

    def test_identity(self):
        for e in (True, None, [3], {4: 2}, (24,), 1, -1, 1e9, object(), "a"):
            self.assertEquals(e, f.identity(e))

    def test_comp(self):
        inc = lambda n: n + 1
        twice = lambda n: n * 2
        dec = lambda n: n - 1

        fn = f.comp(inc, twice, dec, twice)
        self.assertEquals(3, fn(1))
        self.assertEquals(7, fn(2))
        self.assertEquals(27, fn(7))
        self.assertEquals(107, fn(27))

    def test_complement(self):
        odd = lambda e: e & 1
        even = f.complement(odd)

        self.assertTrue(even(2))
        self.assertFalse(even(41))

    def test_constantly(self):
        x = object()
        fn = f.constantly(x)

        self.assertEquals(x, fn())
        self.assertEquals(x, fn(1, 2, 3, 4, 5, a=1, foo=3))

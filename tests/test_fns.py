# -*- coding: UTF-8 -*-

import unittest

import clj as c


class TestFns(unittest.TestCase):
    def test_identity(self):
        for e in (True, None, [3], {4: 2}, (24,), 1, -1, 1e9, object(), "a"):
            self.assertEquals(e, c.identity(e))

    def test_inc(self):
        self.assertEquals(2, c.inc(1))
        self.assertEquals(2.0, c.inc(1.0))
        self.assertEquals(0, c.inc(-1))

    def test_dec(self):
        self.assertEquals(1, c.dec(2))
        self.assertEquals(1.0, c.dec(2.0))
        self.assertEquals(-2, c.dec(-1))

    def test_even(self):
        self.assertTrue(c.is_even(42))
        self.assertFalse(c.is_even(1))
        self.assertFalse(c.is_even(-1))
        self.assertTrue(c.is_even(-2))

    def test_odd(self):
        self.assertTrue(c.is_odd(41))
        self.assertFalse(c.is_odd(2))
        self.assertTrue(c.is_odd(-1))
        self.assertFalse(c.is_odd(-2))

    def test_comp(self):
        twice = lambda n: n * 2

        fn = c.comp(c.inc, twice, c.dec, twice)
        self.assertEquals(3, fn(1))
        self.assertEquals(7, fn(2))
        self.assertEquals(27, fn(7))
        self.assertEquals(107, fn(27))

    def test_complement(self):
        odd = lambda e: e & 1
        even = c.complement(odd)

        self.assertTrue(even(2))
        self.assertFalse(even(41))

    def test_constantly(self):
        x = object()
        fn = c.constantly(x)

        self.assertEquals(x, fn())
        self.assertEquals(x, fn(1, 2, 3, 4, 5, a=1, foo=3))

    def test_juxt(self):
        fn = c.juxt(c.inc, c.identity, c.dec)
        self.assertEquals([3, 2, 1], fn(2))

        self.assertEquals([43], c.juxt(c.inc)(42))

    def test_is_distinct(self):
        self.assertTrue(c.is_distinct(42))
        self.assertTrue(c.is_distinct(1, 2))
        self.assertTrue(c.is_distinct(1, 2, 3))
        self.assertFalse(c.is_distinct(1, 2, 3, 3))
        self.assertFalse(c.is_distinct(1, 2, 1))

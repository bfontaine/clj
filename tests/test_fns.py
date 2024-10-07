import pytest

import clj as c


@pytest.mark.parametrize("e", (True, None, [3], {4: 2}, (24,), 1, -1, 1e9, object(), "a"))
def test_identity(e):
    assert c.identity(e) == e


def test_inc():
    assert c.inc(1) == 2
    assert c.inc(1.0) == 2.0
    assert c.inc(-1) == 0


def test_dec():
    assert c.dec(2) == 1
    assert c.dec(2.0) == 1.0
    assert c.dec(-1) == -2


def test_even():
    assert c.is_even(42)
    assert not c.is_even(1)
    assert not c.is_even(-1)
    assert c.is_even(-2)


def test_odd():
    assert c.is_odd(41)
    assert not c.is_odd(2)
    assert c.is_odd(-1)
    assert not c.is_odd(-2)


def test_comp():
    def twice(n):
        return n * 2

    fn = c.comp(c.inc, twice, c.dec, twice)
    assert fn(1) == 3
    assert fn(2) == 7
    assert fn(7) == 27
    assert fn(27) == 107


def test_complement():
    def odd(e):
        return e & 1

    even = c.complement(odd)

    assert even(2)
    assert not even(41)


def test_constantly():
    x = object()
    fn = c.constantly(x)

    assert fn() == x
    assert fn(1, 2, 3, 4, 5, a=1, foo=3) == x


def test_juxt():
    fn = c.juxt(c.inc, c.identity, c.dec)
    assert fn(2) == [3, 2, 1]

    assert c.juxt(c.inc)(42) == [43]


def test_is_distinct():
    assert c.is_distinct(42)
    assert c.is_distinct(1, 2)
    assert c.is_distinct(1, 2, 3)
    assert not c.is_distinct(1, 2, 3, 3)
    assert not c.is_distinct(1, 2, 1)

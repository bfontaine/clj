# -*- coding: UTF-8 -*-

# See http://clojure.org/reference/other_functions
from typing import TypeVar, Union, Callable, Hashable

T = TypeVar('T')


def identity(x: T) -> T:
    """
    Returns its argument.
    """
    return x


def inc(x: Union[int, float]):
    """
    Returns a number one greater than num.
    """
    return x + 1


def dec(x: Union[int, float]):
    """
    Returns a number one less than num.
    """
    return x - 1


def is_even(x: int):
    """
    Return ``True`` if ``x`` is an even number.
    """
    return bool(~x & 1)


def is_odd(x: int):
    """
    Return ``True`` if ``x`` is an odd number.
    """
    return not is_even(x)


def comp(*fns) -> Callable:
    """
    Takes a set of functions and returns a function that is the composition of
    those functions. The returned function takes a variable number of args,
    applies the rightmost of functions to the args, the next function
    (right-to-left) to the result, etc.
    """
    if not fns:
        return constantly(None)

    def _comp(*args, **kw):
        res = fns[-1](*args, **kw)

        for i in range(1, len(fns)):
            res = fns[-1 - i](res)

        return res

    return _comp


def complement(f: Callable) -> Callable[..., bool]:
    """
    Takes a function ``f`` and returns a function that takes the same arguments
    as ``f``, has the same effects, if any, and returns the opposite truth
    value.
    """

    def _f(*args, **kw):
        return not f(*args, **kw)

    return _f


def constantly(x: T) -> Callable[..., T]:
    """
    Returns a function that takes any number of arguments and returns ``x``.
    """

    def _fn(*_args, **_kw):
        return x

    return _fn


def juxt(*fns) -> Callable[..., list]:
    """
    Takes a set of functions and returns a function that is the juxtaposition
    of those functions. The returned function takes a variable number of
    arguments, and returns a list containing the result of applying each
    function to the arguments (left-to-right).

        juxt(a, b, c)(x) # => [a(x), b(x), c(x)]
    """

    # Note we accept zero argument while Clojure wants at least one.

    def _fn(*args, **kw):
        return [f(*args, **kw) for f in fns]

    return _fn


def is_distinct(*args: Hashable):
    s = set()
    for arg in args:
        if arg in s:
            return False
        s.add(arg)
    return True

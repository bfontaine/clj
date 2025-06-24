from typing import TypeVar, Callable, Hashable, Any

from typing_extensions import ParamSpec

X = TypeVar('X')
T = TypeVar('T')
Params = ParamSpec('Params')
Number = TypeVar('Number', int, float)


# See http://clojure.org/reference/other_functions


def identity(x: T) -> T:
    """
    Returns its argument.
    """
    return x


def inc(x: Number) -> Number:
    """
    Returns a number one greater than num.
    """
    return x + 1


def dec(x: Number) -> Number:
    """
    Returns a number one less than num.
    """
    return x - 1


def is_even(x: int) -> bool:
    """
    Return ``True`` if ``x`` is an even number.
    """
    return bool(~x & 1)


def is_odd(x: int) -> bool:
    """
    Return ``True`` if ``x`` is an odd number.
    """
    return bool(x & 1)


# TODO: better typing
def comp(*fns: Callable[..., Any]) -> Callable[..., Any]:
    """
    Takes a set of functions and returns a function that is the composition of
    those functions. The returned function takes a variable number of args,
    applies the rightmost of functions to the args, the next function
    (right-to-left) to the result, etc.
    """
    if not fns:
        return constantly(None)

    def _comp(*args: Any, **kw: Any) -> Any:
        res = fns[-1](*args, **kw)

        for i in range(1, len(fns)):
            res = fns[-1 - i](res)

        return res

    return _comp


def complement(f: Callable[Params, Any]) -> Callable[Params, bool]:
    """
    Takes a function ``f`` and returns a function that takes the same arguments
    as ``f``, has the same effects, if any, and returns the opposite truth
    value.
    """

    def _f(*args: Any, **kw: Any) -> bool:
        return not f(*args, **kw)

    return _f


def constantly(x: T) -> Callable[..., T]:
    """
    Returns a function that takes any number of arguments and returns ``x``.
    """

    def _fn(*_args: Any, **_kw: Any) -> T:
        return x

    return _fn


def juxt(*fns: Callable[Params, T]) -> Callable[Params, list[T]]:
    """
    Takes a set of functions and returns a function that is the juxtaposition
    of those functions. The returned function takes a variable number of
    arguments, and returns a list containing the result of applying each
    function to the arguments (left-to-right).

        juxt(f, g, h)(x) # => [f(x), g(x), h(x)]
    """

    # Note we accept zero argument while Clojure wants at least one.

    def _fn(*args: Any, **kw: Any) -> list[T]:
        return [f(*args, **kw) for f in fns]

    return _fn


def is_distinct(*args: Hashable) -> bool:
    s = set()
    for arg in args:
        if arg in s:
            return False
        s.add(arg)
    return True

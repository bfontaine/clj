# -*- coding: UTF-8 -*-

# See http://clojure.org/reference/other_functions

def identity(x):
    """
    Returns its argument.
    """
    return x

def inc(x):
    """
    Returns a number one greater than num.
    """
    return x + 1

def dec(x):
    """
    Returns a number one less than num.
    """
    return x - 1

def comp(*fns):
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

def complement(f):
    """
    Takes a function ``f`` and returns a function that takes the same arguments
    as ``f``, has the same effects, if any, and returns the opposite truth
    value.
    """
    def _f(*args, **kw):
        return not f(*args, **kw)

    return _f

def constantly(x):
    """
    Returns a function that takes any number of arguments and returns ``x``.
    """
    def _fn(*args, **kw):
        return x

    return _fn

def juxt(*fns):
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

def is_distinct(*args):
    s = set()
    for arg in args:
        if arg in s:
            return False
        s.add(arg)
    return True

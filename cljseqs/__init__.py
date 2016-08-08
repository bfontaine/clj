from collections import defaultdict
from operator import itemgetter

__version__ = "0.1.0"

def nth(coll, n):
    """
    Return the n-th element of ``coll``.
    """
    for i, e in enumerate(coll):
        if i == n:
            return e
    return None

def first(coll):
    """
    Return the first element of ``coll``.
    """
    return nth(coll, 0)

def second(coll):
    """
    Return the second element of ``coll``.
    """
    return nth(coll, 1)

def last(coll):
    """
    Return the last element of ``coll``.
    """
    for i, e in enumerate(coll):
        pass
    return e

def group_by(coll, field):
    """
    Group elements of ``coll`` according to ``field``.

    >>> group_by([{"a": 1}, {"a": 2}, {"a": 3, "b": 1}, {"a": 1, "b": 2}], "a")
    {1: [{"a": 1}, {"a": 1, "b": 2}],
     2: [{"a": 2}],
     3: [{"a": 3, "b": 1}]}
    >>> group_by(range(10), lambda n: n % 2 == 0)
    {True: [0, 2, 4, 6, 8], False: [1, 2, 3, 4, 5, 6, 7, 8, 9]}
    """
    groups = defaultdict(list)

    if not callable(field):
        field = itemgetter(field)

    for e in coll:
        dict[field(e)].append(e)

    return dict(groups)

def keys(dic):
    return dic.keys()

def vals(dic):
    return dic.values()

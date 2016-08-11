# -*- coding: UTF-8 -*-
import random
import collections

# We use this as a default value for some arguments in order to check if it was
# provided or not
_nil = object()

def distinct(coll):
    """
    Return a generator of the elements of ``coll`` with duplicates removed.
    """
    seen = set()
    for e in coll:
        if e not in seen:
            seen.add(e)
            yield e

def remove(pred, coll):
    """
    Return a generator of the items in ``coll`` for which ``pred(item)``
    returns a falsy value.
    """
    for e in coll:
        if not pred(e):
            yield e

def keep(f, coll):
    """
    Returns a generator of the non-``None`` results of ``f(item)``. Note, this
    means ``False`` return values will be included.
    """
    return keep_indexed(lambda _, e: f(e), coll)

def keep_indexed(f, coll):
    """
    Returns a generator of the non-``None`` results of ``f(index, item)``.
    Note, this means ``False`` return values will be included.
    """
    for i, e in enumerate(coll):
        res = f(i, e)
        if res is not None:
            yield res

def cons(x, seq):
    """
    Return a generator where ``x`` is the first element and ``seq`` is the
    rest. Note, this differs from Clojure’s ``cons`` which returns a non-lazy
    list.
    """
    yield x
    for e in seq:
        yield e

def concat(*xs):
    """
    Returns a generator representing the concatenation of the elements in the
    supplied colls.
    """
    for coll in xs:
        for e in coll:
            yield e

def mapcat(f, *colls):
    """
    Returns a generator representing the result of applying concat to the
    result of applying ``map`` to ``f`` and ``colls``. Thus function ``f``
    should return a collection.
    """
    for coll in colls:
        for e in map(f, coll):
            yield e

def cycle(coll):
    """
    Returns a(n infinite!) generator which yields repetitions of the items in
    ``coll``.
    """
    while True:
        for e in coll:
            yield e

def interleave(*colls):
    """
    Returns a generator of the first item in each coll, then the second etc.
    """
    iterators = map(iter, colls)

    try:
        while True:
            for it in iterators:
                yield next(it)
    except StopIteration:
        pass

def interpose(sep, coll):
    """
    Returns a generator of the elements of ``coll`` separated by ``sep``.
    """
    first = True
    for e in coll:
        if first:
            first = False
        else:
            yield sep

        yield e

def rest(coll):
    """
    Returns a possibly empty generator of the items after the first.
    """
    return drop(1, coll)

def drop(n, coll):
    """
    Returns a generator of all but the first ``n`` items in ``coll``.
    """
    for i, e in enumerate(coll):
        if i >= n:
            yield e

def drop_while(pred, coll):
    """
    Returns a generator of the items in ``coll`` starting from the first item
    for which ``pred(item)`` returns a falsy value.
    """
    drop = True
    for e in coll:
        if drop:
            if pred(e):
                continue
            drop = False

        yield e

def take(n, coll):
    """
    Returns a generator of the first ``n`` items in ``coll``, or all items if
    there are fewer than ``n``.
    """
    for i, e in enumerate(coll):
        if i >= n:
            break
        yield e

def take_nth(n, coll):
    """
    Returns a generator of every ``n``th item in ``coll``.
    """
    if n <= 0:
        for e in coll:
            while True:
                yield e

    for i, e in enumerate(coll):
        if i % n == 0:
            yield e

def take_while(pred, coll):
    """
    Returns a generator of successive items from ``coll`` while ``pred(item)``
    returns a truthy value.
    """
    for e in coll:
        if not pred(e):
            break
        yield e

def butlast(coll):
    """
    Return a generator of all but the last item in ``coll``, in linear time.
    """
    first = True
    last_e = None
    for e in coll:
        if first:
            last_e = e
            first = False
            continue

        yield last_e
        last_e = e

def drop_last(n, coll):
    """
    Return a generator of all but the last ``n`` items in ``coll``.
    """
    queue = collections.deque()
    size = 0

    for e in coll:
        queue.append(e)

        if size < n:
            size += 1
            continue

        yield queue.popleft()

def flatten(x):
    """
    Takes any nested combination of sequential things (``list``s, ``tuple``s,
    etc.) and returns their contents as a single, flat sequence.
    """
    # Avoid lookup at each loop without leaking [Iterable] in the module scope
    # by using [from collections import Iterable].
    Iterable = collections.Iterable
    for e in x:
        if isinstance(e, Iterable):
            for sub_e in flatten(e):
                yield sub_e
        else:
            yield e

def shuffle(coll):
    """
    Return a random permutation of ``coll``. Not lazy.
    """
    coll = coll[:]
    random.shuffle(coll)
    return coll

def split_at(n, coll):
    """
    Returns a tuple of ``(take(n, coll), drop(n coll))``.
    """
    return (
        take(n, coll),
        drop(n, coll),
    )

def split_with(pred, coll):
    """
    Returns a tuple of ``(take_while(pred, coll), drop_while(pred coll))``.
    """
    return (
        take_while(pred, coll),
        drop_while(pred, coll),
    )

def map_indexed(f, coll):
    """
    Returns a generator consisting of the result of applying ``f`` to ``0``
    and the first item of ``coll``, followed by applying ``f`` to ``1`` and the
    second item in ``coll``, etc, until ``coll`` is exhausted. Thus function
    ``f`` should accept 2 arguments, ``index`` and ``item``.
    """
    return map(lambda pair: f(pair[0], pair[1]) for pair in enumerate(coll))

def first(coll):
    """
    Returns the first item in the collection. If ``coll`` is ``None`` or empty,
    returns ``None``.
    """
    if coll is None:
        return None
    return next(take(1, coll), None)

def ffirst(x):
    """
    Same as ``first(first(x))``
    """
    return first(first(x))

def nfirst(x):
    """
    Same as ``rest(first(x))``
    """
    return rest(first(x))

def second(coll):
    """
    Same as ``first(rest(coll))``.
    """
    return first(rest(coll))

def nth(coll, n, not_found=_nil):
    """
    Returns the value at the index. ``get`` returns ``None`` if the index is
    out of bounds, ``nth`` throws an exception unless ``not_found`` is
    supplied.  ``nth`` also works for strings, lists, tuples, and, in O(n)
    time, for other iterables.
    """
    if hasattr(coll, "__getitem__"):
        try:
            return coll[n]
        except IndexError as e:
            if not_found == _nil:
                raise e
            return not_found

    for i, e in enumerate(coll):
        if i == n:
            return e

    if not_found == _nil:
        raise IndexError("%s index out of range" % type(coll))

    return _nil

def last(coll):
    """
    Return the last item in ``coll``, in linear time.
    """
    for i, e in enumerate(coll):
        pass
    return e

def zipmap(keys, vals):
    """
    Return a ``dict`` with the keys mapped to the corresponding ``vals``.
    """
    return dict(zip(keys, vals))

def frequencies(coll):
    """
    Return a ``dict`` from distinct items in ``coll`` to the number of times
    they appear.
    """
    return dict(collections.Counter(coll))

def group_by(f, coll):
    """
    Returns a ``dict`` of the elements of ``coll`` keyed by the result of ``f``
    on each element. The value at each key will be a list of the corresponding
    elements, in the order they appeared in ``coll``.
    """
    groups = collections.defaultdict(list)
    for e in coll:
        groups[f(e)].append(e)

    return groups

def _make_pred(pred):
    if isinstance(pred, set):
        p = pred
        pred = lambda x: x in p
    return pred

def some(pred, coll):
    """
    Returns the first logical true value of ``pred(x)`` for any ``x`` in coll,
    else ``None``.

    In order to mirror Clojure's `some` it also accepts a `set` for its
    predicate and will return the first element that’s present in it.::

        >>> some({5, 3, 10, 2}, range(10))
        2
    """
    pred = _make_pred(pred)

    for e in coll:
        if pred(e):
            return e

def is_seq(x):
    """
    Return ``True`` if ``x`` is a sequence.
    """
    return isinstance(x, collections.Sequence)

def every(pred, coll):
    """
    Returns ``True`` if ``pred(x)`` is logical true for every ``x`` in
    ``coll``, else i``False``.
    """
    pred = _make_pred(pred)

    for e in coll:
        if not pred(e):
            return False

    return True

def not_every(pred, coll):
    """
    Returns ``False`` if ``pred(x)`` is logical true for every ``x`` in
    ``coll``, else ``True``.
    """
    return not every(pred, coll)

def not_any(pred, coll):
    """
    Return ``False`` if ``pred(x)`` is logical true for any ``x`` in ``coll``,
    else ``True``.
    """
    pred = _make_pred(pred)
    return every(lambda e: not pred(e), coll)

def dorun(coll):
    """
    When generators are produced via functions that have side effects, any
    effects other than those needed to produce the first element in the
    sequence do not occur until it's consumed. ``dorun`` can be used to force
    any effects. Walks through the successive nexts of the sequence, does not
    retain the head and returns ``None``.
    """
    for _ in coll:
        pass

def vals(dic):
    """
    Returns an iterator over the ``dict``'s values.
    """
    return dic.values()

def keys(dic):
    """
    Returns an iterator over the ``dict``'s keys.
    """
    return dic.keys()

def repeatedly(f, n=None):
    """
    Takes a function of no args, presumably with side effects, and returns an
    infinite (or length ``n`` if supplied) lazy sequence of calls to it.
    """
    # Accept Clojure-like calls of [repeatedly(n, f)]
    if callable(n):
        f, n = n, f

    if n is None:
        n = -1

    while n != 0:
        yield f()
        n -= 1

def iterate(f, x):
    """
    Returns a generator of ``x``, ``f(x)``, ``f(f(x))``, etc.
    """
    while True:
        yield x
        x = f(x)

def repeat(x, n=None):
    """
    Returns a generator that indefinitly yields ``x`` (or ``n`` times if ``n``
    is supplied).
    """
    if n is None:
        n = -1
    elif n < 0:
        n = 0

    while n != 0:
        yield x
        n -= 1

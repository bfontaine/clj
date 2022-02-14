# -*- coding: UTF-8 -*-
import random
import collections
import itertools
import collections.abc as collections_abc

# We use this as a default value for some arguments in order to check if they
# were provided or not
from typing import Iterable, TypeVar, Any, Callable, Iterator, Union, Tuple, Dict, Optional, List, Set, cast, Deque

_nil = object()

# We redefine `range` below so keep a reference to the original one here
_range = range

T = TypeVar('T')
T2 = TypeVar('T2')


def _is_collection_abc(x):
    return isinstance(x, collections_abc.Sized) and \
           isinstance(x, collections_abc.Iterable)


def _make_gen(g: Iterable[T]) -> Iterator[T]:
    for e in g:
        yield e


# The order of the functions here match the one in the Clojure docs:
#     http://clojure.org/reference/sequences

def distinct(coll: Iterable[T]) -> Iterable[T]:
    """
    Return a generator of the elements of ``coll`` with duplicates removed.
    """
    seen = set()
    for e in coll:
        if e not in seen:
            seen.add(e)
            yield e


# alias
filter = filter


def remove(pred: Callable[[T], Any], coll: Iterable[T]) -> Iterable[T]:
    """
    Return a generator of the items in ``coll`` for which ``pred(item)``
    returns a falsy value.
    """
    return itertools.filterfalse(pred, coll)


def keep(f: Callable[[T], Any], coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of the non-``None`` results of ``f(item)``. Note, this
    means ``False`` return values will be included.
    """
    return keep_indexed(lambda _, e: f(e), coll)


def keep_indexed(f: Callable[[int, T], Any], coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of the non-``None`` results of ``f(index, item)``.
    Note, this means ``False`` return values will be included.
    """
    for i, e in enumerate(coll):
        res = f(i, e)
        if res is not None:
            yield res


def cons(x: T2, seq: Iterable[T]) -> Iterable[Union[T, T2]]:
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

    This is equivalent to ``itertools.chain``.
    """
    return itertools.chain(*xs)


# alias
map = map


def mapcat(f: Callable[[Any], Iterable], *colls):
    """
    Returns a generator representing the result of applying concat to the
    result of applying ``map`` to ``f`` and ``colls``. Thus function ``f``
    should return a collection.
    """
    for coll in map(f, *colls):
        for e in coll:
            yield e


def cycle(coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a (infinite!) generator which yields repetitions of the items in ``coll``.
    """
    els = []
    for e in coll:
        yield e
        els.append(e)

    while True:
        for e in els:
            yield e


def interleave(*colls) -> Iterable:
    """
    Returns a generator of the first item in each coll, then the second etc.
    """
    iterators = [iter(coll) for coll in colls]

    try:
        while True:
            values = [next(it) for it in iterators]
            for v in values:
                yield v
    except StopIteration:
        pass


def interpose(sep: T2, coll: Iterable[T]) -> Iterable[Union[T, T2]]:
    """
    Returns a generator of the elements of ``coll`` separated by ``sep``.
    """
    first_ = True
    for e in coll:
        if first_:
            first_ = False
        else:
            yield sep

        yield e


def rest(coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a possibly empty generator of the items after the first.
    """
    return drop(1, coll)


def drop(n: int, coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of all but the first ``n`` items in ``coll``.
    """
    if coll is None:
        return

    for i, e in enumerate(coll):
        if i >= n:
            yield e


def drop_while(pred: Callable[[T], Any], coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of the items in ``coll`` starting from the first item
    for which ``pred(item)`` returns a falsy value.

    This is equivalent to ``itertools.dropwhile``.
    """
    return itertools.dropwhile(pred, coll)


def take(n: int, coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of the first ``n`` items in ``coll``, or all items if
    there are fewer than ``n``.
    """
    if n <= 0:
        return

    for i, e in enumerate(coll):
        yield e
        if i + 1 >= n:
            break


def take_nth(n: int, coll: Iterable[T]) -> Iterable[T]:
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


def take_while(pred: Callable[[T], Any], coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of successive items from ``coll`` while ``pred(item)``
    returns a truthy value.

    This is equivalent to ``itertools.takewhile``.
    """
    return itertools.takewhile(pred, coll)


def butlast(coll: Iterable[T]) -> Iterable[T]:
    """
    Return a generator of all but the last item in ``coll``, in linear time.
    """
    first_ = True
    last_e: Optional[T] = None
    for e in coll:
        if first_:
            last_e = e
            first_ = False
            continue

        yield cast(T, last_e)
        last_e = e


def drop_last(n: int, coll: Iterable[T]) -> Iterable[T]:
    """
    Return a generator of all but the last ``n`` items in ``coll``.
    """
    if n == 1:
        for e in butlast(coll):
            yield e
        return

    queue: Deque[T] = collections.deque()
    size = 0

    for e in coll:
        queue.append(e)

        if size < n:
            size += 1
            continue

        yield queue.popleft()


def flatten(x: Iterable) -> Iterable:
    """
    Takes any nested combination of sequential things (``list``s, ``tuple``s,
    etc.) and returns their contents as a single, flat sequence.
    """
    # FIXME:
    #   > RecursionError: maximum recursion depth exceeded in comparison
    #   When called with a very deep list (~1000 levels of depth)

    # Avoid lookup at each loop without leaking [Iterable] in the module scope
    # by using [from collections import Iterable].
    iterable_class = collections.abc.Iterable
    for e in x:
        if isinstance(e, iterable_class) and not isinstance(e, (bytes, str)):
            for sub_e in flatten(e):
                yield sub_e
        else:
            yield e


def reverse(coll: Iterable[T]) -> Iterable[T]:
    """
    Return an iterator of the items in ``coll`` in reverse order. Not lazy.
    """
    for e in reversed(list(coll)):
        yield e


def shuffle(coll: Iterable[T]) -> Iterable[T]:
    """
    Return a random permutation of ``coll``. Not lazy.
    """
    coll = list(coll)
    random.shuffle(coll)
    return coll


def _iter(coll, n=0):
    # If it's an iterator, we already consumed the beginning
    if isinstance(coll, collections.abc.Iterator):
        return coll
    return coll[n:]


def split_at(n: int, coll: Iterable[T]) -> Tuple[Iterable[T], Iterable[T]]:
    """
    Returns a tuple of ``(take(n, coll), drop(n coll))``.
    """
    if n <= 0:
        return [], coll

    if coll is None:
        return [], []

    # Unfortunately we must consume all elements for the first case because
    # unlike Clojure's lazy lists, Python's generators yield their elements
    # only once.
    taken = []
    for i, e in enumerate(coll):
        taken.append(e)
        if i + 1 >= n:
            break

    return taken, _iter(coll, n)


def split_with(pred: Callable[[T], Any], coll: Iterable[T]) -> Tuple[Iterable[T], Iterable[T]]:
    """
    Returns a tuple of ``(take_while(pred, coll), drop_while(pred coll))``.
    """
    # See note in split_at.
    taken = []
    for i, e in enumerate(coll):
        if pred(e):
            taken.append(e)
        else:
            middle = e
            break
    else:
        return taken, []

    def dropped_while():
        yield middle
        for el in _iter(coll, i + 1):
            yield el

    return taken, dropped_while()


def replace(smap: Dict[T, T2], coll: Iterable[T]) -> Iterable[Union[T, T2]]:
    """
    Given a map of replacement pairs and a list/collection, yield a sequence
    where any element = a key in ``smap`` replaced with the corresponding val
    in ``smap``.
    """
    for e in coll:
        yield smap.get(e, e)


def reductions(f: Callable, coll: Iterable[T], init: Any = _nil) -> Iterable:
    """
    Yield the intermediate values of the reduction (as per ``reduce``) of
    ``coll`` by ``f``, starting with ``init``.
    """
    first_value, is_empty = _first(coll)
    if is_empty:
        if init is _nil:
            yield None
        else:
            yield init
        return

    first_value = cast(T, first_value)

    if init is _nil:
        init_value = first_value
    else:
        coll = cons(first_value, coll)
        init_value = init

    yield init_value

    for e in coll:
        init_value = f(init_value, e)
        yield init_value


def map_indexed(f: Callable[[int, T], T2], coll: Iterable[T]) -> Iterable[T2]:
    """
    Returns a generator consisting of the result of applying ``f`` to ``0``
    and the first item of ``coll``, followed by applying ``f`` to ``1`` and the
    second item in ``coll``, etc, until ``coll`` is exhausted. Thus function
    ``f`` should accept 2 arguments, ``index`` and ``item``.
    """
    return map(lambda pair: f(pair[0], pair[1]), enumerate(coll))


def _first(coll: Iterable[T]) -> Tuple[Optional[T], bool]:
    """
    Like first(coll), but return a tuple of ``(first, is_empty)`` where `first` is either the first
    element of the collection or ``None`` and ``is_empty`` is a boolean that is ``True`` if the collection
    is empty.
    """
    if coll is None:
        return None, True

    _flag = object()
    first_value: Union[T, object] = next(_make_gen(take(1, coll)), _flag)
    if first_value is _flag:
        return None, True
    return cast(Optional[T], first_value), False


def first(coll: Iterable[T]) -> Optional[T]:
    """
    Returns the first item in the collection. If ``coll`` is empty, returns ``None``.
    """
    first_value: Optional[T] = _first(coll)[0]
    return first_value


def ffirst(x: Iterable[Iterable[T]]) -> Optional[T]:
    """
    Same as ``first(first(x))``
    """
    f = first(x)
    if f is None:
        return None
    return first(f)


def nfirst(x: Iterable[Iterable[T]]) -> Iterable[T]:
    """
    Same as ``rest(first(x))``
    """
    f = first(x)
    if f is None:
        return []
    return rest(f)


def second(coll: Iterable[T]) -> Optional[T]:
    """
    Same as ``first(rest(coll))``.
    """
    return first(rest(coll))


def nth(coll: Iterable[T], n: int, not_found: Any = _nil) -> Any:
    """
    Returns the value at the index. ``get`` returns ``None`` if the index is
    out of bounds, ``nth`` throws an exception unless ``not_found`` is
    supplied.  ``nth`` also works for strings, lists, tuples, and, in O(n)
    time, for other iterables.
    """
    if n >= 0:
        if hasattr(coll, "__getitem__"):
            try:
                return cast(list, coll)[n]
            except IndexError:
                if not_found is not _nil:
                    return not_found
                raise

        for i, e in enumerate(coll):
            if i == n:
                return e

    if not_found is _nil:
        raise IndexError("%s index out of range" % type(coll))

    return not_found


def last(coll: Iterable[T]) -> Optional[T]:
    """
    Return the last item in ``coll``, in linear time. Return ``None`` if ``coll`` is empty.
    """
    e = None
    for item in coll:
        e = item
    return e


def zipmap(keys: Iterable[T], vals: Iterable[T2]) -> Dict[T, T2]:
    """
    Return a ``dict`` with the keys mapped to the corresponding ``vals``.
    """
    return dict(zip(keys, vals))


def group_by(f: Callable[[T], T2], coll: Iterable[T]) -> Dict[T2, List[T]]:
    """
    Returns a ``dict`` of the elements of ``coll`` keyed by the result of ``f``
    on each element. The value at each key will be a list of the corresponding
    elements, in the order they appeared in ``coll``.
    """
    groups = collections.defaultdict(list)
    for e in coll:
        groups[f(e)].append(e)

    return dict(groups)


def _make_pred(pred: Union[Callable[[T], T2], Set[T]]) -> Callable[[T], Union[T2, bool]]:
    if isinstance(pred, set):
        return lambda x: x in cast(Set[T], pred)

    return pred


def some(pred: Union[Callable[[T], Any], Set[T]], coll: Iterable[T]) -> Optional[T]:
    """
    Returns the first logical true value of ``pred(x)`` for any ``x`` in coll,
    else ``None``.

    In order to mirror Clojure's ``some`` it also accepts a `set` for its
    predicate and will return the first element that’s present in it.

        >>> some({5, 3, 10, 2}, range(10))
        2
    """
    pred = _make_pred(pred)

    for e in coll:
        if pred(e):
            return e
    return None


def is_seq(x):
    """
    Return ``True`` if ``x`` is a sequence.
    """
    return isinstance(x, collections_abc.Sequence)


def every(pred: Union[Callable[[T], Any], Set[T]], coll: Iterable[T]) -> bool:
    """
    Returns ``True`` if ``pred(x)`` is logical true for every ``x`` in
    ``coll``, else i``False``.
    """
    pred2 = _make_pred(pred)

    for e in coll:
        if not pred2(e):
            return False

    return True


def not_every(pred: Union[Callable[[T], Any], Set[T]], coll: Iterable[T]) -> bool:
    """
    Returns ``False`` if ``pred(x)`` is logical true for every ``x`` in
    ``coll``, else ``True``.
    """
    return not every(pred, coll)


def not_any(pred: Union[Callable[[T], Any], Set[T]], coll: Iterable[T]) -> bool:
    """
    Return ``False`` if ``pred(x)`` is logical true for any ``x`` in ``coll``,
    else ``True``.
    """
    pred2 = _make_pred(pred)
    return every(lambda e: not pred2(e), coll)


def dorun(coll: Iterable) -> None:
    """
    When generators are produced via functions that have side effects, any
    effects other than those needed to produce the first element in the
    sequence do not occur until it's consumed. ``dorun`` can be used to force
    any effects. Walks through the successive nexts of the sequence, does not
    retain the head and returns ``None``.
    """
    for _ in coll:
        pass


def repeatedly(f: Union[Callable[[], T2], int], n: Optional[Union[int, Callable[[], T2]]] = None) \
        -> Iterable[T2]:
    """
    Takes a function of no args, presumably with side effects, and returns an
    infinite (or length ``n`` if supplied) lazy sequence of calls to it.
    """
    # Accept Clojure-like calls of [repeatedly(n, f)]
    if callable(n) and isinstance(f, int):
        f, n = n, f

    if n is None:
        n = -1

    f = cast(Callable[[], T2], f)
    n = cast(int, n)

    while n != 0:
        yield f()
        n -= 1


def iterate(f: Callable[[Any], Any], x) -> Iterable:
    """
    Returns a generator of ``x``, ``f(x)``, ``f(f(x))``, etc.
    """
    while True:
        yield x
        x = f(x)


def repeat(x: T, n: Optional[int] = None) -> Iterable[T]:
    """
    Returns a generator that indefinitely yields ``x`` (or ``n`` times if ``n`` is supplied).

    This is equivalent to ``itertools.repeat``.
    """
    kwargs = {}
    if n is not None:
        kwargs["times"] = n
    return itertools.repeat(x, **kwargs)


def range(*args: int) -> Iterator[int]:
    """
    Usage: range()
           range(end)
           range(start, end)
           range(start, end, step)

    Returns a generator of numbers from ``start`` (inclusive) to ``end``
    (exclusive), by ``step``, where ``start`` defaults to ``0``, ``step`` to
    ``1``, and ``end`` to infinity. When ``step`` is equal to ``0``, returns an
    infinite sequence of ``start``.

    Note that this delegates to Python’s built-in ``range`` if there are arguments.
    """
    if args:
        for e in _range(*args):
            yield e
        return

    n = 0
    while True:
        yield n
        n += 1


def tree_seq(has_branch: Callable[[Any], Any], get_children: Callable[[Any], Iterable], root: Any) \
        -> Iterable:
    """
    Returns a generator of the nodes in a tree, via a depth-first walk.
    ``has_branch`` must be a function of one argument that returns ``True`` if
    passed a node that can have children (but may not). ``get_children`` must
    be a function of one argument that returns an iterable of the children.
    Will only be called on nodes for which ``has_branch`` returns true.
    ``root`` is the root node of the tree.
    """
    yield root
    if has_branch(root):
        for child in get_children(root):
            for subchild in tree_seq(has_branch, get_children, child):
                yield subchild


def dedupe(coll: Iterable[T]) -> Iterable[T]:
    """
    Returns a generator of the elements of coll with consecutive duplicates removed.
    """
    initial = True
    prev = None
    for e in coll:
        if initial or e != prev:
            initial = False
            yield e
        prev = e


def empty(coll: T) -> Optional[T]:
    """
    Returns an empty collection of the same type as ``coll``, or ``None``.
    """
    if _is_collection_abc(coll):
        return type(coll)()
    return None


# Not listed in http://clojure.org/reference/sequences but useful for
# generators to avoid doing e.g. len(list(gen)) that loads everything in
# memory.
def count(coll: Iterable) -> int:
    """
    Returns the number of items in the collection. Also works on strings.
    """
    if hasattr(coll, "__len__"):
        return len(cast(list, coll))

    n = 0
    for _ in coll:
        n += 1
    return n


def partition(coll: Iterable[T], n: int, step: Optional[int] = None, pad: Optional[Iterable[T2]] = None) \
        -> Iterator[List[Union[T, T2]]]:
    """
    Returns a generator of lists of ``n`` items each, at offsets ``step`` apart. If ``step`` is not supplied, defaults
    to ``n``, i.e. the partitions do not overlap. If a ``pad`` collection is supplied, use its elements as necessary to
    complete last partition up to ``n`` items. In case there are not enough padding elements, return a partition with
    fewer than ``n`` items.

    Note: ``step!=n`` is not supported for now.

    Note: in Clojure, ``(partition 0 [1 2 3])`` returns an infinite lazy sequence of empty lists. To avoid issues this
    Python implementation returns an empty generator if called with n≤0.
    """
    if n <= 0:
        return

    if step is not None and step != n:
        # TODO
        raise NotImplementedError("Step != n is not supported for now.")

    current_partition: List[Union[T, T2]] = []
    partition_index = 0
    partition_end = n

    for element in coll:
        current_partition.append(element)
        partition_index += 1
        if partition_index == partition_end:
            yield current_partition
            current_partition = []
            partition_index = 0
            partition_end = n

    if pad is not None and 0 < partition_index < partition_end:
        for pad_element in pad:
            current_partition.append(pad_element)
            if partition_index == partition_end:
                break

        yield current_partition

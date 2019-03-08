# -*- coding: UTF-8 -*-

__version__ = "0.1.1"

from clj.seqs import (butlast, concat, cons, count, cycle, distinct, dorun,
    drop, drop_last, drop_while, every, ffirst, first, flatten, group_by,
    interleave, interpose, is_seq, iterate, keep, keep_indexed, last,
    map_indexed, mapcat, nfirst, not_any, not_every, nth, range, reductions,
    remove, repeat, repeatedly, replace, rest, second, shuffle, some, split_at,
    split_with, take, take_nth, take_while, tree_seq, zipmap)

from clj.fns import comp, complement, constantly, dec, identity, inc, juxt

if False:  # make pyflakes happy
    comp, complement, constantly, dec, identity, inc, juxt,
    butlast, concat, cons, count, cycle, distinct, dorun,
    drop, drop_last, drop_while, every, ffirst, first, flatten, group_by,
    interleave, interpose, is_seq, iterate, keep, keep_indexed, last,
    map_indexed, mapcat, nfirst, not_any, not_every, nth, range, reductions,
    remove, repeat, repeatedly, replace, rest, second, shuffle, some, split_at,
    split_with, take, take_nth, take_while, tree_seq, zipmap,

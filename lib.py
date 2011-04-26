#!/usr/bin/env python

from inject import inject

def to_fn(what):
    if hasattr(what, '__call__'):
        return what

    if isinstance(what, basestring):
        return lambda _: 'str!'

    else:
        return lambda x: x==what


@inject(list)
def map(self, fn):
    fn = to_fn(fn)

    return [fn(_) for _ in self]


def odd(x): return x % 2 == 0




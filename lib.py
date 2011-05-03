#!/usr/bin/env python

import unittest
from inject import inject


"""
 map 
 filter / keep
 pos / index 
 some
 all
 trues
 
"""

def to_fn(what):
    if hasattr(what, '__call__'):
        return what

    if isinstance(what, basestring):
        return lambda _: eval(adjust_str_function(what))

    else:
        return lambda x: x==what

def adjust_str_function(what):
    if what[0] in '*<>%^=':
        what = '_%s' % what

    return what

@inject(list)
def trues(self):
    return [_ for _ in self if _]

@inject(list)
def map(self, fn):
    fn = to_fn(fn)

    return [fn(_) for _ in self]

@inject(list)
def pos(self, fn, default=None):
    fn = to_fn(fn)

    for i,x in enumerate(self):
        if fn(x):
            return i

    return default

@inject(list)
def index(self, fn):
    return self.pos(fn)

@inject(list)
def filter(self, fn):
    fn = to_fn(fn)

    return [_ for _ in self if fn(_)]


@inject(list)
def keep(self, fn):
    return self.filter(fn)


@inject(list)
def rem(self, fn):
    fn = to_fn(fn)

    return [_ for _ in self if not fn(_)]

@inject(list)
def all(self, fn):
    fn = to_fn(fn)

    for x in self:
        if not fn(x):
            return False
        
    return True
        
    
@inject(list)
def some(self, fn):
    fn = to_fn(fn)

    for x in self:
        if fn(x):
            return True
        
    return False

def odd(x): return x % 2 != 0
def double(x): return x*2

class LibTest(unittest.TestCase):

    def setUp(self):
        self.seq = range(5)

    def test_trues(self):
        self.assertEqual([1,2,None,3,False,4].trues(), [1,2,3,4])

    def test_map(self):
        r = self.seq.map(double)
        self.assertEqual(r, [0,2,4,6,8])

    def test_map_str(self):
        r = self.seq.map('2*_')
        self.assertEqual(r, [0,2,4,6,8])

    def test_map_str(self):
        r = self.seq.map(1)
        self.assertEqual(r, [False,True,False,False,False])

    def test_fn_str(self):
        f = to_fn('_*2')
        self.assertEqual(f(2), 4)

    def test_fn_str_operator(self):
        f = to_fn('*2')
        self.assertEqual(f(2), 4)


    def test_filter(self):
        r = self.seq.filter(odd)
        self.assertEqual(r, [1,3])

    def test_filter_str(self):
        r = self.seq.filter('odd(_)')
        self.assertEqual(r, [1,3])

    def test_filter_str(self):
        r = self.seq.filter(3)
        self.assertEqual(r, [3])

    def test_keep(self):
        r = self.seq.keep(odd)
        self.assertEqual(r, [1,3])


    def test_pos(self):
        r = self.seq.pos(odd)
        self.assertEqual(r, 1)

        r = self.seq.pos(7)
        self.assertEqual(r, None)

        r = self.seq.pos(7, -1)
        self.assertEqual(r, -1)

    def test_index(self):
        r = self.seq.index(odd)
        self.assertEqual(r, 1)


    def test_rem(self):
        r = self.seq.rem(odd)
        self.assertEqual(r, [0,2,4])

        r = self.seq.rem('>2')
        self.assertEqual(r, [0,1,2])

    def test_all(self):
        r = self.seq.all(odd)
        self.assertEqual(r, False)

        self.assertEqual([1,1].all(odd), True)
        self.assertEqual([2,2].all(2), True)

    def test_some(self):
        r = self.seq.some(odd)
        self.assert_(r)

if __name__ == '__main__':
    unittest.main()

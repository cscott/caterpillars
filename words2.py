#!/usr/bin/python
from __future__ import with_statement
import heapq
import itertools
import random
import re
from contextlib import contextmanager
random.seed(42)

MIN_SEQ_LEN=3
MAX_SEQ_LEN=4

# original ANSWER patterns
# patterns=[('*lsssslrslsrssrl', '*rlsslsrslrssssr'),
#           ('*sssrlsrsslrl', '*rlrsslsrlsss'),
#           ('*rssslslsssrsrlr', '*lrlslsssrsrsssl'),
#           ('*srlssrslrsssssrssssrlrslrlr', '*lrlrslrlsssslssssslrslssrls'),
#           ('*sslssssrsrsslss', '*ssrsslslssssrss'),
#           ('*rlrssrsssrs', '*slssslsslrl'),
#           ('*lslssslrlrlsssrlsslsl', '*rsrssrlsssrlrlrsssrsr'),
#           ('*lssrlsslssrlrsr', '*lslrlssrssrlssr'),
#           ('*srsrslrlsrsrsslrl', '*rlrsslslsrlrslsls')]
# new WIGS patterns
patterns=[('*sslssssslrl', '*rlrsssssrss'), ('*rslssslssrl', '*rlssrsssrsl'), ('*lsssrslrss', '*sslrslsssr'), ('*sssrlrssssss', '*sssssslrlsss'), ('*lslssslrlrlsssrlrsslsrl', '*rlsrsslrlsssrlrlrsssrsr'), ('*ssrsrslssr', '*lssrslslss'), ('*lrsrsssrslslrlrsr', '*lslrlrsrslssslslr'), ('*rlsssssrslrsssss', '*ssssslrslsssssrl'), ('*lrssrlsslrls', '*srlrssrlsslr'), ('*lssslrlss', '*ssrlrsssr'), ('*srsssrslrssssrsssssrs', '*slssssslsssslrslsssls'), ('*rsrssrssssrlrsrlsrlr', '*lrlsrlslrlsssslsslsl'), ('*rlrssrsssrsl', '*rslssslsslrl')]

flatpat = [p[1:] for p in itertools.chain(*patterns)]

def show_long_strings():
    # enumerate all substrings
    m = {}
    for i in xrange(len(flatpat)):
        for j in xrange(len(flatpat[i])):
            for k in xrange(j+1, len(flatpat[i])):
                s = flatpat[i][j:k]
                m.setdefault(len(s), {}).setdefault(s, 0)
                m[len(s)][s] += 1
    # print out a sorted list
    for l in sorted(m.keys()):
        flipped = [(n,s) for (s,n) in m[l].items()]
        for n,s in sorted(flipped):
            if n < 2: continue # not a reused section
            print l, n, s

class Possibility:
    def __init__(self, choices, chosen, remaining, next_unalloc=(0,0)):
        self.choices=choices
        """Array of bits, which one of the orientations for each piece."""
        self.chosen=chosen or set()
        self._next_unalloc, found = self._find_next_unalloc(*next_unalloc)
        self.remaining = remaining - found
        self._score = None

    def _find_next_unalloc(self, firsti=0, firstj=0):
        # scan through to find next piece not yet spoken for.
        found = 0
        i,j = firsti, firstj
        while i < len(patterns):
            pat = patterns[i][self.choices[i]]
            while j < len(pat):
                for k in reversed(xrange(j+1,
                                         1+min(len(pat), j+MAX_SEQ_LEN))):
                    s = pat[j:k]
                    if s in self.chosen:
                        # skip ahead
                        found += len(s)
                        j = k
                        break
                else:
                    return (i,j), found
            j = 0
            i += 1
        else:
            return None, found # all allocated!

    def is_final(self):
        return self._next_unalloc is None

    def chose_next(self, amt):
        i,j = self._next_unalloc
        pat = patterns[i][self.choices[i]]
        if (j+amt) > len(pat): return None
        nchosen = self.chosen.copy()
        nchosen.add(pat[j:j+amt])
        return Possibility(self.choices, nchosen, self.remaining,
                           self._next_unalloc)

    def score(self):
        if self._score is None:
            #((self.remaining+MAX_SEQ_LEN-1) / MAX_SEQ_LEN)
            self._score = len(self.chosen) + \
                          (1 if self.remaining > 0 else 0)
        return self._score
    def __cmp__(self, other):
        c = cmp(self.score(), other.score())
        if c != 0: return c
        return cmp(self.choices, other.choices)
    def __repr__(self):
        return "Possibility(%s, %s, %d)" % \
               (repr(self.choices), repr(self.chosen), self.remaining)

class FoundOne(Exception):
    pass

def print_solution(p):
    print "FOUND ONE", p.score()
    print p
    # assign a letter to each chosen
    m={}
    for s in p.chosen:
        if s == '*': continue
        m[s] = chr(len(m)+ord('A'))
    # now print out each word
    results=[]
    for i in xrange(len(patterns)):
        word = ''
        pat = patterns[i][p.choices[i]]
        j = 1 # skip initial *
        while j < len(pat):
            for k in reversed(xrange(j+1, 1+len(pat))):
                s = pat[j:k]
                if s in m:
                    word += m[s]
                    j = k
                    break
            else:
                assert False
        print i, word, len(word)
        results.append(word)

    print "Min", MIN_SEQ_LEN, "Max", MAX_SEQ_LEN
    print 'Number of shapes:', len(p.chosen)-1
    print 'Max word length:', max(len(w) for w in results)
    print 'Min word length:', min(len(w) for w in results)
    raise FoundOne()

def do_one(heap):
    # pull smallest item from the heap
    p = heapq.heappop(heap)
    #print "Looking at", p.score(), p, p._next_unalloc, p.remaining
    if p.is_final():
        print_solution(p)
        return
    # make a new 'letter'
    for i in xrange(MIN_SEQ_LEN, MAX_SEQ_LEN+1):
        pp = p.chose_next(i)
        if pp is not None:
            heapq.heappush(heap, pp)

def mk_initial_state(heap):
    def enum(i):
        if i >= len(patterns):
            yield []
        else:
            for r in enum(i+1):
                for j in xrange(len(patterns[i])):
                    yield [j] + r
    for choices in enum(0):
        remaining = sum(len(patterns[i][choices[i]]) \
                        for i in xrange(len(choices)))
        heapq.heappush(heap, Possibility(choices, set('*'), remaining))

heap=[]
mk_initial_state(heap)
try:
    while len(heap) > 0:
        do_one(heap)
except FoundOne:
    pass

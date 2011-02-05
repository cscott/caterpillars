#!/usr/bin/python
from __future__ import with_statement
import png
import sys

def read(filename):
    palette = {}
    with open(filename, 'rb') as f:
        width, height, pixels, metadata = png.Reader(file=f).asRGBA8()
        assert width == 16 and height==16
        def pixel(r,g,b,a):
            if r==255 and g==255 and b==255: return -1 # void
            if (r,g,b) not in palette:
                palette[(r,g,b)] = len(palette)
            return palette[(r,g,b)]
        def row(r):
            rr = list(r)
            return [pixel(*rr[i:(i+4)]) for i in xrange(0, len(rr), 4)]
        rows = [row(r) for r in pixels]
        #print len(palette)
        def char(c):
            if c < 0: return '.'
            return chr(ord('A')+c)
        return '\n'.join(''.join(char(c) for c in r) for r in rows)

filename = sys.argv[1] if len(sys.argv) > 1 else 'alternate.png'
print read(filename)

#!/usr/bin/python
from __future__ import with_statement
import png
import random
import sys
from contextlib import contextmanager

MAX_PIECES=20
MIN_PIECE_SIZE=15
MAX_PIECE_SIZE=30
random.seed(42)

class Pixel:
    # pixels belonging to specific pieces are labeled with non-negative #s
    UNKNOWN=-1
    VOID   =-2
    SOLID  =-3
    @staticmethod
    def used(p):
        return p>=0

class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)
    def __sub__(self, other):
        return Point(self.row - other.row, self.col - other.col)
    def __cmp__(self, other):
        c = cmp(self.row, other.row)
        return c if c!=0 else cmp(self.col, other.col)
    def __str__(self):
        return str(tuple([self.row, self.col]))
    def __repr__(self):
        return "Point"+str(self)
class Dir:
    NORTH='n'
    EAST ='e'
    SOUTH='s'
    WEST ='w'
    dtable = { NORTH:Point(-1,0), EAST:Point(0,+1),
               SOUTH:Point(+1,0), WEST:Point(0,-1) }
    @staticmethod
    def all():
        return [Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST]
    @staticmethod
    def dxy(dir):
        return Dir.dtable[dir]

class Image:
    def __init__(self, pixarray):
        self.rows = pixarray
        self.height = len(self.rows)
        self.width = len(self.rows[0])
        self.solids_left = sum(sum(1 for p in row if p==Pixel.SOLID)
                               for row in self.rows)
    def in_bounds_p(self, row, col):
        return row >= 0 and row < self.height and \
               col >= 0 and col < self.width
    def in_bounds_pp(self, pt):
        return self.in_bounds_p(pt.row, pt.col)

    def p(self, row, col):
        return self.rows[row][col]
    def pp(self, pt):
        return self.p(pt.row, pt.col)

    @contextmanager
    def setpp(self, pt, newv):
        with self.setp(pt.row, pt.col, newv):
            yield

    @contextmanager
    def setp(self, row, col, newv):
        """Temporarily set (row,col) to newv."""
        oldv = self.rows[row][col]
        change = 0
        if oldv==Pixel.SOLID: change -= 1
        if newv==Pixel.SOLID: change += 1
        try:
            self.rows[row][col] = newv
            self.solids_left += change
            yield
        finally:
            self.rows[row][col] = oldv
            self.solids_left -= change

    @contextmanager
    def flood_fill(self, row, col, newv):
        start = Point(row, col)
        if self.pp(start) not in [Pixel.SOLID, Pixel.UNKNOWN]:
            yield (0, Point(-1, -1))
        else:
            points = [p for p in [(start + Dir.dxy(d)) for d in Dir.all()]
                      if self.in_bounds_pp(p)]
            with self.setpp(start, newv):
                if len(points): start = points.pop()
                with self.flood_fill(start.row, start.col, newv) as (sz1,pt1):
                    if len(points): start = points.pop()
                    with self.flood_fill(start.row, start.col, newv) as (sz2,pt2):
                        if len(points): start = points.pop()
                        with self.flood_fill(start.row, start.col, newv) as (sz3,pt3):
                            if len(points): start = points.pop()
                            with self.flood_fill(start.row, start.col, newv) as (sz4,pt4):
                                yield ((1+sz1+sz2+sz3+sz4), max(start, pt1, pt2, pt3, pt4))

class Piece:
    def __init__(self, id, row, col, wiggle=None):
        self.id = id
        """Non-negative id number for this piece."""
        self.start = Point(row, col)
        """Starting row and column."""
        self.end = self.start
        """Final row and column."""
        self.wiggle = [] if wiggle is None else wiggle
        """Path from start to end"""
    def add(self, dir):
        self.wiggle.append(dir)
        self.end += Dir.dxy(dir)
    def remove(self, dir):
        self.end -= Dir.dxy(self.wiggle.pop())
    @contextmanager
    def grow(self, dir):
        self.add(dir)
        yield
        self.remove(dir)

    def end_valid(self, img):
        if not img.in_bounds_pp(self.end):
            # ends out of bounds
            return False
        p = img.pp(self.end)
        if p == Pixel.VOID or Pixel.used(p):
            # includes a space which must be empty, or already used
            # (possibly self intersecting)
            return False
        for adjpt in [(self.end + Dir.dxy(d)) for d in Dir.all()]:
            if not img.in_bounds_pp(adjpt):
                continue
            if img.pp(adjpt) == self.id:
                # adjacent to itself, not allowed (thinness criterion)
                return False
        # i guess this is an okay piece
        return True

    @contextmanager
    def mark_tail(self, img):
        #print "Marking tail at", self.end, self.wiggle[-1]
        # Mark penultimate piece as being part of us.
        with img.setpp(self.end - Dir.dxy(self.wiggle[-1]), self.id):
            # Mark the tail as being solid:
            with img.setpp(self.end, Pixel.SOLID):
                yield

    def __len__(self):
        return len(self.wiggle)
    def __repr__(self):
        return "Piece(%d, %d, %d, %s)" % (self.id,
                                          self.start.row, self.start.col,
                                          repr(''.join(self.wiggle)))


def guess():
    # should return (VOID, SOLID) or (SOLID, VOID) with appropriate
    # probabilities to ensure a decent amount of solid pixels.
    return random.choice((Pixel.VOID, Pixel.SOLID),
                         (Pixel.VOID, Pixel.SOLID),
                         (Pixel.SOLID, Pixel.VOID))

def read(filename):
    """Read in the answer template as a black+white+transparent PNG file"""
    with open(filename, 'rb') as f:
        width, height, pixels, metadata = png.Reader(file=f).asRGBA8()
        #assert width == 32 and height==16
        def pixel(r,g,b,a):
            return Pixel.UNKNOWN if a < 128 else \
                   Pixel.SOLID if r > 128 else Pixel.VOID
        def row(r):
            rr = list(r)
            return [pixel(*rr[i:(i+4)]) for i in xrange(0, len(rr), 4)]
        return Image([row(r) for r in pixels])

best_gaps=256
def check_best_solution(img, pieces):
    global best_gaps
    if img.solids_left >= best_gaps:
        return
    best_gaps = img.solids_left
    print "Best so far:", best_gaps#, find_smallest(img, 0, 0, len(pieces)+1)
    print_solution(img, pieces)
    sys.stdout.flush()

def checker(img, pieces):
    rows = [[' ' for c in xrange(img.width)] for r in xrange(img.height)]
    for p in pieces:
        pc = chr(ord('A') + p.id)
        pt = p.start
        rows[pt.row][pt.col] = pc.lower()
        for w in p.wiggle:
            pt = pt+Dir.dxy(w)
            rows[pt.row][pt.col] = pc
    for r in xrange(img.height):
        for c in xrange(img.width):
            p = img.p(r, c)
            if Pixel.used(p):
                #print p, rows[r][c], ord(rows[r][c].upper())-ord('A')
                assert p == ord(rows[r][c].upper())-ord('A')
            else:
                assert rows[r][c] == ' '

def print_solution(img, pieces):
    rows = [[' ' for c in xrange(img.width)] for r in xrange(img.height)]
    for r in xrange(img.height):
        for c in xrange(img.width):
            if img.p(r, c)==Pixel.VOID:
                rows[r][c] = '.'
            elif img.p(r, c)==Pixel.UNKNOWN:
                rows[r][c] = '_'
    for p in pieces:
        pc = chr(ord('A') + p.id)
        pt = p.start
        rows[pt.row][pt.col] = pc.lower()
        for w in p.wiggle:
            pt = pt+Dir.dxy(w)
            rows[pt.row][pt.col] = pc
    for r in rows:
        print ''.join(r)
    
def print_solution2(img):
    rows = [[' ' for c in xrange(img.width)] for r in xrange(img.height)]
    for r in xrange(img.height):
        for c in xrange(img.width):
            if img.p(r, c)==Pixel.VOID:
                rows[r][c] = '.'
            elif img.p(r, c)==Pixel.UNKNOWN:
                rows[r][c] = '_'
            elif Pixel.used(img.p(r, c)):
                rows[r][c] = chr(ord('A') + img.p(r, c))
    for r in rows:
        print ''.join(r)
    
def found_one(pieces):
    print "FOUND ONE!"
    print_solution(img, pieces)
    print pieces
    return True

def find_smallest(img, row, col, id):
    while row < img.height:
        if img.p(row, col) == Pixel.SOLID:
            with img.flood_fill(row, col, id) as (sz1, pt1):
                sz2, pt2 = find_smallest(img, row, col, id+1)
                return (min(sz1, sz2), min(pt1, pt2))
        col += 1
        if col >= img.width:
            col = 0
            row += 1
    # nothing left to fill
    #print "Flood fill complete:"
    #print_solution2(img)
    return ((img.height * img.width),
            Point(img.height, img.width)) # large sentinels

def is_blocked(img, pieces):
    return False # XXX this code is crashing XXX
    # count the number of isolated areas, ensure that smallest is still
    # larger than MIN_PIECE_SIZE
    start_id = len(pieces)+1
    small_area, small_corner = find_smallest(img, 0, 0, start_id)
    if small_area < MIN_PIECE_SIZE:
        return True
    # check that first disconnected region is reachable by current start
    # point
    if len(pieces)>0 and small_corner < pieces[-1].start:
        return True
    # I guess it's not blocked after all.
    #print "Not blocked:", small_area, small_corner
    #print_solution(img, pieces)
    #print_solution2(img)
    return False

def grow_one(img, pieces):
    piece = pieces[-1]
    # try to extend this piece
    # (try options which decrease solids left first)
    ds = [(d,piece.end + Dir.dxy(d)) for d in Dir.all()]
    ds = [(img.pp(pt)==Pixel.SOLID if img.in_bounds_pp(pt) else False,
           random.random(),
           d) for (d,pt) in ds]
    ds = [d for (_,_,d) in reversed(sorted(ds))]

    for d in ds: #random.sample(Dir.all(), 4):
        with piece.grow(d):
            # is this valid?
            if not piece.end_valid(img):
                continue
            # have we blocked something off? (XXX test is slow)
            # XXX TEST IS CRASHING
            #with img.flood_fill(piece.end.row, piece.end.col, piece.id):
            #    if is_blocked(img, pieces):
            #        continue
            # mark spaces as used by this piece
            with piece.mark_tail(img):
                with img.setpp(piece.end, piece.id):
                    check_best_solution(img, pieces)
                # are we done?
                if img.solids_left==1:
                    found_one(img, pieces)
                    return True
                # ok, try to keep growing this piece?
                if len(piece) < MAX_PIECE_SIZE:
                    if grow_one(img, pieces):
                        return True # we rock!
                # try to start next piece?
                if (len(piece) >= MIN_PIECE_SIZE and
                    len(pieces) < MAX_PIECES):
                    with img.setpp(piece.end, piece.id):
                        #checker(img, pieces)
                        if not is_blocked(img, pieces):
                            if search_from(img, piece.start, pieces):
                                return True # yeah, boyz!

            

def new_piece(img, row, col, pieces):
    """Start a new piece"""
    assert img.p(row, col) == Pixel.SOLID
    #print "Starting a piece at", row, col, "pieces", len(pieces), "left", img.solids_left
    piece = Piece(len(pieces), row, col)
    pieces.append(piece) # add new piece
    try:
        return grow_one(img, pieces)
    finally:
        pieces.pop() # remove unsuccessful piece

def search_from(img, start, pieces):
    row, col = start.row, start.col
    # find first non-void piece
    while row < img.height:
        p = img.p(row, col)
        if p != Pixel.VOID and not Pixel.used(p):
            # try to start a piece here
            with img.setp(row, col, Pixel.SOLID):
                if new_piece(img, row, col, pieces):
                    return True # success!
        col += 1
        if col >= img.width:
            col = 0
            row += 1
    return False # no success

def search(filename):
    img = read(filename)
    assert not is_blocked(img, [])
    search_from(img, Point(0, 0), [])

#search('sample.png')
search('jaguar2.png')

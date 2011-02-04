#!/usr/bin/python
from __future__ import with_statement
import itertools
import png
import random
from contextlib import contextmanager

random.seed(42)

NO_MIRROR=True
NO_ROTATION=False
UPDATE_PIECE=8

ASSEMBLED1="""
Aa..bB_BBBBB_cC_
A.gG.BBBIIIBBBCC
A..G.B.II.IB..C_
A.AG.B..i.I.CCCC
A.AG.H.e..II.EEC
AAAGHH.EE.EII.EC
_A_GGHFFEEE..EEC
_A_GHH_F__EEEE_C
AAGGHDDF_EE__EEC
A.hGH.DFFFFF_KCC
A.HHH.D...F_KK_K
A.H.H.D.FFFFFKKK
AA.A.DD..JF.F..K
DAAADDJ.JJJ..KKK
DD_DD_J...J.KK_K
_DDDJJJJJJJ.K__K
""".strip()

ASSEMBLED2="""
AA..BB.BBBBB.CC.
A.DD.BBBEEEBBBC.
A..D.B.EE.EB..C.
A.DD.B..E.E.CCCC
A.AD.B.F..EE.GGC
AAADHH.FG.GEE.GC
.A.DDHFFGGG..GGC
.A.D.H.FF.GGGGCC
AADDHHHF...GIIIC
A.HDH.HFFFFGFFII
A.HHH.H...FGGFI.
A.H.H.H.FFFFFFII
AA.A.JH..JF.F..I
.AAAJJJ.JJJ..III
JJJJJ.J...J.II..
J.J...JJJJJ.I...
""".strip()

ASSEMBLED3="""
""".strip()

ASSEMBLED=ASSEMBLED3
OUTPUT_BASENAME='output3'

class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)
    def __sub__(self, other):
        return Point(self.row - other.row, self.col - other.col)
    def rotate(self, amt):
        if amt == 0: return self
        return Point(self.col, -self.row).rotate(amt-1)
    def mirror(self):
        return Point(self.row, -self.col)
        
    def __cmp__(self, other):
        c = cmp(self.row, other.row)
        return c if c!=0 else cmp(self.col, other.col)
    def __str__(self):
        return str(tuple([self.row, self.col]))
    def __repr__(self):
        return "Point"+str(self)

class Piece:
    def __init__(self, id, mirrored=None):
        self.id = id
        self.size = Point(0,0)
        self.origin = None
        self.rows=[]
        self._mirrored=mirrored
        self._rotated=None
        self._points=None
    def __str__(self):
        pch = chr(ord('A')+self.id)
        x = '\n'.join(''.join((pch if c else ' ') for c in r)
                      for r in self.rows)
        return x
    def points(self):
        if self._points is None:
            def _mk_points():
                for r in xrange(self.size.row):
                    for c in xrange(self.size.col):
                        if self.rows[r][c]:
                            yield Point(r, c)
            self._points = list(_mk_points())
        return self._points
    def mirror(self):
        if self._mirrored is None:
            p = Piece(self.id, mirrored=self)
            for pt in self.points():
                p.add(pt.mirror() + self.size)
            self._mirrored = p
        return self._mirrored
    def rotate(self, rotation):
        if rotation == 0: return self
        assert rotation > 0
        if self._rotated is None:
            big = max(self.size.row, self.size.col)
            offset = Point(big, big)
            p = Piece(self.id)
            for pt in self.points():
                p.add(pt.rotate(1) + offset)
            self._rotated = p
        return self._rotated.rotate(rotation-1)
    
    def add(self, pt):
        assert pt.row >= 0 and pt.col >= 0
        if self.origin is None:
            self.origin = pt
        pt -= self.origin
        while pt.row < 0:
            p1 = Point(row=1, col=0)
            self.rows.insert(0, [False] * self.size.col)
            self.origin -= p1
            self.size += p1
            pt += p1
        while pt.row >= self.size.row:
            p1 = Point(row=1, col=0)
            self.rows.append([False] * self.size.col)
            self.size += p1
        while pt.col < 0:
            p1 = Point(row=0, col=1)
            for r in self.rows:
                r.insert(0, False)
            self.origin -= p1
            self.size += p1
            pt += p1
        while pt.col >= self.size.col:
            p1 = Point(row=0, col=1)
            for r in self.rows:
                r.append(False)
            self.size += p1
        assert not self.rows[pt.row][pt.col]
        self.rows[pt.row][pt.col] = True

class Position:
    def __init__(self, piece, origin):
        self.piece = piece
        self.origin = origin
    def _points(self):
        for pt in self.piece.points():
            yield pt + self.origin
    def points(self):
        return list(self._points())
    def __str__(self):
        return "Piece %d at %s" % (self.piece.id, str(self.origin))

class Image:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = [[-1 for _ in xrange(self.width)]
                     for __ in xrange(self.height)]
    def in_bounds(self, pt):
        return pt.row >= 0 and pt.row < self.height and \
               pt.col >= 0 and pt.col < self.width
    def p(self, pt):
        return self.rows[pt.row][pt.col]

    @contextmanager
    def setp(self, pt, newv):
        """Temporarily set (row,col) to newv."""
        oldv = self.rows[pt.row][pt.col]
        try:
            self.rows[pt.row][pt.col] = newv
            yield oldv
        finally:
            self.rows[pt.row][pt.col] = oldv
    @contextmanager
    def setpts(self, ptlst, newv):
        if len(ptlst)==0:
            yield True # success
        else:
            pt, ptlst = ptlst[0], ptlst[1:]
            with self.setp(pt, newv) as oldv:
                if oldv >= 0:
                    yield False # oops, already set!
                else:
                    with self.setpts(ptlst, newv) as success:
                        yield success
    def __str__(self):
        x = '\n'.join(''.join((' ' if c<0 else chr(ord('A')+c)) for c in r)
                      for r in self.rows)
        return x

def mkpieces():
    pieces = []
    pict = ASSEMBLED.split()
    for r in xrange(len(pict)):
        row = pict[r]
        for c in xrange(len(row)):
            ch = row[c].upper()
            if ch in "._ ": continue
            cid = ord(ch) - ord('A')
            # make sure there are enough pieces
            while cid >= len(pieces):
                pieces.append(Piece(len(pieces)))
            # add this to the appropriate piece
            pieces[cid].add(Point(r, c))
    return (len(pict), len(pict[0]), pieces)

TOTAL_FOUND=0
def place_one(img, pieces, result):
    global TOTAL_FOUND
    if len(pieces)==0:
        print "Found one!"
        print ', '.join(str(r) for r in result)
        print img
        output_png("%s-%02d.png" % (OUTPUT_BASENAME, TOTAL_FOUND), img)
        TOTAL_FOUND += 1
        return 1 # success
    num_results = 0
    piece = pieces[0]
    for place in gen_placements(piece, img.height, img.width):
        #if piece.id==1 and place.origin.col < 4: continue # XXX TESTING
        if len(pieces) >= UPDATE_PIECE:
            print "Attempting to place", place
        with img.setpts(place.points(), place.piece.id) as success:
            if success:
                num_results += place_one(img, pieces[1:], result+[place])
    return num_results

def gen_placements(piece, height, width):
    rp = piece
    for rotation in xrange(4):
        mp = rp
        for mirror in xrange(2):
            for r in xrange(height):
                if (r+mp.size.row) > height: continue
                for c in xrange(width):
                    if (c+mp.size.col) > width: continue
                    yield Position(mp, Point(r,c))
            if NO_MIRROR or piece.id==0: break
            mp = mp.mirror()
        if NO_ROTATION or piece.id==0: break
        rp = rp.rotate(1)

def solve(height, width, pieces):
    print_pieces(pieces)
    num_sol = place_one(Image(height, width), pieces, [])
    print num_sol, "solutions found."


def print_pieces(pieces):
    i=0
    for p in pieces:
        print '#',i, "original origin", p.origin
        print str(p)
        #print "-"
        #print str(p.rotate(1))
        i+=1

def colors():
    for r in [0, 64, 128, 192, 255]:
        for g in [0, 64, 128, 192, 255]:
            for b in [0, 64, 128, 192, 255]:
                # skip white and black
                if r==0 and g==0 and b==0: continue
                if r==255 and g==255 and b==255: continue
                yield (r,g,b,255) # rgba

def assemble_img(img, pieces, func):
    if len(pieces)==0:
        func(img)
    else:
        p, pieces = pieces[0], pieces[1:]
        place = Position(p, p.origin)
        with img.setpts(place.points(), place.piece.id) as x:
            assert x
            assemble_img(img, pieces, func)

COLORS=list(colors())
PALETTE = random.sample(COLORS, len(COLORS))
TRANSPARENT = (0,0,0,0)
WHITE = (255,255,255,255)

def output_png(filename, img):
    global PALETTE, COLORS, WHITE, TRANSPARENT
    def color_for(p):
        return WHITE if p < 0 else PALETTE[p]
    rows = [[color_for(img.p(Point(r,c))) for c in xrange(img.width)]
            for r in xrange(img.height)]
    # flatten the row
    rows = [list(itertools.chain(*r)) for r in rows]
    w = png.Writer(img.width, img.height, alpha=True, bitdepth=8)
    f = open(filename, 'wb')
    w.write(f, rows)
    f.close()

def do_output_png(filename, height, width, pieces):
    img = Image(height, width)
    assemble_img(img, pieces, lambda img: output_png(filename, img))

def show_pieces(height, width, pieces):
    # rotate some of them so that "L hook" is consistent.
    for n,r in [(0,3),(1,2),(2,1),(3,1),(6,1),(7,1),(8,1)]:
        pieces[n] = pieces[n].rotate(r)
    print_pieces(pieces)

def emit_pieces(height, width, pieces):
    # compute max # of points in a piece
    max_pts = max(len(p.points()) for p in pieces)
    print "#define HEIGHT", height
    print "#define WIDTH", width
    print "#define NUM_PIECES", len(pieces)
    print "struct piece {"
    print "  int id;"
    print "  int height;"
    print "  int width;"
    print "  int num_points;"
    print "  struct { int row; int col; } points[%d];" % max_pts
    print "} pieces[%d][4/*rotations*/] = {" % len(pieces)
    for p in pieces:
        print "  {"
        for rotation in xrange(4):
            rp = p.rotate(rotation)
            print "    {     /* ROTATION #%d */" % rotation
            print "      %-2d, /* id     */" % rp.id
            print "      %-2d, /* height */" % rp.size.row
            print "      %-2d, /* width  */" % rp.size.col
            print "      %-2d, /* # pts  */" % len(rp.points())
            print "      {"
            print "       ",
            i=0
            for pt in rp.points():
                if i==8:
                    print
                    print "       ",
                    i=0
                print ("{%2d,%2d}," % (pt.row, pt.col)),
                i+=1
            print
            print "      }"
            print "    },"
        print "  },"
    print "};"

#solve(*mkpieces())
do_output_png('output3.png', *mkpieces())
#show_pieces(*mkpieces())
#emit_pieces(*mkpieces())

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
AADDHHHF..FGIIIC
A.HDH.HFFFFGFFII
A.HHH.H...FGGFI.
A.H.H.H.FFFFFFII
AA.A.JH..JF.F..I
.AAAJJJ.JJJ..III
JJJJJ.J...J.II..
J.J...JJJJJ.I...
""".strip()

ASSEMBLED3="""
AA..BBBBBDDD....
A.CC.CCCBBBDDDD.
A..C.C.CC.B...D.
A.EC.C..C.B.FFDD
A.EC.C.D..BB.FFD
AAECCC.DD.FBB.FD
.AEEEEEEDDF...FD
.AAA...E.DFFFFFD
GGGAEEEE.DD....D
G.GAE.HHHHDDDDDD
G.AAE.H..HHHHIII
G.A.E.H.II..H..I
GG.H.HH..II..III
.GGHHH..GGI.II..
..GGGGG..GI.I...
......GGGGIII...
""".strip()

# new critic meta answer
ASSEMBLED4="""
A...B ..CCCCDDDDDDDEEEEEEE_EEE__
AA. B.  . .C CCCCCDDDDDDDEEE_E__
FA. B.. . .CCC. .C.G.  .D ..DEE_
FA.BB.A . .   ..CC.G.. .D.  DDEE
FA_B .AA. ... . . .G.H..D. ..D_E
FAABBBBAAAAGGGGGGGGG.H .D.  .D_E
FFAA__BB_BAGIIII____ HHHDD..DDEE
JF_A___BBBAGG__I_______HHDDDDEEK
JF_AAAAAAAA_G__I________H__EEEKK
JFFF...LL..GGIII III _HHHEEE_KK_
JJ_F .LL. F.II...I.I.HH..EHHHK__
_JFF .L ..F.I.   I.I.H.  .H HKKK
JJF. .LL.FF.I. ..I. .H.. .H. ..K
J_F..FFF.F .I.  .I. .H.  .H..KKK
JJFFFF_FFFJJII..II...H.  .H.KK__
_JJJJJJJJJJ__IIII    HHHHHH.K___
""".replace('_','.').replace(' ','.').strip()

ASSEMBLED5="""
A...BB..CCDD.DDDEEEEEEE....FF...
AA.AB.GG.C.D.D.EEHHHHHEEEFFFIIII
.A.AB..G.C.D.D.E.H.J.HH.FF..IFFI
.A.AB.KG.C.DDD..HH.J..H.F.IIIF.I
.A.AB.KG.C...L.M.J.J.N..F.I..F.I
.AAABKKGCCOOOLLMMJJJ.NN.F.II.F.I
...BBKGGC...OOLLM..MMMNNFF..FFII
..BB.KG.CCCCCOOLMMMMLLLN.FFFFII.
..BKKKGGPPPPCCOLLLLLLNNN...III..
..BK...GP..PPCOOOQQQNNIIIIII....
.BBKK.GG.RR.PC...Q.Q.II..SSSSS..
.BGGK.GR..R.P.QQQQ.Q.I.TT.UUUSSS
BBG.K.GR.RR.P.Q..V.Q.I..T.U.U..S
B.G..GGR.RV.P.QQ.V.Q.I.TT.U..SSS
BBGGGG.RRRVVPP..VV...I.TU.U.SS..
.BBBBBBBBBBVVVVVVTTTTTTTUUU.S...
""".strip()

ASSEMBLED6="""
A...BB...CCCDDDDD.EEEEE.........
AA.FB.CC.C.CDCCCDEEGGGEEEEEEE...
.A.FB..C.C.CCC.CDD.G.GG.HH..EHHH
.A.FB.IC.C.III.C.D.G..G.H.EEEH.H
.A.FB.IC.C...I..DD.G.J..H.E..H.H
.AFFBBICCCIIII.K.G.G.JL.H.EE.H.H
.AF..BIIIIIMMMMKJGGGJJLLHH..HH.H
.AF..BBBB.....MKJ..JJ..LLHHHH..H
.AFFFFFFBBB...MKJJJJ....L......H
.AA...NF..BBMMMKK.LLLLLLLOOOOOHH
..AA.NN.PP.MM...KLLQQQ...ORRROOO
.NNA.NP..P.M.KKKKL.Q.Q.RR.R.R..O
.N.A.NP.PP.M.K..SL.Q.Q..R.R..OOO
.N..NNP.PS.M.KK.SL.Q.Q.QR.R.OO..
.NNNN.PPPSSSS...SL.Q.Q.QR.R.O...
............SSSSSL...QQQRRROO...
""".strip()

ASSEMBLED6="""
A...BB...CCCDDDDD.EEEEE......HHH
AA.FB.CC.C.CDCCCDEEGGGEEEEEEEH.H
.A.FB..C.C.CCC.CDD.G.GG.HH..EH.H
.A.FB.IC.C.III.C.D.G..G.H.EEEH.H
.A.FB.IC.C...I..DD.G.J..H.E..H.H
.AFFBBICCCIIII.K.G.G.JL.H.EE.H.H
.AF..BIIIIIMMMMKJGGGJJLLHH..HH.H
.AF..BBBBMMM..MKJ..JJ..LLHHHH..H
.AFFFFFFBBB...MKJJJJ....L......H
.AA...NF..BBMMMKK.LLLLLLLOOOOOHH
..AA.NN.PP.MM...KLLQQQ...ORRROOO
.NNA.NP..P.M.KKKKL.Q.Q.RR.R.R..O
.N.A.NP.PP.M.K..SL.Q.Q..R.R..OOO
.N..NNP.PS.M.KK.SL.Q.Q.QR.R.OO..
.NNNN.PPPSSSS...SL.Q.Q.QR.R.O..O
............SSSSSL...QQQRRR.OOOO
""".strip()

"""New, shorter, critic meta answer."""
ASSEMBLED7="""
AAAABBBBBCDDDDD.
AEEEBFFFBCCCCCDD
AE.EBF.FBB...C.D
AE.BBF.FFFF.GCCD
AE.B.F.GGGF.GGCD
AEE.G.GG.G...GCD
AAEEGGGHHGGGGGCD
IAAEEEEEHHHHHHHD
IIJJ...EEKKKKKHD
.IJ.LLLLEK...KHH
.IJ.L..LEK.MMKKH
IIJ.LL.LEEE.MMKH
ILJJ...LMMEE.MKH
ILLJJJJLKM...MKH
IILLL.LLKMMMMMKH
.IIILLL.KKKKKKKH
""".strip()

"""Tweak interlocking for solvability missing 1 piece."""
ASSEMBLED8="""
AAAABBBBBBCCCCC.
ADDDBEEE.FFFFFCC
AD.DBE.EFF...F.C
AD.BBE.EEEE.GFFC
AD.B.E.GGGE.GGFC
ADD.G.GG.G...GFC
AADDGGGHHGGGGGFF
IAADDDDDHHHHHHHF
IIAA...DDJJJJJH.
.II.KKKKDJ...JHH
.LI.K..KDJ.MMJJH
LLI.KK.KDDD.MMJH
LKII...KMMDD.MJH
LKKIIIIKJM...MJH
LLKKKK.KJMMMMMJH
.LLLLKKKJJJJJJJH
""".strip()

# non-critic version: OCTOPOD
ASSEMBLED9="""
..AAAA.BBBBCCCC.
.AA..ABB..B...C.
.A....B.FBBE.EC.
.A....B.FFFE.EC.
AAA..BBB..FE.EC.
..AABBFFFFFEEEC.
...AFFF..DDECCCC
...AAA....DEC...
....GA....DEC...
....GAA..DDEC...
.GGGGGDDDDEECC..
.G...DD..EE..CC.
.G...D....H...C.
.G...D....H...C.
.G.DDDH..HH..CCC
GG.DHHHHHHCCCC..
""".strip()

ASSEMBLED10="""
.AAAABBCCCDDDDD.
AA..ABCC..D...D.
A....BC.DDDE.DD.
A....BC.FFFE.D..
AB..BBCC..FE.D..
ABBBB.GCCCFEDD..
AAAA.GG..CFED...
...A.G....FED...
AAAAGG....FED...
GGGGGHH..FFED...
G...HHGGGF.EDDD.
G...HGG..FFE..DD
G...HG....FE...D
G.HHHG....FE...D
G.HGGGF..FFE..DD
GGGG..FFFFEEDDD.
""".strip()

ASSEMBLED11="""
.AAAABBCCCDDDDD.
AA..ABCC..D...D.
A....BC.EEEE.DD.
A....BC.ECCE.D..
AB..BBCC..CE.D..
ABBBB.FCCCCEDD..
AAAA.FF..GGED...
...A.F....GED...
AAAAFF....GED...
FFFFFHH..GGED...
F...HHFFFG.EDDD.
F...HFF..GGE..DD
F...HF....GE...D
F.HHHF....GE...D
F.HFFFG..GGE..DD
FFFF..GGGGEEDDD.
""".strip()

ASSEMBLED12="""
.AAAABBCCCDDDDD.
AA..ABCC..D...D.
A....BC.EEEE.DD.
A....BC.ECCE.D..
AB..BBCC..CE.D..
ABBBB.FCCCCEDD..
AAA..FF..GGED...
..A..F....GED...
AAAFFF....GED...
FFFFHHH..GGED...
F...H.FFFG.EDDD.
F...HFF..GGE..DD
F...HF....GE...D
F.HHHF....GE...D
F.HFFFG..GGE..DD
FFFF..GGGGEEDDD.
""".strip()

ASSEMBLED13="""
.AAAABBCCCDDDDD.
AA..ABCC..D...D.
A....BC.EEEE.DD.
A....BC.ECCE.D..
AB..BBCC..CE.D..
ABBBB.FCCCCEDD..
AAAA.FF..GGED...
...A.F....GED...
AAAAFF....GED...
FFFFFHH..GGED...
F...HHGGGG.EDDD.
F...HGG..HHE..DD
F...HG....HE...D
F.FFHG....HE...D
F.F.HGG..HHE..DD
FFF.HHHHHHEEDDD.
""".strip()

ALL_PUZZLES=[ASSEMBLED1, ASSEMBLED2, ASSEMBLED3, ASSEMBLED4, ASSEMBLED5,
             ASSEMBLED6, ASSEMBLED7, ASSEMBLED8, ASSEMBLED9, ASSEMBLED10,
             ASSEMBLED11, ASSEMBLED12, ASSEMBLED13]

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
    def p(self, pt):
        return self.rows[pt.row][pt.col]

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

def mkpieces(ASSEMBLED):
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
def place_one(img, pieces, result, output_basename):
    global TOTAL_FOUND
    if len(pieces)==0:
        print "Found one!"
        print ', '.join(str(r) for r in result)
        print img
        output_png("%s-%02d.png" % (output_basename, TOTAL_FOUND), img)
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
                num_results += place_one(img, pieces[1:], result+[place],
                                         output_basename)
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

def solve(height, width, pieces, output_basename):
    print_pieces(pieces)
    num_sol = place_one(Image(height, width), pieces, [], output_basename)
    print num_sol, "solutions found."


def print_pieces(pieces):
    for p in pieces:
        print '#',p.id, "original origin", p.origin
        print str(p)

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

def to_relative(path, prevdir=None):
    if len(path)==0: return ''
    nextdir, path = path[0], path[1:]
    if prevdir is None:
        return '*' + to_relative(path, nextdir)
    if nextdir == prevdir:
        return 's' + to_relative(path, nextdir)
    if (prevdir,nextdir) in [('n','e'), ('e','s'), ('s','w'), ('w','n')]:
        return 'r' + to_relative(path, nextdir)
    if (prevdir,nextdir) in [('n','w'), ('e','n'), ('s','e'), ('w','s')]:
        return 'l' + to_relative(path, nextdir)
    assert False

def trace_from(piece, pt):
    last=None
    result=[]
    neigh={'n':Point(-1,0), 'e':Point(0,1), 's':Point(1,0), 'w':Point(0,-1)}
    found_next = True
    while found_next:
        found_next = False
        for dir,dpt in neigh.iteritems():
            npt = pt + dpt
            if last is not None and npt == last: continue
            if npt.row < 0 or npt.col < 0: continue
            if npt.row >= piece.size.row or npt.col >= piece.size.col: continue
            if not piece.p(npt): continue
            # ok, this is the next point
            last = pt
            pt = npt
            result.append(dir)
            found_next = True
            break
    dir_str = ''.join(result)
    rel_str = to_relative(dir_str)
    print "Tracing #", piece.id, "from", pt, "length", len(dir_str)+1
    print 'Absolute:', dir_str
    print 'Relative:', rel_str
    return rel_str

def show_piece(piece):
    # find starting location (only one orthogonal neighbor)
    results=[]
    for pt in piece.points():
        neighbors=0
        if pt.row > 0 and piece.p(pt+Point(-1,0)): neighbors+=1
        if pt.col > 0 and piece.p(pt+Point(0,-1)): neighbors+=1
        if pt.row < (piece.size.row-1) and piece.p(pt+Point(1,0)): neighbors+=1
        if pt.col < (piece.size.col-1) and piece.p(pt+Point(0,1)): neighbors+=1
        assert neighbors in [1,2]
        if neighbors==1:
            results.append(trace_from(piece, pt))
    return tuple(results)

def show_pieces(height, width, pieces):
    results=[]
    for p in pieces:
        print_pieces([p])
        results.append(show_piece(p))
    print results

def emit_pieces(f, height, width, pieces):
    # compute max # of points in a piece
    max_pts = max(len(p.points()) for p in pieces)
    print >>f, "#define HEIGHT", height
    print >>f, "#define WIDTH", width
    print >>f, "#define NUM_PIECES", len(pieces)
    print >>f, "struct piece {"
    print >>f, "  int id;"
    print >>f, "  int height;"
    print >>f, "  int width;"
    print >>f, "  int num_points;"
    print >>f, "  struct { int row; int col; } points[%d];" % max_pts
    print >>f, "} pieces[%d][8/*rotations,mirroring*/] = {" % len(pieces)
    for p in pieces:
        print >>f, "  { /* Piece #%d */" % p.id
        for mirror in xrange(2):
            mp = p
            for rotation in xrange(4):
                rp = mp.rotate(rotation)
                print >>f, "    {     /* ROTATION #%d %s*/" % \
                      (rotation, ("MIRRORED " if mirror==1 else ""))
                print >>f, "      %-2d, /* id     */" % rp.id
                print >>f, "      %-2d, /* height */" % rp.size.row
                print >>f, "      %-2d, /* width  */" % rp.size.col
                print >>f, "      %-2d, /* # pts  */" % len(rp.points())
                print >>f, "      {"
                print >>f, "       ",
                i=0
                for pt in rp.points():
                    if i==8:
                        print >>f
                        print >>f, "       ",
                        i=0
                    print >>f, ("{%2d,%2d}," % (pt.row, pt.col)),
                    i+=1
                print >>f
                print >>f, "      }"
                print >>f, "    },"
            mp = mp.mirror()
        print >>f, "  },"
    print >>f, "};"

def write_headers():
    for i in xrange(len(ALL_PUZZLES)):
        with open('pieces%d.h' % (i+1), 'w') as f:
            emit_pieces(f, *mkpieces(ALL_PUZZLES[i]))

def write_pngs():
    for i in xrange(len(ALL_PUZZLES)):
        do_output_png('output%d.png' % (i+1), *mkpieces(ALL_PUZZLES[i]))

write_headers()
write_pngs()
#solve(*mkpieces(ASSEMBLED2(), 'output2'))
show_pieces(*mkpieces(ALL_PUZZLES[-1]))

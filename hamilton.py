#!/usr/bin/python
from __future__ import with_statement, division
import heapq
import itertools
import random
random.seed(1949)

ASSEMBLED="""
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

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.edges = []
    def __hash__(self):
        return hash((self.row,self.col))
    def __eq__(self, other):
        return (self.row, self.col) == (other.row, other.col)
    def __str__(self):
        return "(%d,%d)" % (self.row, self.col)
    def __repr__(self):
        return "Cell(%d,%d)" % (self.row, self.col)
class Edge:
    def __init__(self, fr, to):
        self.fr = fr
        self.to = to
        self.weight = random.random()
    def __hash__(self):
        return hash(self.fr) ^ hash(self.to)
    def __eq__(self, other):
        return (self.fr == other.fr and self.to == other.to)
    def __str__(self):
        return "%s-%s" % (str(self.fr), str(self.to))
    def __repr__(self):
        return "Edge(%s,%s)" % (repr(self.fr), repr(self.to))

def make_cells(ascii):
    cells = {}
    row = 1
    maxcol = 0
    # parse diagram and add cells for non-void spaces
    for row_str in ascii.split():
        col = 1
        cells[row] = {}
        for col_str in row_str:
            if col_str!='.':
                c = Cell(row, col)
                cells[row][col] = c
            col +=1
            maxcol = max(maxcol, col)
        row += 1
    maxrow = row
    # add cells for borders
    cells[0] = {}
    cells[maxrow] = {}
    for col in xrange(maxcol+1):
        cells[0][col] = Cell(0, col)
        cells[maxrow][col] = Cell(maxrow, col)
    for row in xrange(1, maxrow):
        cells[row][0] = Cell(row, 0)
        cells[row][maxcol] = Cell(row, maxcol)
    # now connect all the cells
    for row in cells.keys():
        for col in cells[row].keys():
            # up
            if (row-1) in cells and col in cells[row-1]:
                e = Edge(cells[row][col], cells[row-1][col])
                cells[row][col].edges.append(e)
            # down
            if (row+1) in cells and col in cells[row+1]:
                e = Edge(cells[row][col], cells[row+1][col])
                cells[row][col].edges.append(e)
            # left
            if (col-1) in cells[row]:
                e = Edge(cells[row][col], cells[row][col-1])
                cells[row][col].edges.append(e)
            # right
            if (col+1) in cells[row]:
                e = Edge(cells[row][col], cells[row][col+1])
                cells[row][col].edges.append(e)
    # put all the cells together
    return list(itertools.chain.from_iterable(r.itervalues()
                                              for r in cells.itervalues()))

def make_spanning_tree():
    cells = make_cells(ASSEMBLED)
    # set up spanning tree algorithm
    connected = set()
    worklist = []
    edges = set()
    # pick a starting cell at random
    start = random.choice(cells)
    connected.add(start)
    # add its edges to priority queue
    for e in start.edges:
        heapq.heappush(worklist, (e.weight, e))
    # until our worklist is empty...
    while worklist:
        # take an edge
        _,e = heapq.heappop(worklist)
        # is the node it connects already connected?
        if e.to in connected: continue
        # ok, that's good.  let's connect it!
        connected.add(e.to)
        edges.add(e)
        for ee in e.to.edges:
            if ee.to in connected: continue # premature optimization
            heapq.heappush(worklist, (ee.weight, ee))
    # ok! now let's strip all except for these edges from the graph
    for c in cells:
        c.edges = [e for e in c.edges if e in edges]
    # done.
    return start, cells

SVG_TMPL="""<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="10cm" height="10cm" version="1.1"
     viewBox="0 0 1000 1000" preserveAspectRatio="true"
     xmlns="http://www.w3.org/2000/svg">
  <desc>Jigsaw Hamiltonian</desc>

  <!-- Show outline of canvas using 'rect' element -->
  <rect x="0" y="0" width="1000" height="1000"
        fill="none" stroke="blue" stroke-width="2" />
  <!-- our stuff goes here -->
  %s
  </svg>
"""

# blocks are 10 units on a side; 0,0 is the center of a block
def center_coord(cell):
    return '%d,%d' % (cell.col*10, cell.row*10)

def _spanning_tree_path(start):
    first = True
    p = ''
    for e in start.edges:
        if first:
            first = False
        else:
            p += 'M %s L ' % center_coord(start)
        p += '%s ' % center_coord(e.to)
        p += _spanning_tree_path(e.to)
    return p
def spanning_tree_path(start):
    return ('M %s L ' % center_coord(start)) + _spanning_tree_path(start)

def spanning_circuit_path(start):
    # "Easier to do this by taking the spanning tree, making the stroke 3.3mm
    # wide, and using inkscape's "convert stroke to path" feature.  That way
    # you can get nice rounded corners & everything.
    pass

def draw_spanning_tree():
    start, cells = make_spanning_tree()
    p =  spanning_tree_path(start)
    p = "<path d=\"%s\" fill=\"none\" stroke=\"black\" stroke-width=\"1\" />" % p
    # add stuff
    print SVG_TMPL % p

def find_hamiltonian():
    cells = make_cells(ASSEMBLED)



draw_spanning_tree()

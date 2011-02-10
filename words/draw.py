#!/usr/bin/python
import itertools

alphabet={
    'A': 'srlss', 'B': 'rslrs', 'C': 'rlrss', 'D': 'ssssr', 'E': 'slr',
    'F': 'slss', 'G': 'lrlsl', 'H': 'rsss', 'I': 'rsl', 'J': 'slsrl',
    'K': 'slsr', 'L': 'lssrl', 'M': 'rlr', 'N': 'lrs', 'O': 'ssss',
    'P': 'srs', 'Q': 'lss', 'R': 'lslss', 'S': 'srls', 'T': 'ssr',
    'U': 'ssl', 'V': 'rsrss', 'W': 'lrlss', 'X': 'lsls',
    'Y': 'sss', 'Z': 'lrsrs'
    }
rev_alpha = dict((y,x) for x,y in alphabet.items())

words = [
    'ABDOMEN','CHI','REWAX','MUST','MUJIK','QUIPS','LUTZ','GYVE','TUFTY',
    'THE', 'QUICK', 'BROWN', 'FOX', 'JUMPS', 'OVER', 'THE', 'LAZY', 'DOG',
    'HOW', 'QUICKLY', 'DAFT','JUMPING','ZEBRAS','VEX'
    ]


WORDFILE='enable1.txt'
MIN_SEQ_LEN=3
MAX_SEQ_LEN=5
DICT=None
def read_dict():
    global DICT
    if DICT is not None: return # already read
    DICT=set()
    with open(WORDFILE) as f:
        while True:
            word = f.readline()
            if not word: break
            word = word.strip().upper()
            if not word: continue
            DICT.add(word)

def pat_from_word(word, sep=False):
    def a(c):
        return alphabet[c] + ('|' if sep else '')
    return ''.join(itertools.chain(*[a(c) for c in word]))

def possible_letters(pat):
    if pat=='':
        yield ''
        return
    for i in xrange(MIN_SEQ_LEN, MAX_SEQ_LEN+1):
        if i > len(pat): break
        a,b = pat[:i], pat[i:]
        if a.endswith('*'):
            l = [(a[:(i-1)] + x) for x in ['r', 'l', 's']]
        else:
            l = [a]
        for aa in l:
            if aa in rev_alpha:
                for w in possible_letters(b):
                    yield rev_alpha[aa] + w

def all_words(word):
    read_dict()
    pat = pat_from_word(word)
    # the last character is really a star
    pat = pat[:-1] + '*'
    for w in possible_letters(pat):
        if w in DICT:
            yield w

def check_words(words):
    for w in words:
        print w, ":",
        for wp in all_words(w):
            print wp,
        print

class Direction:
    NORTH=0
    EAST=1
    SOUTH=2
    WEST=3
    @staticmethod
    def add(p1, p2):
        return (p1+p2) % 4
    @staticmethod
    def toxy(d):
        return [(0,-1), (1,0), (0,1), (-1,0)][d]
    @staticmethod
    def rotate(d, x, y):
        xx,xy = Direction.toxy(Direction.add(d, 1))
        yx,yy = Direction.toxy(Direction.add(d, 2))
        return (x*xx + y*yx, x*xy + y*yy)
    @staticmethod
    def rotates(d, x, y):
        return " %d,%d " % Direction.rotate(d, x, y)

def enddir(pat, direction):
    if pat=='': return direction
    head, tail = pat[0], pat[1:]
    if head=='s':
        return enddir(tail, direction)
    elif head=='l':
        direction = Direction.add(direction, 3)
        return enddir(tail, direction)
    elif head=='r':
        direction = Direction.add(direction, 1)
        return enddir(tail, direction)
    elif head=='|':
        return enddir(tail, direction) # ignore
    else:
        assert False

def centerpoint(pat, direction):
    if pat=='':
        return (0,0)
    head, tail = pat[0], pat[1:]
    if head=='s':
        x, y = centerpoint(tail, direction)
        x1, y1 = Direction.toxy(direction)
        return (x+10*x1, y+10*y1)
    elif head=='l':
        direction = Direction.add(direction, 3)
        x, y = centerpoint(tail, direction)
        x1, y1 = Direction.toxy(direction)
        return (x+10*x1, y+10*y1)
    elif head=='r':
        direction = Direction.add(direction, 1)
        x, y = centerpoint(tail, direction)
        x1, y1 = Direction.toxy(direction)
        return (x+10*x1, y+10*y1)
    elif head=='|':
        return centerpoint(tail, direction) # ignore
    else:
        assert False

def path_mouth(direction):
    d = direction
    p = "l" + Direction.rotates(d, -3, 5)
    p += "l" + Direction.rotates(d, -3, -5)
    return p

def path_halfmouth(pat, direction):
    d = direction
    p = "l" + Direction.rotates(d, -3, 5)
    p += "l" + Direction.rotates(d, +3, -5) # retrace
    # back at the mouth opening
    p += path(pat, direction)
    # at the other side of the mouth
    p += "l" + Direction.rotates(d, 3, 5)
    p += "l" + Direction.rotates(d, -3, -5) # retrace
    return p

def path_straight(pat, direction):
    d = direction
    p  = "a 2,2 0 0,0" + Direction.rotates(d, 2, -2)
    p += "l" + Direction.rotates(d, 0, -6)
    p += "a 2,2 0 0,0" + Direction.rotates(d,-2, -2)
    p += path(pat, direction)
    p += "a 2,2 0 0,0" + Direction.rotates(d,-2,  2)
    p += "l" + Direction.rotates(d, 0, 6)
    p += "a 2,2 0 0,0" + Direction.rotates(d, 2,  2)
    return p

def path_left(pat, direction):
    d = direction
    p  = "a 2,2 0 0,0" + Direction.rotates(d, 2, -2)
    p += "l" + Direction.rotates(d, 0, -6)
    p += "a 2,2 0 0,0" + Direction.rotates(d,-2, -2)
    p += "l" + Direction.rotates(d, -6, 0)
    p += "a 2,2 0 0,0" + Direction.rotates(d,-2,  2)

    p += path(pat, Direction.add(d, 3))

    p += "a 2,2 0 0,0" + Direction.rotates(d, 2,  2)
    return p

def path_right(pat, direction):
    d = direction
    p  = "a 2,2 0 0,0" + Direction.rotates(d, 2, -2)
    p += path(pat, Direction.add(d, 1))
    p += "a 2,2 0 0,0" + Direction.rotates(d,-2, -2)
    p += "l" + Direction.rotates(d, -6, 0)
    p += "a 2,2 0 0,0" + Direction.rotates(d,-2,  2)
    p += "l" + Direction.rotates(d, 0, 6)
    p += "a 2,2 0 0,0" + Direction.rotates(d, 2,  2)
    return p

def path(pat, direction):
    if pat=='':
        return path_mouth(direction)
    head, tail = pat[0], pat[1:]
    if head=='s':
        return path_straight(tail, direction)
    elif head=='l':
        return path_left(tail, direction)
    elif head=='r':
        return path_right(tail, direction)
    elif head=='|':
        return path_halfmouth(tail, direction)
    else:
        assert false

def path_egg(pat, direction):
    d = direction
    # 0,0 is the center of the egg; blocks are 10 units on a side,
    # rectangles are rounded with rx/ry = 2
    # draw as if direction was NORTH and thus mouth is UP
    p = "M" + Direction.rotates(d, 0, 5)
    p += "l" + Direction.rotates(d, 3, 0)
    p += "a 2,2 0 0,0" + Direction.rotates(d, 2, -2)
    p += "l" + Direction.rotates(d, 0, -6)
    p += "a 2,2 0 0,0" + Direction.rotates(d, -2, -2)
    # now we're at start of mouth
    p += path_halfmouth(pat, direction)
    # now we're at close of mouth
    p += "a 2,2 0 0,0" + Direction.rotates(d, -2, 2)
    p += "l" + Direction.rotates(d, 0, 6)
    p += "a 2,2 0 0,0" + Direction.rotates(d, 2, 2)
    p += "L" + Direction.rotates(d, 0, 5)
    return p

def draw_word(word):
    pat = pat_from_word(word, sep=True)
    direction = Direction.EAST
    # draw first half of the tail
    p = path_egg(pat, direction)
    p = "<path d=\"%s\" fill=\"green\" stroke=\"black\" stroke-width=\".5\" />" % p
    i = 0
    for c in word:
        j = pat.find('|', i)
        if j < 0: break
        # add eyes at the head
        x,y = centerpoint('s'+pat[:(j-1)], direction)
        x1,y1 = Direction.rotate(enddir('s'+pat[:j], direction), -3, 0)
        p += "<circle cx=\"%d\" cy=\"%d\" r=\"%d\" fill=\"black\" />" % \
             (x+x1,y+y1,1)
        # add letters at the midpoint
        k = (i+j-1)//2
        x,y = centerpoint('s'+pat[:k], direction)
        p += "<text x=\"%d\" y=\"%d\" style=\"text-anchor: middle\" font-size=\"8\">%s</text>" % (x, y+3, c)
        i=j+1
    return p


SVG_TMPL="""<?xml version="1.0" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="10cm" height="10cm" version="1.1"
     viewBox="0 0 1000 1000" preserveAspectRatio="true"
     xmlns="http://www.w3.org/2000/svg">
  <desc>Caterpillars!</desc>

  <!-- Show outline of canvas using 'rect' element -->
  <rect x="0" y="0" width="1000" height="1000"
        fill="none" stroke="blue" stroke-width="2" />
  <!-- our stuff goes here -->
  %s
  </svg>
"""

def draw_words(words):
    p = ''
    # now print the words
    x,y=40,10
    for w in words:
        p += "<g transform=\"translate(%d,%d)\">" % (x,y)
        p += draw_word(w)
        p += "</g>\n"
        x += 100
        if x > 1000:
            x = 40
            y += 200

    print SVG_TMPL % p

#check_words(words)
draw_words(words)

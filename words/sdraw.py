#!/usr/bin/python
"""Simple version of drawing, no alphabetic step."""
import draw
import random
from draw import Direction
random.seed(4242)

# from output of check.py
pieces = [('*rssssrsrlssslslr', '*lrsrsssrlslssssl'), ('*rsrssssssrsssssrlssrls', '*srlssrlssssslsssssslsl'), ('*sssrsrlssssrls', '*srlssssrlslsss'), ('*sslsssslssrlrslssssrslrl', '*rlrslssssrslrlssrssssrss'), ('*lslsslssrlrslssssls', '*srssssrslrlssrssrsr'), ('*sssrssrslr', '*lrslsslsss'), ('*lslrsrlssslr', '*lrsssrlslrsr'), ('*ssssrlrlsls', '*srsrlrlssss'), ('*srlrlsrlssrlrlslssslrlrl', '*rlrlrsssrsrlrlssrlsrlrls'), ('*srlsrlssrlss', '*ssrlssrlsrls')]
start = [(0,1,'n'), (0,8,'w'), (1,10,'e'),
         (2,0,'w'), (3,1,'n'), (3,6,'e'),
         (3,11,'w'), (7,13,'s'), (9,0,'w'),
         (12,1,'e')]
offset = [(1,0),(2,1),(0,0),
          (0,3),(1,2),(0,0),
          (0,1),(0,2),(5,11),
          (0,0)]

def draw_pieces(pieces):
    out = ''
    # set up the frame
    for i in xrange(0, 16):
        draw.wall(Direction.NORTH, Direction.NORTH, ( i,  0))
        draw.wall(Direction.NORTH, Direction.EAST,  (15,  i))
        draw.wall(Direction.NORTH, Direction.SOUTH, ( i, 15))
        draw.wall(Direction.NORTH, Direction.WEST,  ( 0,  i))
    # draw the caterpillars
    for (pp,_),(py,px,d),(oy,ox) in zip(pieces, start, offset):
        x,y = (px+ox)*10, (py+oy)*10
        x,y = x+15, y+15
        out += "<g transform=\"translate(%d,%d)\">" % (x,y)
        out += draw.draw_word_pat(' ', pp[1:]+'s|', draw.Direction.fromchar(d),
                                  px+ox, py+oy)
        out += "</g>\n"
    # make a frame
    out += """
    <path d="M0,0 L180,0 L180,180 L0,180 Z M10,10 L10,170 L170,170 L170,10 Z" fill="none" stroke="%s" stroke-width=".5" />
    """ % ("#00f" if draw.PONOKO else "black")
    print draw.SVG_TMPL % out

if __name__ == '__main__':
    draw_pieces(pieces)

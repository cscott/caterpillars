#!/usr/bin/python
"""Simple version of drawing, no alphabetic step."""
import draw
import random
random.seed(4242)

# from output of check.py
pieces = [('*rssssrsrlssslslr', '*lrsrsssrlslssssl'), ('*rsrssssssrsssssrlssrls', '*srlssrlssssslsssssslsl'), ('*sssrsrlssssrls', '*srlssssrlslsss'), ('*sslsssslssrlrslssssrslrl', '*rlrslssssrslrlssrssssrss'), ('*lslsslssrlrslssssls', '*srssssrslrlssrssrsr'), ('*sssrssrslr', '*lrslsslsss'), ('*lslrsrlssslr', '*lrsssrlslrsr'), ('*ssssrlrlsls', '*srsrlrlssss'), ('*srlrlsrlssrlrlslssslrlrl', '*rlrlrsssrsrlrlssrlsrlrls'), ('*srlsrlssrlss', '*ssrlssrlsrls')]

def draw_pieces(pieces):
    out = ''
    x,y=40,10
    random.shuffle(pieces)
    for p1,p2 in pieces:
        pp = random.choice([p1,p2]) # don't betray orientation
        out += "<g transform=\"translate(%d,%d)\">" % (x,y)
        out += draw.draw_word_pat(' ', pp[1:]+'s|')
        out += "</g>\n"
        x += 100
        if x > 1000:
            x = 40
            y += 200
    # make a frame
    out += """
    <path d="M0,0 L180,0 L180,180 L0,180 Z M10,10 L10,170 L170,170 L170,10 Z" fill="#7f8" stroke="black" stroke-width=".5" />
    """
    print draw.SVG_TMPL % out

if __name__ == '__main__':
    draw_pieces(pieces)

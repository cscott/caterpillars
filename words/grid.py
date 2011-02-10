#!/usr/bin/python
import random
random.seed(42)

# 'ASSEMBLED3' image with ABDOMEN/CHI/GYVE/LUTZ/MUJIK/MUST/QUIPS/REWAX/TUFTY
# word set.  Lowercase here indicates the position of eggs.
ASSEMBLED="""
Aa..BBBBBdDD....
A.CC.CCCBBBDDDD.
A..C.C.CC.B...D.
A.EC.C..c.B.fFDD
A.EC.C.D..BB.FFD
AAECCC.DD.FBb.FD
.AEEEEEEDDF...FD
.AAA...E.DFFFFFD
GGGAEEEE.DD....D
G.gAE.HHHHDDDDDD
G.AAE.H..HHHHIII
G.A.e.H.iI..h..I
GG.H.HH..II..III
.GGHHH..GGI.II..
..GGGGG..GI.I...
......GGGGIII...
""".strip()

ANSWER='ANSWERTWO'
result=''
for c in ASSEMBLED:
    if c.islower():
        result+=ANSWER[0]
        ANSWER=ANSWER[1:]
    elif c=='\n':
        result+=c
    else:
        result+=chr(ord('A')+random.randrange(0, 26))
print result

#!/usr/bin/python
import random
random.seed(43)

# 'ASSEMBLED3' image with ABDOMEN/CHI/GYVE/LUTZ/MUJIK/MUST/QUIPS/REWAX/TUFTY
# word set.  Lowercase here indicates the position of eggs.
ASSEMBLED1="""
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

# 'ASSEMBLED3' image with AWHILE/EGG/SANDS/CUP/EVER/JUDY/BOOK/TRUE/FROM
# word set.  Lowercase here indicates the position of eggs.
ASSEMBLED2="""
AA..bBBBBdDD....
A.cC.CCCBBBDDDD.
A..C.C.CC.B...D.
A.EC.C..C.B.fFDD
A.EC.C.D..BB.FFD
AAECCC.DD.FBB.FD
.AEEEEEEDDF...FD
.AAA...E.DFFFFFD
GGGAEEEE.DD....D
G.GAE.HHHHDDDDDD
G.AAE.H..HHHHIII
G.a.e.H.iI..H..I
GG.h.HH..II..III
.GGHHH..gGI.II..
..GGGGG..GI.I...
......GGGGIII...
""".strip()

ASSEMBLED=ASSEMBLED2

ANSWER='ANSWERTWO'
result=[]
row=''
for c in ASSEMBLED:
    if c.islower():
        row+=ANSWER[0]
        ANSWER=ANSWER[1:]
    elif c=='\n':
        result.append(row)
        row=''
    else:
        row+=chr(ord('A')+random.randrange(0, 26))
result.append(row)
print '\n'.join(result)

# now print the columns separately
print
for i in xrange(len(result[0])):
    print "Column", i
    for r in result:
        print r[i]
    print

#!/usr/bin/python
from __future__ import with_statement
import random
import re
from contextlib import contextmanager
random.seed(42)

WORDFILE='/usr/share/dict/american-english-large'
WORDFILE='/usr/share/dict/american-english'

BAD_WORDS=['puzo','elsa']

def letter_pattern(word):
    m = {}
    word = word.lower()
    for c in word:
        if c not in m:
            m[c] = len(m)
    return ''.join(chr(ord('A')+m[c]) for c in word)

DICT={}
def add_word(word):
    global DICT
    pat = letter_pattern(word)
    if pat not in DICT: DICT[pat]=[]
    DICT[pat].append(word.lower())

def read_dict():
    with open(WORDFILE) as f:
        while True:
            word = f.readline()
            if not word: break
            word = word.strip()
            if not word: continue
            if word[0].isupper(): continue
            word = word.lower()
            if "'" in word: continue
            if re.match('^[A-Z]+$', word, re.IGNORECASE) is None: continue
            if word.lower() in BAD_WORDS: continue
            add_word(word)

read_dict()

@contextmanager
def add_mapping(word, possibility, assignment):
    if len(word)==0:
        yield True # success!
    else:
        letter_from, word = word[0], word[1:]
        letter_to, possibility = possibility[0], possibility[1:]
        assert letter_from.isupper() and letter_to.islower()
        present = letter_from in assignment
        if present and assignment[letter_from] != letter_to:
            yield False # oops, already mapped letter_from
        elif not present and letter_to in assignment:
            yield False # already mapped something to letter_to
        else:
            assignment[letter_from] = letter_to
            assignment[letter_to] = letter_from
            with add_mapping(word, possibility, assignment) as success:
                yield success
            if not present:
                del assignment[letter_from]
                del assignment[letter_to]

# should map one letter in assignment at a time, and avoid re-checking
# idential partial assignments that have failed
def find_assignment(input, assignment):
    if len(input)==0: return dict(assignment) # success!
    word, input = input[0], input[1:]
    # partial mapping
    matcher=re.compile(''.join(('.' if c not in assignment else assignment[c])
                               for c in word), re.IGNORECASE)
    for possibility in DICT[letter_pattern(word)]:
        # quick check for consistency with assignment.
        if matcher.match(possibility) is None: continue
        # add mapping, recurse
        with add_mapping(word, possibility, assignment) as success:
            if success:
                # recurse!
                m = find_assignment(input, assignment)
                if m is not None:
                    return m # success!
    # no, we couldn't make this word
    return None

#input=[#"BHECH",
#    "BHEQP",
#    "BAL", "EHGF", "HEKL", "CJEHK", "DIMF", "XYZIAN",
#    "KOHRS",
#    "DITPUVB", #"DI.G.B"
#    #"BKPQR"
#    #"BNUVMW"
#    ]
input=[
    "IFAPN",
    "DKQC",
    "QOIPL",
    #"CAKDIDGIK",
    "FDPQI",
    "LHH",
    ##"BDCKEIB",
    "BKPNE",
    "PAKMJ",
]
input.sort(key=lambda x: len(DICT[letter_pattern(x)]))

# shuffle dictionary so we don't just get first solution in alpha order
if True:
    for lst in DICT.values():
        random.shuffle(lst)

assignment = find_assignment(input, {})
if assignment is None:
    print "No solutions"
else:
    for w in input:
        print w, ''.join(assignment.get(x, '?') for x in w)

#print input, [len(DICT[letter_pattern(x)]) for x in input]
#print DICT[letter_pattern("BHECH")]

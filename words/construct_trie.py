#!/usr/bin/python
from __future__ import with_statement
import os
import sys

#WORDFILE='enable1.txt' # scrabble dictionary
#WORDFILE='looking-words' # all words in Looking Glass, being generous
#WORDFILE='looking-words-2' # "Looking glass numbered" words
#WORDFILE='/usr/share/dict/american-english' # big dict
#WORDFILE='big-dict' # bigger dict
#WORDFILE='answer-words'
WORDFILE=sys.argv[2]
NUMBER='NUMBER'
GOAL='GOAL'
MAXLEN='MAXLEN'
MINLEN='MINLEN'

BAD_WORDS=set(['imbar','gan','peh','meane','verra','caz','bez','idyls','mut'])

tries = {}
with open(WORDFILE) as f:
    while True:
        word = f.readline()
        if not word: break
        word = word.strip().lower()
        if not word: continue
        if "'" in word: continue
        if word in BAD_WORDS: continue
        word_len = len(word)
        start = tries
        start[MAXLEN] = max(word_len, start.get(MAXLEN, 0))
        start[MINLEN] = min(word_len, start.get(MINLEN, 7))
        for letter in word:
            start = start.setdefault(letter, {})
            word_len -= 1
            start[MAXLEN] = max(word_len, start.get(MAXLEN, 0))
            start[MINLEN] = min(word_len, start.get(MINLEN, 7))
        assert word_len == 0
        start[GOAL] = True

# breadth-first search of trie; assign numbers
LETTERS = [(lnum, chr(ord('a')+lnum)) for lnum in xrange(26)]
def number(s, lookup, first_goal):
    if NUMBER in s: return s[NUMBER]
    count = len(lookup)
    if s[MINLEN] == 0 and s[MAXLEN] == 0: # this is a terminal goal state
        if len(first_goal) == 0:
            first_goal[NUMBER] = count
        else:
            s[NUMBER] = first_goal[NUMBER] # canonical goal state
            return s[NUMBER]
    s[NUMBER] = count
    # compute the letter mask.
    mask = sum(1<<lnum for (lnum,l) in LETTERS if l in s)
    assert (GOAL in s) == (s[MINLEN] == 0)
    # add min len and max len, limited to 7
    min_len = min(s[MINLEN], 7)
    max_len = min(s[MAXLEN], 7)
    mask += (min_len << 26) + (max_len << 29)
    # add the letter mask to the lookup table
    lookup.append(mask)
    # now add the indices of the 'next' pointers, recursing as necessary
    for (lnum,l) in LETTERS:
        if l in s:
            lookup.append(None) # reserve space
    # now recurse
    count = count + 1
    for (lnum,l) in LETTERS:
        if l in s:
            lookup[count] = number(s[l], lookup, first_goal)
            count = count + 1
    # return the index of this entry
    return s[NUMBER]

lookup=[]
first_goal = {}
number(tries, lookup, first_goal)
    
print "#include <stdint.h>"
print "#define MAX_WORD_LEN", tries[MAXLEN]
print "#define MIN_WORD_LEN", tries[MINLEN]
print "uint32_t "+sys.argv[1]+"[] = {"
for i in lookup: print str(i)+"UL,"
print "};"

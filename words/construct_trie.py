#!/usr/bin/python
from __future__ import with_statement
import os

WORDFILE='enable1.txt'
NUMBER='NUMBER'
GOAL='GOAL'

tries = {}
max_word_len = 0
with open(WORDFILE) as f:
    while True:
        word = f.readline()
        if not word: break
        word = word.strip().lower()
        if not word: continue
        if "'" in word: continue
        max_word_len = max(max_word_len, len(word))
        start = tries
        for letter in word:
            start = start.setdefault(letter, {})
        start[GOAL] = True

# breadth-first search of trie; assign numbers
LETTERS = [(lnum, chr(ord('a')+lnum)) for lnum in xrange(26)]
def number(s, lookup, first_goal):
    if NUMBER in s: return s[NUMBER]
    count = len(lookup)
    if GOAL in s and len(s) == 1: # this is a terminal goal state
        if len(first_goal) == 0:
            first_goal[NUMBER] = count
        else:
            s[NUMBER] = first_goal[NUMBER] # canonical goal state
            return s[NUMBER]
    s[NUMBER] = count
    # compute the letter mask.
    mask = sum(1<<lnum for (lnum,l) in LETTERS if l in s)
    if GOAL in s: mask += 1 << 26 # special 'is_goal' flag
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
print "#define MAX_WORD_LEN", max_word_len
print "uint32_t trie_data[] = {"
for i in lookup: print str(i)+","
print "};"

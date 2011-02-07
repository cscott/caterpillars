/** Main search routine. */
#include <assert.h>
#include <stdio.h>

#include "state.h"
#include "trie.h"

shape_t shape_parse(char *shape_str, int len) {
    shape_t shape = 0;
    assert (len > 0);
    while (true) {
	switch (*shape_str) {
	case 's':
	    shape += 0; break;
	case 'r':
	    shape += 1; break;
	case 'l':
	    shape += 2; break;
	default:
	    assert(false);
	}
	shape_str++; len--;
	if (len == 0) return shape;
	shape = (3 * shape) + 3;
    }
}


/* state is: (188 bytes)
current letter-to-shape mapping. (52 bytes)
for each of 9*2 possible pieces: (90 bytes)
   current position in trie (uint32)
   current position in piece(uint8)
set of mapped shapes (for efficiency) (46 bytes) (not necessary to hash)
  hash complete state & keep it unique

shape = 16 bit integer: 3 bit length, 6 pairs of bits for twists.
 alternatively use trie index, as computed below = max 362 = 16 bits still.

do one is:
  for each piece:
    if not done:
      for each possible next shape: <- min, max
        for each possible next letter in trie:
           if shape already present in mapping:
	     if map[letter] != shape: skip
           add to letter-to-shape mapping (if not already present)
           update piece's position in trie
           update piece's position in piece
           if validity_check:
             add to heap of states

validity_check is:
  done = 0
  for each piece:
    if at end of piece:
       are we at goal state in trie?
          yes: done++, next piece
          no: invalid word, return INVALID
    look at possible next letters
    look at possible next shapes
    verify that 'possible letters' union 'map.get(shapes, set(unused letters))'
     is not empty
    ie, either some possible next shape currently maps to a possible next letter
        or some possible next shape is unmapped, and one of the unmapped letters
        is a possible next letter.
    // XXX would be nice to verify a length constraint, too.



shape-to-letter mapping is complete trinary tree, stored in flat array?
node[0] = 0
node[1] = 1
node[2] = 2
node[0.0] = 3
node[0.1] = 4
node[0.2] = 5
node[1.0] = 6
node[1.1] = 7
node[1.2] = 8
node[2.0] = 9
node[2.1] = 10
node[2.2] = 11
node[0.0.0] = 12
node[0.0.1] = 13
node[0.0.2] = 14
node(x).child(y) = (3*x) + y + 3
num_nodes_on_level(x) = 3^(x+1) (3, 9, 27, 81, 243, ...)
num_nodes_for_level(x) = (3^(x+2) - 3)/2  (3, 12, 39, 120, 363)
level 0 encodes all words of length 1
level 1 encodes all words of length 2
all sequences up to length 4 in 120 byte array;
all sequences up to length 5 in 363 byte array

so, <=5-move sequences in 363 byte array; element of array is mapped letter
or 46-byte index (1 bit per entry) for 'is this piece used'

alternatively: 26*(10 bits) for letter-to-piece mapping (52 bytes)
but it's ~26 times slower to look up the piece corresponding to a given letter
*/


int main(int argc, char **argv) {
}

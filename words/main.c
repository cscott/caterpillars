/** Main search routine. */
#include <stdio.h>

#include "trie.h"

/* state is:
current shape-to-letter mapping.  <- keep this unique, index by it?
for each of 9*2 possible pieces:
   current position in trie
   current position in piece
set of unmapped letters (for efficiency)

do one is:
  for each piece:
    if not done:
      for each possible next shape: <- min, max
        for each possible next letter in trie:
           if shape already present in mapping and map[shape] != letter: skip
           add to shape-to-letter mapping (if not already present)
           update piece's position in trie
           update piece's position in piece
           if validity_check:
             add to set of states

validity_check is:
  for each piece:
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
node[0.0] = 1
node[0.1] = 2
node[0.2] = 3
node[0.0.0] = 4
node[0.0.1] = 5
node[0.0.2] = 6
node[0.1.0] = 7
node[0.1.1] = 8
node[0.1.2] = 9
node(x).child(y) = (3*x) + y + 1
num_nodes_on_level(x) = 3^x (1, 3, 9, 27, 81, ...)
num_nodes_for_level(x) = (3^(x+1) - 1)/2  (1, 4, 13, 40, 121, 364)

so, sequences up to length 5, in 121 byte array; element of array is mapping.
*/


int main(int argc, char **argv) {
}

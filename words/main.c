/** Main search routine. */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "state.h"
#include "heap.h"
#include "trie.h"

/* state is: (188 bytes)
current letter-to-shape mapping. (52 bytes)
for each of 9*2 possible pieces: (90 bytes)
   current position in trie (uint32)
   current position in piece(uint8)
set of mapped shapes (for efficiency) (46 bytes) (not necessary to hash)
  hash complete state & keep it unique

shape =  trie index, as computed below = max 362 = 16 bits still.
*/

#define MIN_SEQ_LEN 3
#define MAX_SEQ_LEN 5

#define MAX_PIECE_LEN 30 /* larger than largest piece */

char *pieces[NUM_PIECES][NUM_VARIANTS] = {
    {"lsssslrslsrssrl*", "rlsslsrslrssssr*"},
    {"sssrlsrsslrl*", "rlrsslsrlsss*"},
    {"rssslslsssrsrlr*", "lrlslsssrsrsssl*"},
    {"srlssrslrsssssrssssrlrslrlr*", "lrlrslrlsssslssssslrslssrls*"},
    {"sslssssrsrsslss*", "ssrsslslssssrss*"},
    {"rlrssrsssrs*", "slssslsslrl*"},
    {"lslssslrlrlsssrlsslsl*", "rsrssrlsssrlrlrsssrsr*"},
    {"lssrlsslssrlrsr*", "lslrlssrssrlssr*"},
    {"srsrslrlsrsrsslrl*", "rlrsslslsrlrslsls*"},
};

int piece_length[NUM_PIECES]; // variants all have same length
bool can_make[MAX_PIECE_LEN];

static void fill_can_make(int i) {
    int j;
    if (i >= MAX_PIECE_LEN) return; // exceeds table boundary
    if (can_make[i]) return; // already done
    can_make[i] = true;
    for (j=MIN_SEQ_LEN; j<=MAX_SEQ_LEN; j++)
	fill_can_make(i+j);
}

/** Fill in piece length and can_make tables. */
void piece_init(void) {
    int i;
    for (i=0; i<NUM_PIECES; i++) {
	piece_length[i] = strlen(pieces[i][0]); // variants all have same len
	assert(piece_length[i] < MAX_PIECE_LEN);
    }

    for (i=0; i<MAX_PIECE_LEN; i++)
	can_make[i] = false;
    fill_can_make(0);

#if 0 /* debugging */
    for (i=0; i<NUM_PIECES; i++)
	printf("Length of %d: %d\n", i, piece_length[i]);
    for (i=0; i<MAX_PIECE_LEN; i++)
	printf("Can make %d: %d\n", i, can_make[i]);
#endif
}

/*
validity_check is:
  done = 0
  for each piece:
    if at end of piece:
       are we at goal state in trie?
          yes: done++, next piece
          no: invalid word, return INVALID
    min_possible_letters = round up: (len(piece)-piece_pos)/MAX_SEQ_LEN
    max_possible_letters = round up: (len(piece)-piece_pos)/MIN_SEQ_LEN
    if min_possible_letters > trie.max_len or
       max_possible_letters < trie.min_len: this piece is INVALID
    look at possible next letters
    look at possible next shapes
    verify that 'possible letters' union 'map.get(shapes, set(unused letters))'
     is not empty
    ie, either some possible next shape currently maps to a possible next letter
        or some possible next shape is unmapped, and one of the unmapped letters
        is a possible next letter.
    // XXX would be nice to verify a length constraint, too.
    */
bool validate(state_t *state) {
    int done = 0;
    //XXX
    return true;
}

/*
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
*/
void extend_piece_by(heap_t *heap, state_t *state, struct trie *trie,
		     shape_t shape, int piece, int var, int len) {
    uint32_t mask;
    int i, j;
    state_t *ns;
    bool shape_mapped = state_is_shape_mapped(state, shape);
    /* Are we going to be able to complete this piece? */
    if (!can_make[piece_length[piece] - (state->piece_pos[piece] + len)])
	return;
    /* for each possible next letter in trie: */
    for (i=0, j=-1, mask=1; i<26; i++, mask<<=1) {
	if ((trie->letter_mask.mask & mask) == 0) continue;
	j++;
	// is this shape or letter already spoken for?
	if (shape_mapped) {
	    if (state->letter_to_shape[i] != shape) continue;
	} else {
	    if (state_is_letter_mapped(state, i+'A')) continue;
	}
	// ok, new state!
	ns = state_add_mapping(state, i+'A', shape);
	// sync piece/var
	ns->current_piece = piece;
	ns->current_var = var;
	// update piece/trie positions.
	ns->trie_pos[piece] = trie->next[j];
	ns->piece_pos[piece] += len;
	// check and add new state
	if (validate(ns))
	    heap_push(heap, ns);
	else
	    state_free(ns);
    }
}

void extend_piece(heap_t *heap, state_t *state, int piece, int var) {
    uint32_t trie_pos = state->trie_pos[piece];
    struct trie *trie;
    shape_t shape;
    int pi, i;
    /* Is this a dead piece? */
    if (trie_pos == TRIE_NO_STATE)
	return;
    trie = trie_for_index(trie_pos);
    /* Is this an end state in the piece? */
    pi = state->piece_pos[piece];
    if (pieces[piece][var][pi] == '\0' && trie->letter_mask.min_len == 0) {
	if (piece+1 >= NUM_PIECES) {
	    char buf[80];
	    state_snprint(buf, sizeof(buf), state);
	    printf("SOLUTION FOUND!\n%s\n", buf);
	} else {
	    /* do variants of next piece */
	    for (i=0; i<NUM_VARIANTS; i++)
		extend_piece(heap, state, piece+1, i);
	}
	return;
    }
    /* ok, for each possible next shape: */
    for (i=MIN_SEQ_LEN; i <= MAX_SEQ_LEN && (pi+i) <= piece_length[piece]; i++){
	/* special case final '*' */
	if (pieces[piece][var][pi+i-1] == '*') {
	    shape = shape_parse(&pieces[piece][var][pi], i-1);
	    // three different possible endings
	    shape = (3*shape) + 3;
	    extend_piece_by(heap, state, trie, shape+0, piece,var, i/*length*/);
	    extend_piece_by(heap, state, trie, shape+1, piece,var, i/*length*/);
	    extend_piece_by(heap, state, trie, shape+2, piece,var, i/*length*/);
	} else {
	    shape = shape_parse(&pieces[piece][var][pi], i);
	    extend_piece_by(heap, state, trie, shape, piece,var, i/*length*/);
	}
    }
}

// rather than extend all pieces, just extend the 'current' piece,
// or if that's done, extend the two options for the 'next' piece.
// (or extend the two options for the first piece, if a new state)
void extend_state(heap_t *heap, state_t *state) {
    int piece, var;
    piece = state->current_piece;
    var = state->current_var;
    extend_piece(heap, state, piece, var);
}


/*
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


void find_solution(void) {
    int best_score = 100;
    int i;
    heap_t *heap = heap_new();
    for (i=0; i<NUM_VARIANTS; i++) {
	heap_push(heap, state_new(0, i));
    }
    while (!heap_is_empty(heap)) {
	state_t *state = heap_pop(heap);
#if 1
	if (state_score(state) < best_score) {
	    best_score = state_score(state);
	    printf("Looking at piece %d var %d pos %d, score %d\n",
		   state->current_piece, state->current_var,
		   state->piece_pos[state->current_piece],
		   state_score(state));
	}
#endif
	extend_state(heap, state);
	state_free(state);
    }
    heap_free(heap);
}

int main(int argc, char **argv) {
#if 0
    char *samples[] = { "s", "r", "l", "ss", "sr", "rls", "rl", "rll", NULL };
    int i;
    for (i=0; samples[i] != NULL; i++)
	printf("Shape %s: %d\n", samples[i],
	       (int)shape_parse(samples[i], strlen(samples[i])));
    trie_print_all_words();
    printf("scott: %d\n", trie_is_word("scott"));
    printf("ship: %d\n", trie_is_word("ship"));
    printf("a: %d\n", trie_is_word("a"));
    printf("aa: %d\n", trie_is_word("aa"));
#endif
    piece_init();
    find_solution();
}

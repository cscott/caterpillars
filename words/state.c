#include <assert.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

#include "state.h"

state_t *state_new(void) {
    int i, j;
    state_t *s = malloc(sizeof(*s));
    for (i=0; i<9; i++) {
	for (j=0; j<2; j++) {
	    s->trie_pos[i][j] = 0; // at start of word
	    s->piece_pos[i][j] = 0; // at start of piece
	}
    }
    for (i=0; i<26; i++)
	s->letter_to_shape[i] = NO_SHAPE;
    for (i=0; i<sizeof(s->shape_mapped); i++)
	s->shape_mapped[i] = 0;
    return s;
}
void state_free(state_t *s) {
    free(s);
}

uint32_t state_hash(state_t *s) {
    uint32_t result = 0;
    uint32_t *u = (uint32_t *)s;
    for (u=(uint32_t*)s; u < (uint32_t*)s->shape_mapped; u++)
	result = ((result<<1) | (result>>31)) ^ (*u);
    return result;
}

bool state_is_shape_mapped(state_t *state, shape_t shape) {
    int i = (shape/16), j = (shape%16);
    return (state->shape_mapped[i] & (1<<j));
}
bool state_is_letter_mapped(state_t *state, char letter) {
    assert (letter >= 'A' && letter <= 'Z');
    return (state->letter_to_shape[letter-'A']) != NO_SHAPE;
}

/** For now, score state based on number of letters mapped, so that we get
 *  the solution with the fewest different shapes/letters first. */
int state_score(state_t *state) {
    int i, score = 0;
    for (i=0; i<26; i++)
	if (state->letter_to_shape[i] != NO_SHAPE)
	    score++;
    return score;
}

state_t *state_add_mapping(state_t *state, char letter, shape_t shape) {
    state_t *ns;
    int i = (shape/16), j = (shape%16);
    assert (letter >= 'A' && letter <= 'Z');
    // shallow copy
    ns = malloc(sizeof(*ns));
    memcpy(ns, state, sizeof(*ns));
    // now add mapping.
    ns->letter_to_shape[letter-'A'] = shape;
    ns->shape_mapped[i] |= (1<<j);
    // ok! (still needs piece/trie positions updated)
    return ns;
}

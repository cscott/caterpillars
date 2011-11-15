#ifndef STATE_H_INCLUDED
#define STATE_H_INCLUDED
#include <stdbool.h>
#include <stdint.h>
#include "shape.h"

#define NUM_PIECES 13
#define NUM_VARIANTS 2
#define NUM_TRIES 2

typedef struct state {
    uint16_t current_piece, current_var;
    uint32_t trie_pos[NUM_PIECES];
    uint8_t which_trie[NUM_PIECES];
    uint8_t piece_pos[NUM_PIECES];
    shape_t letter_to_shape[26];
    uint16_t shape_mapped[23];
} state_t;

state_t *state_new(int current_piece, int current_var, int current_trie);
void state_free(state_t *state);

uint32_t state_hash(state_t *state);
int state_score(state_t *state);

bool state_is_shape_mapped(state_t *state, shape_t shape);
bool state_is_letter_mapped(state_t *state, char letter);

state_t *state_add_mapping(state_t *state, char letter, shape_t shape);

int state_snprint(char *str, size_t size, state_t *state);

#endif /* STATE_H_INCLUDED */

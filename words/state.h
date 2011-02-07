#ifndef STATE_H_INCLUDED
#define STATE_H_INCLUDED
#include <stdbool.h>
#include <stdint.h>

typedef uint16_t shape_t;
#define NO_SHAPE ((shape_t) 0xFFFF)

typedef struct state {
    uint32_t trie_pos[9][2];
    uint8_t piece_pos[9][2];
    shape_t letter_to_shape[26];
    uint16_t shape_mapped[23];
} state_t;

state_t *state_new(void);
void state_free(state_t *state);

uint32_t state_hash(state_t *state);
int state_score(state_t *state);

bool state_is_shape_mapped(state_t *state, shape_t shape);
bool state_is_letter_mapped(state_t *state, char letter);

state_t *state_add_mapping(state_t *state, char letter, shape_t shape);

#endif /* STATE_H_INCLUDED */

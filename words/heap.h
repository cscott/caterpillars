#ifndef HEAP_H_INCLUDED
#define HEAP_H_INCLUDED
#include "state.h"

typedef struct heap {
    int alloced, used;
    state_t **elem;
} heap_t;

heap_t *heap_new(void);
void heap_free(heap_t *heap);
bool heap_is_empty(heap_t *heap);
state_t *heap_pop(heap_t *heap);
void heap_push(heap_t *heap, state_t *state);

#endif /* HEAP_H_INCLUDED */

#include <assert.h>
#include <stdlib.h>
#include "heap.h"

heap_t *heap_new(void) {
    int initial_size = 1024;
    heap_t *h;

    h = calloc(1, sizeof(*h));
    h->alloced = initial_size;
    h->elem = calloc(h->alloced, sizeof(*(h->elem)));
    return h;
}

void heap_free(heap_t *heap) {
    int i;
    for (i=0; i < heap->used; i++)
	if (heap->elem[i] != NULL)
	    state_free(heap->elem[i]);
    free(heap->elem);
    free(heap);
}

bool heap_is_empty(heap_t *heap) {
    return heap->used == 0;
}

/* 'heap' is a heap at all indices >= startpos, except possibly for pos.  pos
 * is the index of a leaf with a possibly out-of-order value.  Restore the
 * heap invariant. */
static void _siftdown(heap_t *heap, int startpos, int pos) {
    state_t *newitem = heap->elem[pos], *parent;
    int parentpos;
    /* Follow the path to the root, moving parents down until finding a place
     * newitem fits. */
    while (pos > startpos) {
        parentpos = (pos - 1) >> 1;
        parent = heap->elem[parentpos];
        if (state_score(newitem) < state_score(parent)) {
            heap->elem[pos] = parent;
            pos = parentpos;
            continue;
	}
        break;
    }
    heap->elem[pos] = newitem;
}

static void _siftup(heap_t *heap, int pos) {
    int endpos = heap->used, startpos = pos, childpos, rightpos;
    state_t *newitem = heap->elem[pos];
    /** Bubble up the smaller child until hitting a leaf. */
    childpos = 2*pos + 1;    /* leftmost child position */
    while (childpos < endpos) {
        // Set childpos to index of smaller child.
        rightpos = childpos + 1;
        if (rightpos < endpos &&
	    !( state_score(heap->elem[childpos]) <
	       state_score(heap->elem[rightpos])))
            childpos = rightpos;
        /* Move the smaller child up. */
        heap->elem[pos] = heap->elem[childpos];
        pos = childpos;
        childpos = 2*pos + 1;
    }
    /* The leaf at pos is empty now.  Put newitem there, and bubble it up
     * to its final resting place (by sifting its parents down). */
    heap->elem[pos] = newitem;
    _siftdown(heap, startpos, pos);
}

state_t *heap_pop(heap_t *heap) {
    // pop the first one.
    state_t *result;
    assert(!heap_is_empty(heap));
    result = heap->elem[0];
    if (heap->used > 1) {
	heap->elem[0] = heap->elem[heap->used-1];
	_siftup(heap, 0);
    }
    heap->used--;
    return result;
}

void heap_push(heap_t *heap, state_t *state) {
    if (heap->used >= heap->alloced) {
	heap->alloced *= 2;
	heap->elem = realloc(heap->elem, heap->alloced*sizeof(heap->elem[0]));
    }
    heap->elem[heap->used++] = state;
    _siftdown(heap, 0, heap->used-1);
}

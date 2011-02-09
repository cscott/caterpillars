#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "shape.h"

shape_t shape_parse(char *shape_str, int len) {
    shape_t shape = 0;
    assert (len > 0);
    goto first;

    do {
	shape = (3 * shape) + 3;
    first:
	switch (*shape_str) {
	case 's':
	    shape += 0; break;
	case 'r':
	    shape += 1; break;
	case 'l':
	    shape += 2; break;
	default:
	    assert(0);
	}
	shape_str++; len--;
    } while (len > 0);
    return shape;
}

int shape_snprint(char *str, size_t size, shape_t shape) {
    char buf[16];
    int i=sizeof(buf);
    buf[--i] = '\0';
    while (1) {
	switch (shape % 3) {
	case 0:
	    buf[--i] = 's'; break;
	case 1:
	    buf[--i] = 'r'; break;
	case 2:
	    buf[--i] = 'l'; break;
	default:
	    assert(0);
	}
	shape = (shape / 3);
	if (shape == 0) break;
	shape--;
    }
    strncpy(str, buf+i, size);
    if (size > 0) str[size - 1] = '\0'; // ensure null-termination
    return strlen(buf);
}

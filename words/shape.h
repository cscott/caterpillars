#ifndef SHAPE_H_INCLUDED
#define SHAPE_H_INCLUDED
#include <stdint.h>

typedef uint16_t shape_t;
#define NO_SHAPE ((shape_t) 0xFFFF)


shape_t shape_parse(char *shape_str, int len);
int shape_snprint(char *str, size_t size, shape_t shape);

#endif /* SHAPE_H_INCLUDED */

#define HEIGHT 16
#define WIDTH 16
#define NUM_PIECES 9
struct piece {
  int id;
  int height;
  int width;
  int num_points;
  struct { int row; int col; } points[29];
} pieces[9][8/*rotations,mirroring*/] = {
  { /* Piece #0 */
    {     /* ROTATION #0 */
      0 , /* id     */
      12, /* height */
      4 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 1, 0}, { 2, 0}, { 3, 0}, { 4, 0}, { 5, 0}, { 5, 1},
        { 6, 1}, { 7, 1}, { 7, 2}, { 7, 3}, { 8, 3}, { 9, 3}, {10, 2}, {10, 3},
        {11, 2},
      }
    },
    {     /* ROTATION #1 */
      0 , /* id     */
      4 , /* height */
      12, /* width  */
      17, /* # pts  */
      {
        { 0, 6}, { 0, 7}, { 0, 8}, { 0, 9}, { 0,10}, { 0,11}, { 1, 4}, { 1, 5},
        { 1, 6}, { 1,11}, { 2, 0}, { 2, 1}, { 2, 4}, { 3, 1}, { 3, 2}, { 3, 3},
        { 3, 4},
      }
    },
    {     /* ROTATION #2 */
      0 , /* id     */
      12, /* height */
      4 , /* width  */
      17, /* # pts  */
      {
        { 0, 1}, { 1, 0}, { 1, 1}, { 2, 0}, { 3, 0}, { 4, 0}, { 4, 1}, { 4, 2},
        { 5, 2}, { 6, 2}, { 6, 3}, { 7, 3}, { 8, 3}, { 9, 3}, {10, 3}, {11, 2},
        {11, 3},
      }
    },
    {     /* ROTATION #3 */
      0 , /* id     */
      4 , /* height */
      12, /* width  */
      17, /* # pts  */
      {
        { 0, 7}, { 0, 8}, { 0, 9}, { 0,10}, { 1, 7}, { 1,10}, { 1,11}, { 2, 0},
        { 2, 5}, { 2, 6}, { 2, 7}, { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4},
        { 3, 5},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      0 , /* id     */
      12, /* height */
      4 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 1, 0}, { 2, 0}, { 3, 0}, { 4, 0}, { 5, 0}, { 5, 1},
        { 6, 1}, { 7, 1}, { 7, 2}, { 7, 3}, { 8, 3}, { 9, 3}, {10, 2}, {10, 3},
        {11, 2},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      0 , /* id     */
      4 , /* height */
      12, /* width  */
      17, /* # pts  */
      {
        { 0, 6}, { 0, 7}, { 0, 8}, { 0, 9}, { 0,10}, { 0,11}, { 1, 4}, { 1, 5},
        { 1, 6}, { 1,11}, { 2, 0}, { 2, 1}, { 2, 4}, { 3, 1}, { 3, 2}, { 3, 3},
        { 3, 4},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      0 , /* id     */
      12, /* height */
      4 , /* width  */
      17, /* # pts  */
      {
        { 0, 1}, { 1, 0}, { 1, 1}, { 2, 0}, { 3, 0}, { 4, 0}, { 4, 1}, { 4, 2},
        { 5, 2}, { 6, 2}, { 6, 3}, { 7, 3}, { 8, 3}, { 9, 3}, {10, 3}, {11, 2},
        {11, 3},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      0 , /* id     */
      4 , /* height */
      12, /* width  */
      17, /* # pts  */
      {
        { 0, 7}, { 0, 8}, { 0, 9}, { 0,10}, { 1, 7}, { 1,10}, { 1,11}, { 2, 0},
        { 2, 5}, { 2, 6}, { 2, 7}, { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4},
        { 3, 5},
      }
    },
  },
  { /* Piece #1 */
    {     /* ROTATION #0 */
      1 , /* id     */
      6 , /* height */
      9 , /* width  */
      14, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 1, 4}, { 1, 5}, { 1, 6},
        { 2, 6}, { 3, 6}, { 4, 6}, { 4, 7}, { 5, 7}, { 5, 8},
      }
    },
    {     /* ROTATION #1 */
      1 , /* id     */
      9 , /* height */
      6 , /* width  */
      14, /* # pts  */
      {
        { 0, 5}, { 1, 5}, { 2, 5}, { 3, 5}, { 4, 4}, { 4, 5}, { 5, 4}, { 6, 1},
        { 6, 2}, { 6, 3}, { 6, 4}, { 7, 0}, { 7, 1}, { 8, 0},
      }
    },
    {     /* ROTATION #2 */
      1 , /* id     */
      6 , /* height */
      9 , /* width  */
      14, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 1, 1}, { 1, 2}, { 2, 2}, { 3, 2}, { 4, 2}, { 4, 3},
        { 4, 4}, { 5, 4}, { 5, 5}, { 5, 6}, { 5, 7}, { 5, 8},
      }
    },
    {     /* ROTATION #3 */
      1 , /* id     */
      9 , /* height */
      6 , /* width  */
      14, /* # pts  */
      {
        { 0, 5}, { 1, 4}, { 1, 5}, { 2, 1}, { 2, 2}, { 2, 3}, { 2, 4}, { 3, 1},
        { 4, 0}, { 4, 1}, { 5, 0}, { 6, 0}, { 7, 0}, { 8, 0},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      1 , /* id     */
      6 , /* height */
      9 , /* width  */
      14, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 1, 4}, { 1, 5}, { 1, 6},
        { 2, 6}, { 3, 6}, { 4, 6}, { 4, 7}, { 5, 7}, { 5, 8},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      1 , /* id     */
      9 , /* height */
      6 , /* width  */
      14, /* # pts  */
      {
        { 0, 5}, { 1, 5}, { 2, 5}, { 3, 5}, { 4, 4}, { 4, 5}, { 5, 4}, { 6, 1},
        { 6, 2}, { 6, 3}, { 6, 4}, { 7, 0}, { 7, 1}, { 8, 0},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      1 , /* id     */
      6 , /* height */
      9 , /* width  */
      14, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 1, 1}, { 1, 2}, { 2, 2}, { 3, 2}, { 4, 2}, { 4, 3},
        { 4, 4}, { 5, 4}, { 5, 5}, { 5, 6}, { 5, 7}, { 5, 8},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      1 , /* id     */
      9 , /* height */
      6 , /* width  */
      14, /* # pts  */
      {
        { 0, 5}, { 1, 4}, { 1, 5}, { 2, 1}, { 2, 2}, { 2, 3}, { 2, 4}, { 3, 1},
        { 4, 0}, { 4, 1}, { 5, 0}, { 6, 0}, { 7, 0}, { 8, 0},
      }
    },
  },
  { /* Piece #2 */
    {     /* ROTATION #0 */
      2 , /* id     */
      5 , /* height */
      7 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 3}, { 0, 4}, { 0, 5}, { 1, 1}, { 1, 3}, { 1, 5},
        { 1, 6}, { 2, 1}, { 2, 3}, { 2, 6}, { 3, 1}, { 3, 3}, { 4, 1}, { 4, 2},
        { 4, 3},
      }
    },
    {     /* ROTATION #1 */
      2 , /* id     */
      7 , /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 4}, { 1, 0}, { 1, 1}, { 1, 2}, { 1, 3}, { 1, 4}, { 2, 0}, { 3, 0},
        { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4}, { 4, 4}, { 5, 3}, { 5, 4}, { 6, 2},
        { 6, 3},
      }
    },
    {     /* ROTATION #2 */
      2 , /* id     */
      5 , /* height */
      7 , /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 1, 3}, { 1, 5}, { 2, 0}, { 2, 3}, { 2, 5},
        { 3, 0}, { 3, 1}, { 3, 3}, { 3, 5}, { 4, 1}, { 4, 2}, { 4, 3}, { 4, 5},
        { 4, 6},
      }
    },
    {     /* ROTATION #3 */
      2 , /* id     */
      7 , /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 1}, { 0, 2}, { 1, 0}, { 1, 1}, { 2, 0}, { 3, 0}, { 3, 1}, { 3, 2},
        { 3, 3}, { 3, 4}, { 4, 4}, { 5, 0}, { 5, 1}, { 5, 2}, { 5, 3}, { 5, 4},
        { 6, 0},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      2 , /* id     */
      5 , /* height */
      7 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 3}, { 0, 4}, { 0, 5}, { 1, 1}, { 1, 3}, { 1, 5},
        { 1, 6}, { 2, 1}, { 2, 3}, { 2, 6}, { 3, 1}, { 3, 3}, { 4, 1}, { 4, 2},
        { 4, 3},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      2 , /* id     */
      7 , /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 4}, { 1, 0}, { 1, 1}, { 1, 2}, { 1, 3}, { 1, 4}, { 2, 0}, { 3, 0},
        { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4}, { 4, 4}, { 5, 3}, { 5, 4}, { 6, 2},
        { 6, 3},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      2 , /* id     */
      5 , /* height */
      7 , /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 1, 3}, { 1, 5}, { 2, 0}, { 2, 3}, { 2, 5},
        { 3, 0}, { 3, 1}, { 3, 3}, { 3, 5}, { 4, 1}, { 4, 2}, { 4, 3}, { 4, 5},
        { 4, 6},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      2 , /* id     */
      7 , /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 1}, { 0, 2}, { 1, 0}, { 1, 1}, { 2, 0}, { 3, 0}, { 3, 1}, { 3, 2},
        { 3, 3}, { 3, 4}, { 4, 4}, { 5, 0}, { 5, 1}, { 5, 2}, { 5, 3}, { 5, 4},
        { 6, 0},
      }
    },
  },
  { /* Piece #3 */
    {     /* ROTATION #0 */
      3 , /* id     */
      10, /* height */
      9 , /* width  */
      29, /* # pts  */
      {
        { 0, 2}, { 0, 3}, { 0, 4}, { 1, 4}, { 1, 5}, { 1, 6}, { 1, 7}, { 2, 7},
        { 3, 7}, { 3, 8}, { 4, 0}, { 4, 8}, { 5, 0}, { 5, 1}, { 5, 8}, { 6, 1},
        { 6, 2}, { 6, 8}, { 7, 2}, { 7, 8}, { 8, 2}, { 8, 3}, { 8, 8}, { 9, 3},
        { 9, 4}, { 9, 5}, { 9, 6}, { 9, 7}, { 9, 8},
      }
    },
    {     /* ROTATION #1 */
      3 , /* id     */
      9 , /* height */
      10, /* width  */
      29, /* # pts  */
      {
        { 0, 4}, { 0, 5}, { 1, 3}, { 1, 4}, { 2, 1}, { 2, 2}, { 2, 3}, { 2, 9},
        { 3, 0}, { 3, 1}, { 3, 9}, { 4, 0}, { 4, 8}, { 4, 9}, { 5, 0}, { 5, 8},
        { 6, 0}, { 6, 8}, { 7, 0}, { 7, 6}, { 7, 7}, { 7, 8}, { 8, 0}, { 8, 1},
        { 8, 2}, { 8, 3}, { 8, 4}, { 8, 5}, { 8, 6},
      }
    },
    {     /* ROTATION #2 */
      3 , /* id     */
      10, /* height */
      9 , /* width  */
      29, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 0, 5}, { 1, 0}, { 1, 5},
        { 1, 6}, { 2, 0}, { 2, 6}, { 3, 0}, { 3, 6}, { 3, 7}, { 4, 0}, { 4, 7},
        { 4, 8}, { 5, 0}, { 5, 8}, { 6, 0}, { 6, 1}, { 7, 1}, { 8, 1}, { 8, 2},
        { 8, 3}, { 8, 4}, { 9, 4}, { 9, 5}, { 9, 6},
      }
    },
    {     /* ROTATION #3 */
      3 , /* id     */
      9 , /* height */
      10, /* width  */
      29, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 0, 6}, { 0, 7}, { 0, 8}, { 0, 9}, { 1, 1},
        { 1, 2}, { 1, 3}, { 1, 9}, { 2, 1}, { 2, 9}, { 3, 1}, { 3, 9}, { 4, 0},
        { 4, 1}, { 4, 9}, { 5, 0}, { 5, 8}, { 5, 9}, { 6, 0}, { 6, 6}, { 6, 7},
        { 6, 8}, { 7, 5}, { 7, 6}, { 8, 4}, { 8, 5},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      3 , /* id     */
      10, /* height */
      9 , /* width  */
      29, /* # pts  */
      {
        { 0, 2}, { 0, 3}, { 0, 4}, { 1, 4}, { 1, 5}, { 1, 6}, { 1, 7}, { 2, 7},
        { 3, 7}, { 3, 8}, { 4, 0}, { 4, 8}, { 5, 0}, { 5, 1}, { 5, 8}, { 6, 1},
        { 6, 2}, { 6, 8}, { 7, 2}, { 7, 8}, { 8, 2}, { 8, 3}, { 8, 8}, { 9, 3},
        { 9, 4}, { 9, 5}, { 9, 6}, { 9, 7}, { 9, 8},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      3 , /* id     */
      9 , /* height */
      10, /* width  */
      29, /* # pts  */
      {
        { 0, 4}, { 0, 5}, { 1, 3}, { 1, 4}, { 2, 1}, { 2, 2}, { 2, 3}, { 2, 9},
        { 3, 0}, { 3, 1}, { 3, 9}, { 4, 0}, { 4, 8}, { 4, 9}, { 5, 0}, { 5, 8},
        { 6, 0}, { 6, 8}, { 7, 0}, { 7, 6}, { 7, 7}, { 7, 8}, { 8, 0}, { 8, 1},
        { 8, 2}, { 8, 3}, { 8, 4}, { 8, 5}, { 8, 6},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      3 , /* id     */
      10, /* height */
      9 , /* width  */
      29, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 0, 5}, { 1, 0}, { 1, 5},
        { 1, 6}, { 2, 0}, { 2, 6}, { 3, 0}, { 3, 6}, { 3, 7}, { 4, 0}, { 4, 7},
        { 4, 8}, { 5, 0}, { 5, 8}, { 6, 0}, { 6, 1}, { 7, 1}, { 8, 1}, { 8, 2},
        { 8, 3}, { 8, 4}, { 9, 4}, { 9, 5}, { 9, 6},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      3 , /* id     */
      9 , /* height */
      10, /* width  */
      29, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 0, 6}, { 0, 7}, { 0, 8}, { 0, 9}, { 1, 1},
        { 1, 2}, { 1, 3}, { 1, 9}, { 2, 1}, { 2, 9}, { 3, 1}, { 3, 9}, { 4, 0},
        { 4, 1}, { 4, 9}, { 5, 0}, { 5, 8}, { 5, 9}, { 6, 0}, { 6, 6}, { 6, 7},
        { 6, 8}, { 7, 5}, { 7, 6}, { 8, 4}, { 8, 5},
      }
    },
  },
  { /* Piece #4 */
    {     /* ROTATION #0 */
      4 , /* id     */
      9 , /* height */
      6 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 1, 0}, { 2, 0}, { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4},
        { 3, 5}, { 4, 5}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5}, { 6, 2}, { 7, 2},
        { 8, 2},
      }
    },
    {     /* ROTATION #1 */
      4 , /* id     */
      6 , /* height */
      9 , /* width  */
      17, /* # pts  */
      {
        { 0, 5}, { 0, 6}, { 0, 7}, { 0, 8}, { 1, 5}, { 2, 0}, { 2, 1}, { 2, 2},
        { 2, 3}, { 2, 5}, { 3, 3}, { 3, 5}, { 4, 3}, { 4, 5}, { 5, 3}, { 5, 4},
        { 5, 5},
      }
    },
    {     /* ROTATION #2 */
      4 , /* id     */
      9 , /* height */
      6 , /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 1, 3}, { 2, 3}, { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 4, 0},
        { 5, 0}, { 5, 1}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5}, { 6, 5}, { 7, 5},
        { 8, 5},
      }
    },
    {     /* ROTATION #3 */
      4 , /* id     */
      6 , /* height */
      9 , /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 1, 3}, { 1, 5}, { 2, 3}, { 2, 5}, { 3, 3},
        { 3, 5}, { 3, 6}, { 3, 7}, { 3, 8}, { 4, 3}, { 5, 0}, { 5, 1}, { 5, 2},
        { 5, 3},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      4 , /* id     */
      9 , /* height */
      6 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 1, 0}, { 2, 0}, { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 4},
        { 3, 5}, { 4, 5}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5}, { 6, 2}, { 7, 2},
        { 8, 2},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      4 , /* id     */
      6 , /* height */
      9 , /* width  */
      17, /* # pts  */
      {
        { 0, 5}, { 0, 6}, { 0, 7}, { 0, 8}, { 1, 5}, { 2, 0}, { 2, 1}, { 2, 2},
        { 2, 3}, { 2, 5}, { 3, 3}, { 3, 5}, { 4, 3}, { 4, 5}, { 5, 3}, { 5, 4},
        { 5, 5},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      4 , /* id     */
      9 , /* height */
      6 , /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 1, 3}, { 2, 3}, { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 4, 0},
        { 5, 0}, { 5, 1}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5}, { 6, 5}, { 7, 5},
        { 8, 5},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      4 , /* id     */
      6 , /* height */
      9 , /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 1, 3}, { 1, 5}, { 2, 3}, { 2, 5}, { 3, 3},
        { 3, 5}, { 3, 6}, { 3, 7}, { 3, 8}, { 4, 3}, { 5, 0}, { 5, 1}, { 5, 2},
        { 5, 3},
      }
    },
  },
  { /* Piece #5 */
    {     /* ROTATION #0 */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 2}, { 0, 3}, { 1, 3}, { 1, 4}, { 2, 0}, { 2, 4}, { 3, 0}, { 3, 4},
        { 4, 0}, { 4, 1}, { 4, 2}, { 4, 3}, { 4, 4},
      }
    },
    {     /* ROTATION #1 */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 1, 0}, { 2, 0}, { 2, 4}, { 3, 0}, { 3, 3},
        { 3, 4}, { 4, 0}, { 4, 1}, { 4, 2}, { 4, 3},
      }
    },
    {     /* ROTATION #2 */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 1, 0}, { 1, 4}, { 2, 0},
        { 2, 4}, { 3, 0}, { 3, 1}, { 4, 1}, { 4, 2},
      }
    },
    {     /* ROTATION #3 */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 1, 0}, { 1, 1}, { 1, 4}, { 2, 0},
        { 2, 4}, { 3, 4}, { 4, 2}, { 4, 3}, { 4, 4},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 2}, { 0, 3}, { 1, 3}, { 1, 4}, { 2, 0}, { 2, 4}, { 3, 0}, { 3, 4},
        { 4, 0}, { 4, 1}, { 4, 2}, { 4, 3}, { 4, 4},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 1, 0}, { 2, 0}, { 2, 4}, { 3, 0}, { 3, 3},
        { 3, 4}, { 4, 0}, { 4, 1}, { 4, 2}, { 4, 3},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 1, 0}, { 1, 4}, { 2, 0},
        { 2, 4}, { 3, 0}, { 3, 1}, { 4, 1}, { 4, 2},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      5 , /* id     */
      5 , /* height */
      5 , /* width  */
      13, /* # pts  */
      {
        { 0, 1}, { 0, 2}, { 0, 3}, { 0, 4}, { 1, 0}, { 1, 1}, { 1, 4}, { 2, 0},
        { 2, 4}, { 3, 4}, { 4, 2}, { 4, 3}, { 4, 4},
      }
    },
  },
  { /* Piece #6 */
    {     /* ROTATION #0 */
      6 , /* id     */
      8 , /* height */
      10, /* width  */
      23, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 1, 0}, { 1, 2}, { 2, 0}, { 3, 0}, { 4, 0},
        { 4, 1}, { 5, 1}, { 5, 2}, { 5, 8}, { 5, 9}, { 6, 2}, { 6, 3}, { 6, 4},
        { 6, 5}, { 6, 6}, { 6, 9}, { 7, 6}, { 7, 7}, { 7, 8}, { 7, 9},
      }
    },
    {     /* ROTATION #1 */
      6 , /* id     */
      10, /* height */
      8 , /* width  */
      23, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 0, 6}, { 0, 7}, { 1, 2}, { 1, 3}, { 1, 7},
        { 2, 1}, { 2, 2}, { 2, 6}, { 2, 7}, { 3, 1}, { 4, 1}, { 5, 1}, { 6, 0},
        { 6, 1}, { 7, 0}, { 8, 0}, { 8, 2}, { 9, 0}, { 9, 1}, { 9, 2},
      }
    },
    {     /* ROTATION #2 */
      6 , /* id     */
      8 , /* height */
      10, /* width  */
      23, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 1, 0}, { 1, 3}, { 1, 4}, { 1, 5},
        { 1, 6}, { 1, 7}, { 2, 0}, { 2, 1}, { 2, 7}, { 2, 8}, { 3, 8}, { 3, 9},
        { 4, 9}, { 5, 9}, { 6, 7}, { 6, 9}, { 7, 7}, { 7, 8}, { 7, 9},
      }
    },
    {     /* ROTATION #3 */
      6 , /* id     */
      10, /* height */
      8 , /* width  */
      23, /* # pts  */
      {
        { 0, 5}, { 0, 6}, { 0, 7}, { 1, 5}, { 1, 7}, { 2, 7}, { 3, 6}, { 3, 7},
        { 4, 6}, { 5, 6}, { 6, 6}, { 7, 0}, { 7, 1}, { 7, 5}, { 7, 6}, { 8, 0},
        { 8, 4}, { 8, 5}, { 9, 0}, { 9, 1}, { 9, 2}, { 9, 3}, { 9, 4},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      6 , /* id     */
      8 , /* height */
      10, /* width  */
      23, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 1, 0}, { 1, 2}, { 2, 0}, { 3, 0}, { 4, 0},
        { 4, 1}, { 5, 1}, { 5, 2}, { 5, 8}, { 5, 9}, { 6, 2}, { 6, 3}, { 6, 4},
        { 6, 5}, { 6, 6}, { 6, 9}, { 7, 6}, { 7, 7}, { 7, 8}, { 7, 9},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      6 , /* id     */
      10, /* height */
      8 , /* width  */
      23, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 0, 6}, { 0, 7}, { 1, 2}, { 1, 3}, { 1, 7},
        { 2, 1}, { 2, 2}, { 2, 6}, { 2, 7}, { 3, 1}, { 4, 1}, { 5, 1}, { 6, 0},
        { 6, 1}, { 7, 0}, { 8, 0}, { 8, 2}, { 9, 0}, { 9, 1}, { 9, 2},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      6 , /* id     */
      8 , /* height */
      10, /* width  */
      23, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 0, 3}, { 1, 0}, { 1, 3}, { 1, 4}, { 1, 5},
        { 1, 6}, { 1, 7}, { 2, 0}, { 2, 1}, { 2, 7}, { 2, 8}, { 3, 8}, { 3, 9},
        { 4, 9}, { 5, 9}, { 6, 7}, { 6, 9}, { 7, 7}, { 7, 8}, { 7, 9},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      6 , /* id     */
      10, /* height */
      8 , /* width  */
      23, /* # pts  */
      {
        { 0, 5}, { 0, 6}, { 0, 7}, { 1, 5}, { 1, 7}, { 2, 7}, { 3, 6}, { 3, 7},
        { 4, 6}, { 5, 6}, { 6, 6}, { 7, 0}, { 7, 1}, { 7, 5}, { 7, 6}, { 8, 0},
        { 8, 4}, { 8, 5}, { 9, 0}, { 9, 1}, { 9, 2}, { 9, 3}, { 9, 4},
      }
    },
  },
  { /* Piece #7 */
    {     /* ROTATION #0 */
      7 , /* id     */
      5 , /* height */
      10, /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 0, 6}, { 1, 3}, { 1, 6}, { 1, 7}, { 1, 8},
        { 1, 9}, { 2, 3}, { 2, 9}, { 3, 0}, { 3, 2}, { 3, 3}, { 4, 0}, { 4, 1},
        { 4, 2},
      }
    },
    {     /* ROTATION #1 */
      7 , /* id     */
      10, /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 1, 0}, { 2, 0}, { 2, 1}, { 3, 1}, { 3, 2}, { 3, 3},
        { 3, 4}, { 4, 4}, { 5, 4}, { 6, 3}, { 6, 4}, { 7, 3}, { 8, 3}, { 9, 2},
        { 9, 3},
      }
    },
    {     /* ROTATION #2 */
      7 , /* id     */
      5 , /* height */
      10, /* width  */
      17, /* # pts  */
      {
        { 0, 7}, { 0, 8}, { 0, 9}, { 1, 6}, { 1, 7}, { 1, 9}, { 2, 0}, { 2, 6},
        { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 6}, { 4, 3}, { 4, 4}, { 4, 5},
        { 4, 6},
      }
    },
    {     /* ROTATION #3 */
      7 , /* id     */
      10, /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 1}, { 0, 2}, { 1, 1}, { 2, 1}, { 3, 0}, { 3, 1}, { 4, 0}, { 5, 0},
        { 6, 0}, { 6, 1}, { 6, 2}, { 6, 3}, { 7, 3}, { 7, 4}, { 8, 4}, { 9, 3},
        { 9, 4},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      7 , /* id     */
      5 , /* height */
      10, /* width  */
      17, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 0, 6}, { 1, 3}, { 1, 6}, { 1, 7}, { 1, 8},
        { 1, 9}, { 2, 3}, { 2, 9}, { 3, 0}, { 3, 2}, { 3, 3}, { 4, 0}, { 4, 1},
        { 4, 2},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      7 , /* id     */
      10, /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 1, 0}, { 2, 0}, { 2, 1}, { 3, 1}, { 3, 2}, { 3, 3},
        { 3, 4}, { 4, 4}, { 5, 4}, { 6, 3}, { 6, 4}, { 7, 3}, { 8, 3}, { 9, 2},
        { 9, 3},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      7 , /* id     */
      5 , /* height */
      10, /* width  */
      17, /* # pts  */
      {
        { 0, 7}, { 0, 8}, { 0, 9}, { 1, 6}, { 1, 7}, { 1, 9}, { 2, 0}, { 2, 6},
        { 3, 0}, { 3, 1}, { 3, 2}, { 3, 3}, { 3, 6}, { 4, 3}, { 4, 4}, { 4, 5},
        { 4, 6},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      7 , /* id     */
      10, /* height */
      5 , /* width  */
      17, /* # pts  */
      {
        { 0, 1}, { 0, 2}, { 1, 1}, { 2, 1}, { 3, 0}, { 3, 1}, { 4, 0}, { 5, 0},
        { 6, 0}, { 6, 1}, { 6, 2}, { 6, 3}, { 7, 3}, { 7, 4}, { 8, 4}, { 9, 3},
        { 9, 4},
      }
    },
  },
  { /* Piece #8 */
    {     /* ROTATION #0 */
      8 , /* id     */
      6 , /* height */
      8 , /* width  */
      19, /* # pts  */
      {
        { 0, 5}, { 0, 6}, { 0, 7}, { 1, 0}, { 1, 1}, { 1, 7}, { 2, 1}, { 2, 2},
        { 2, 5}, { 2, 6}, { 2, 7}, { 3, 2}, { 3, 4}, { 3, 5}, { 4, 2}, { 4, 4},
        { 5, 2}, { 5, 3}, { 5, 4},
      }
    },
    {     /* ROTATION #1 */
      8 , /* id     */
      8 , /* height */
      6 , /* width  */
      19, /* # pts  */
      {
        { 0, 4}, { 1, 3}, { 1, 4}, { 2, 0}, { 2, 1}, { 2, 2}, { 2, 3}, { 3, 0},
        { 4, 0}, { 4, 1}, { 4, 2}, { 5, 2}, { 5, 3}, { 5, 5}, { 6, 3}, { 6, 5},
        { 7, 3}, { 7, 4}, { 7, 5},
      }
    },
    {     /* ROTATION #2 */
      8 , /* id     */
      6 , /* height */
      8 , /* width  */
      19, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 1, 3}, { 1, 5}, { 2, 2}, { 2, 3}, { 2, 5},
        { 3, 0}, { 3, 1}, { 3, 2}, { 3, 5}, { 3, 6}, { 4, 0}, { 4, 6}, { 4, 7},
        { 5, 0}, { 5, 1}, { 5, 2},
      }
    },
    {     /* ROTATION #3 */
      8 , /* id     */
      8 , /* height */
      6 , /* width  */
      19, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 1, 0}, { 1, 2}, { 2, 0}, { 2, 2}, { 2, 3},
        { 3, 3}, { 3, 4}, { 3, 5}, { 4, 5}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5},
        { 6, 1}, { 6, 2}, { 7, 1},
      }
    },
    {     /* ROTATION #0 MIRRORED */
      8 , /* id     */
      6 , /* height */
      8 , /* width  */
      19, /* # pts  */
      {
        { 0, 5}, { 0, 6}, { 0, 7}, { 1, 0}, { 1, 1}, { 1, 7}, { 2, 1}, { 2, 2},
        { 2, 5}, { 2, 6}, { 2, 7}, { 3, 2}, { 3, 4}, { 3, 5}, { 4, 2}, { 4, 4},
        { 5, 2}, { 5, 3}, { 5, 4},
      }
    },
    {     /* ROTATION #1 MIRRORED */
      8 , /* id     */
      8 , /* height */
      6 , /* width  */
      19, /* # pts  */
      {
        { 0, 4}, { 1, 3}, { 1, 4}, { 2, 0}, { 2, 1}, { 2, 2}, { 2, 3}, { 3, 0},
        { 4, 0}, { 4, 1}, { 4, 2}, { 5, 2}, { 5, 3}, { 5, 5}, { 6, 3}, { 6, 5},
        { 7, 3}, { 7, 4}, { 7, 5},
      }
    },
    {     /* ROTATION #2 MIRRORED */
      8 , /* id     */
      6 , /* height */
      8 , /* width  */
      19, /* # pts  */
      {
        { 0, 3}, { 0, 4}, { 0, 5}, { 1, 3}, { 1, 5}, { 2, 2}, { 2, 3}, { 2, 5},
        { 3, 0}, { 3, 1}, { 3, 2}, { 3, 5}, { 3, 6}, { 4, 0}, { 4, 6}, { 4, 7},
        { 5, 0}, { 5, 1}, { 5, 2},
      }
    },
    {     /* ROTATION #3 MIRRORED */
      8 , /* id     */
      8 , /* height */
      6 , /* width  */
      19, /* # pts  */
      {
        { 0, 0}, { 0, 1}, { 0, 2}, { 1, 0}, { 1, 2}, { 2, 0}, { 2, 2}, { 2, 3},
        { 3, 3}, { 3, 4}, { 3, 5}, { 4, 5}, { 5, 2}, { 5, 3}, { 5, 4}, { 5, 5},
        { 6, 1}, { 6, 2}, { 7, 1},
      }
    },
  },
};
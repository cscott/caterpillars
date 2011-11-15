#ifdef USE_PIECE_1
# include "pieces1.h"
#endif
#ifdef USE_PIECE_2
# include "pieces2.h"
#endif
#ifdef USE_PIECE_3
# include "pieces3.h"
#endif
#ifdef USE_PIECE_5
# include "pieces5.h"
#endif
#ifdef USE_PIECE_6
# include "pieces6.h"
#endif
#ifdef USE_PIECE_7
# include "pieces7.h"
#endif
#ifdef USE_PIECE_9
# include "pieces9.h"
#endif
#ifdef USE_PIECE_10
# include "pieces10.h"
#endif
#ifdef USE_PIECE_11
# include "pieces11.h"
#endif
#ifdef USE_PIECE_12
# include "pieces12.h"
#endif
#ifdef USE_PIECE_13
# include "pieces13.h"
#endif
#ifdef USE_PIECE_14
# include "pieces14.h"
#endif
#ifdef USE_PIECE_15
# include "pieces15.h"
#endif
#ifdef USE_PIECE_16
# include "pieces16.h"
#endif
#ifdef USE_PIECE_17
# include "pieces17.h"
#endif
#ifdef USE_PIECE_18
# include "pieces18.h"
#endif

#include <stdio.h>
#include <string.h>

int board[HEIGHT][WIDTH];
int num_solutions=0;

//#define CHECK_MIRRORED
#define CHECK_ROTATED
//#define RUN_BACKWARDS

void print_solution(void) {
    int r, c;
    printf("Found a solution!\n");
    num_solutions++;
    for (r=0; r<HEIGHT; r++) {
	for (c=0; c<WIDTH; c++) {
	    printf("%c", (board[r][c]<0)?'.':('A'+board[r][c]));
	}
	printf("\n");
    }
    fflush(stdout);
}

int placeable(struct piece *p, int row, int col) {
    int i;
    for (i=0; i < p->num_points; i++) {
	int r = p->points[i].row + row;
	int c = p->points[i].col + col;
	if (board[r][c] != -1)
	    return 0; // not placeable
    }
    return 1; // ok, can place it here.
}

void write_piece(struct piece *p, int row, int col, int value) {
    int i;
    for (i=0; i < p->num_points; i++) {
	int r = p->points[i].row + row;
	int c = p->points[i].col + col;
	board[r][c] = value;
    }
}

int place_one(int piece_no) {
    int rotation, row, col;
    if (piece_no >= NUM_PIECES) {
	print_solution();
	return;
    }
#ifdef CHECK_MIRRORED
# ifdef CHECK_ROTATED
    rotation = 8;
# else
#   error Cannot check just mirrored w/o reworking the code.  Too bad.
# endif
#else /* don't check mirrored */
# ifdef CHECK_ROTATED
    rotation = 4;
# else
    rotation = 1;
# endif
#endif
    for (rotation--; rotation >=0; rotation--) {
	int h = HEIGHT - pieces[piece_no][rotation].height;
	int w = WIDTH  - pieces[piece_no][rotation].width;
	// first piece doesn't rotate (kill inherent symmetry of solutions)
	// (first piece doesn't mirror, either)
	if (piece_no==0 && rotation!=0) continue;
#ifdef RUN_BACKWARDS
	for (row=h; row >= 0; row--) {
	    for (col=w; col >= 0; col--) {
#else
	for (row=0; row <= h; row++) {
	    for (col=0; col <= w; col++) {
#endif
		if (placeable(&pieces[piece_no][rotation], row, col)) {
		    if (piece_no < 2) {
			printf("[%d] Placing piece %d (rot %d) at %d,%d\n",
			       num_solutions, piece_no, rotation, row, col);
			fflush(stdout);
		    }
		    // do
		    write_piece(&pieces[piece_no][rotation],row,col,piece_no);
		    // recurse!
		    place_one(piece_no+1);
		    // undo
		    write_piece(&pieces[piece_no][rotation],row,col, -1);
		}
	    }
	}
    }
}

int main(int argc, char **argv) {
    // "unused" is -1
    memset(board, -1, sizeof(int)*HEIGHT*WIDTH);
    // go!
    place_one(0);
    // report
    printf("Total solutions found: %d\n", num_solutions);
}

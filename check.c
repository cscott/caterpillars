//#include "pieces1.h"
#include "pieces2.h"

#include <stdio.h>
#include <string.h>

int board[HEIGHT][WIDTH];
int num_solutions=0;

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
    for (rotation=0; rotation < 4; rotation++) {
	int h = HEIGHT - pieces[piece_no][rotation].height;
	int w = WIDTH  - pieces[piece_no][rotation].width;
	for (row=0; row <= h; row++) {
	    for (col=0; col <= w; col++) {
		if (placeable(&pieces[piece_no][rotation], row, col)) {
		    if (piece_no < 3) {
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

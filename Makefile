all: check1 check2 check3

pieces1.h pieces2.h pieces3.h: check.py
	./check.py

check%: pieces%.h check.c
	gcc -O9 -DUSE_PIECE_$* check.c -o $@

clean:
	$(RM) -f check1 check2 check3 pieces1.h pieces2.h pieces3.h

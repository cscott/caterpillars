all: check13

pieces1.h pieces2.h pieces3.h pieces4.h pieces5.h pieces6.h pieces7.h pieces8.h pieces9.h pieces10.h pieces11.h pieces12.h pieces13.h: check.py
	./check.py

check%: pieces%.h check.c
	gcc -O9 -DUSE_PIECE_$* check.c -o $@

clean:
	$(RM) -f check1 check2 check3 check4 check5 check6 check7 check8 check9 check10 check11 check12 check13 pieces1.h pieces2.h pieces3.h pieces4.h pieces5.h pieces6.h pieces7.h pieces8.h pieces9.h pieces10.h pieces11.h pieces12.h pieces13.h

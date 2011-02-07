CFLAGS=-g

all: main

trie_data.h: construct_trie.py
	./construct_trie.py > $@

main: main.o trie.o trie_data.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: trie.h
trie_data.o: trie_data.h
trie.o: trie.h #board.h

clean:
	$(RM) *.o trie_data.h main

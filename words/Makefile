CFLAGS=-g

all: main

trie_data.h: construct_trie.py
	./construct_trie.py > $@

main: main.o board.o play.o search.o trie.o trie_data.o
	$(CC) $(CFLAGS) -o $@ $^

board.o: board.h trie.h
main.o: board.h search.h trie.h
play.o: play.h board.h
search.o: search.h
trie_data.o: trie_data.h
trie.o: trie.h board.h

clean:
	$(RM) *.o main

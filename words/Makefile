CFLAGS=-g

all: main

trie_data.c: construct_trie.py
	./construct_trie.py > $@

main: main.o state.o trie.o trie_data.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: trie.h state.h
trie.o: trie.h
state.o: state.h

clean:
	$(RM) *.o trie_data.c main

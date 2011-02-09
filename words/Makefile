CFLAGS=-g

all: main

trie_data.c: construct_trie.py
	./construct_trie.py > $@

main: main.o shape.o state.o heap.o trie.o trie_data.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: trie.h shape.h state.h heap.h
trie.o: trie.h
state.o: state.h shape.h
heap.o: heap.h state.h shape.h
shape.o: shape.h

clean:
	$(RM) *.o trie_data.c main

#CFLAGS=-g
CFLAGS=-O9 -DNDEBUG

BIGDICT=/usr/share/dict/american-english
#BIGDICT=big-dict

all: main

big_trie_data.c: construct_trie.py $(BIGDICT)
	./construct_trie.py big_trie_data $(BIGDICT) > $@
ans_trie_data.c: construct_trie.py answer-words
	./construct_trie.py ans_trie_data answer-words > $@

main: main.o shape.o state.o heap.o trie.o big_trie_data.o ans_trie_data.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: trie.h shape.h state.h heap.h
trie.o: trie.h
state.o: state.h shape.h
heap.o: heap.h state.h shape.h
shape.o: shape.h

clean:
	$(RM) *.o *_trie_data.c main

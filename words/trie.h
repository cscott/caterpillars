/* Trie data structure, for fast & compact word search. */
#ifndef TRIE_H_INCLUDED
#define TRIE_H_INCLUDED
#include <stdbool.h>
#include <stdint.h>

union letter_mask {
    struct {
	unsigned a:1;
	unsigned b:1;
	unsigned c:1;
	unsigned d:1;
	unsigned e:1;
	unsigned f:1;
	unsigned g:1;
	unsigned h:1;
	unsigned i:1;
	unsigned j:1;
	unsigned k:1;
	unsigned l:1;
	unsigned m:1;
	unsigned n:1;
	unsigned o:1;
	unsigned p:1;
	unsigned q:1;
	unsigned r:1;
	unsigned s:1;
	unsigned t:1;
	unsigned u:1;
	unsigned v:1;
	unsigned w:1;
	unsigned x:1;
	unsigned y:1;
	unsigned z:1;
	unsigned blank:1;
	unsigned is_goal:1;
    };
    unsigned mask;
};

struct word_mask {
    int word_len;
    union letter_mask mask[15];
};

struct board;
struct word_mask;

typedef void (*match_cb_func)(char *buf, int word_len);

void trie_match_mask(struct word_mask *word_mask, match_cb_func match_cb);

bool trie_is_word(char *word);
void trie_print_all_words(int word_len);

void trie_print_word_mask(struct word_mask *word_mask);

#endif /* TRIE_H_INCLUDED */

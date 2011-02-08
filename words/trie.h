/* Trie data structure, for fast & compact word search. */
#ifndef TRIE_H_INCLUDED
#define TRIE_H_INCLUDED
#include <stdbool.h>
#include <stdint.h>

#define TRIE_NO_STATE (~(uint32_t)0)

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
	unsigned min_len:3; // 0="goal state", 7="7 or greater"
	unsigned max_len:3; // 7="7 or greater"
    };
    uint32_t mask;
};

struct trie {
    union letter_mask letter_mask;
    uint32_t next[0];
};

#if 0
struct word_mask {
    int word_len;
    union letter_mask mask[15];
};
typedef void (*match_cb_func)(char *buf, int word_len);
void trie_match_mask(struct word_mask *word_mask, match_cb_func match_cb);
void trie_print_word_mask(struct word_mask *word_mask);
#endif


bool trie_is_word(char *word);
void trie_print_all_words();
struct trie *trie_for_index(uint32_t index);

void trie_is_goal_state(uint32_t trie_pos);


#endif /* TRIE_H_INCLUDED */

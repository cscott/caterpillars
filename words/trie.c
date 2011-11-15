/* construct search trie */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "trie.h"
#define MAX_WORD_LEN 28

static bool check_from(uint32_t *which_trie, unsigned index, char *rest) {
    struct trie *trie = (struct trie *) &which_trie[index];
    unsigned mask = which_trie[index], desired;
    char next = *rest;

    if (next == '\0')
	return (trie->letter_mask.min_len==0); /* is this goal state? */


    next = toupper(next) - 'A';
    desired = 1 << next;
    if ((mask & desired) == 0)
	return false;
    
    while (true) {
	index++;
	mask &= (mask - 1); // clear least significant set bit
	if ((mask & desired) == 0)
	    return check_from(which_trie, which_trie[index], rest+1);
    }
}

bool trie_is_word(uint32_t *which_trie, char *word) {
    return check_from(which_trie, 0, word);
}

static void print_all_words_from(uint32_t *which_trie, unsigned index,
				 char *buf, int bufidx) {
    struct trie *trie = trie_for_index(which_trie, index);
    unsigned mask = trie->letter_mask.mask, desired;
    int i, j;

    if (trie->letter_mask.min_len==0/* is goal? */) {
	buf[bufidx] = '\0';
	printf("%s\n", buf);
    }
    for (i=0, j=0; i<26; i++) {
	desired = 1 << i;
	if (mask & desired) {
	    buf[bufidx] = 'a' + i;
	    print_all_words_from(which_trie, trie->next[j++], buf, bufidx+1);
	}
    }
}
void trie_print_all_words(uint32_t *which_trie) {
    char buf[MAX_WORD_LEN+1];
    print_all_words_from(which_trie, 0, buf, 0);
}
struct trie *trie_for_index(uint32_t *which_trie, uint32_t index) {
    return (struct trie *) &which_trie[index];
}

#if 0
/** Support search. */
static void match_mask_from(uint32_t *which_trie,
			    int word_len, union letter_mask *mask,
			    unsigned index, char *buf, int bufidx,
			    match_cb_func match_cb) {
    struct trie *trie = (struct trie *) &which_trie[index];
    unsigned trie_mask = which_trie[index], desired;
    int i;
    if (trie->letter_mask.min_len==0) {
	buf[bufidx] = '\0'; // convenience
	match_cb(buf, word_len);
	return;
    }
    for (i=0, desired=1; i<26; i++, desired <<= 1) {
	if (trie_mask & desired) {
	    index++;
	    if (desired & mask->mask) {
		buf[bufidx] = 'A' + i;
		match_mask_from(word_len, mask+1, which_trie[index],
				buf, bufidx+1, match_cb);
	    }
	}
    }
}

void trie_match_mask(uint32_t *which_trie,
		     struct word_mask *word_mask, match_cb_func match_cb) {
    char buf[16];
    if (word_mask->word_len < 2 || word_mask->word_len > 15) return;
    match_mask_from(which_trie,
		    word_mask->word_len, word_mask->mask,
		    which_trie[word_mask->word_len-1], buf, 0,
		    match_cb);
}

#define ALL_LETTERS 0x3FFFFFF
void trie_print_word_mask(uint32_t *which_trie, struct word_mask *word_mask) {
    int i, j, run;
    unsigned lm;
    for (i=0; i < word_mask->word_len; i++) {
	unsigned m = word_mask->mask[i].mask;
	if ((m & ALL_LETTERS) == ALL_LETTERS)
	    printf(".");
	else {
	    printf("[");
	    for (j=0, run=0, lm=1; j < 26; j++, lm<<=1) {
		if (m & lm) {
		    if (run==0) {
			printf("%c", 'a'+j);
			run=1;
		    } else if (run==1) {
			run=2;
		    } else if (run==2) {
			printf("-");
			run=3;
		    }
		} else {
		    if (run==1) {
			run=0;
		    } else if (run==2 || run==3) {
			printf("%c", 'a'+j-1);
			run=0;
		    }
		}
	    }
	    if (run==2) printf("z");
	    printf("]");
	}
    }
}
#endif

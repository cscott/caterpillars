/* construct search trie */
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "trie.h"

extern uint32_t trie_data[];

struct trie {
    union letter_mask letter_mask;
    unsigned next[0];
};

static bool check_from(unsigned index, char *rest) {
    struct trie *trie = (struct trie *) &trie_data[index];
    unsigned mask = trie_data[index], desired;
    char next = *rest;

    if (next == '\0')
	return trie->letter_mask.is_goal;

    next = toupper(next) - 'A';
    desired = 1 << next;
    if ((mask & desired) == 0)
	return false;
    
    while (true) {
	index++;
	mask &= (mask - 1); // clear least significant set bit
	if ((mask & desired) == 0)
	    return check_from(trie_data[index], rest+1);
    }
}

bool trie_is_word(char *word) {
    int word_len = strlen(word);
    if (word_len < 2 || word_len > 15) return false;
    return check_from(trie_data[word_len-1], word);
}

static void print_all_words_from(unsigned index, char *buf, int bufidx) {
    struct trie *trie = (struct trie *) &trie_data[index];
    unsigned mask = trie_data[index], desired;
    int i;

    if (trie->letter_mask.is_goal) {
	buf[bufidx] = '\0';
	printf("%s\n", buf);
    }
    index++;
    for (i=0; i<26; i++) {
	desired = 1 << i;
	if (mask & desired) {
	    buf[bufidx] = 'a' + i;
	    print_all_words_from(trie_data[index], buf, bufidx+1);
	    index++;
	}
    }
}
void trie_print_all_words(int word_len) {
    char buf[16];
    if (word_len < 2 || word_len > 15) return;
    print_all_words_from(trie_data[word_len-1], buf, 0);
}

/** Support search. */
static void match_mask_from(int word_len, union letter_mask *mask,
			    unsigned index, char *buf, int bufidx,
			    match_cb_func match_cb) {
    struct trie *trie = (struct trie *) &trie_data[index];
    unsigned trie_mask = trie_data[index], desired;
    int i;
    if (trie->letter_mask.is_goal) {
	buf[bufidx] = '\0'; // convenience
	match_cb(buf, word_len);
	return;
    }
    for (i=0, desired=1; i<26; i++, desired <<= 1) {
	if (trie_mask & desired) {
	    index++;
	    if (desired & mask->mask) {
		buf[bufidx] = 'A' + i;
		match_mask_from(word_len, mask+1, trie_data[index],
				buf, bufidx+1, match_cb);
	    }
	}
    }
}

void trie_match_mask(struct word_mask *word_mask, match_cb_func match_cb) {
    char buf[16];
    if (word_mask->word_len < 2 || word_mask->word_len > 15) return;
    match_mask_from(word_mask->word_len, word_mask->mask,
		    trie_data[word_mask->word_len-1], buf, 0,
		    match_cb);
}

#define ALL_LETTERS 0x3FFFFFF
void trie_print_word_mask(struct word_mask *word_mask) {
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

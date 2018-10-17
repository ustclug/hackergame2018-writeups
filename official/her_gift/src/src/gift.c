// This problem is aimed to tell players that they can "patch" or "hook" a program to get desired results.
// And it's designed to be much more easier to patch or hook instead of reversing important functions directly.
// Expected solution is to patch or hook (alarm() and) sleep()
// By taoky, for hackergame 2018

// IMPORTANT: gift.c and sha1.c SHOULD be compiled by [obfuscator-llvm](https://github.com/obfuscator-llvm/obfuscator)
// command: compiled_obfuscator_llvm/build/bin/clang gift.c sha1.c -mllvm -fla -mllvm -sub -mllvm -bcf
// Please note that some function names in these codes are designed to be misleading to confuse players.

#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <stdbool.h>
#include <ctype.h>
#include "sha1.h"

void init (void) __attribute__((constructor));

char *lyrics[100] = {
	"Join us now and share the software;",
	"You'll be free, hackers, you'll be free.",
	"Join us now and share the software;",
	"You'll be free, hackers, you'll be free.",
	"Hoarders can get piles of money,",
	"That is true, hackers, that is true.",
	"But they cannot help their neighbors;",
	"That's not good, hackers, that's not good.",
	"When we have enough free software",
	"At our call, hackers, at our call,",
	"We'll kick out those dirty licenses",
	"Ever more, hackers, ever more.",
	"Join us now and share the software;",
	"You'll be free, hackers, you'll be free.",
	"Join us now and share the software;",
	"You'll be free, hackers, you'll be free." 
};

void rest() {
	puts("Error code [2333]");
	puts("Running this program for too long is unhealthy for your computer.");
	puts("Please contact your administrator for details.");
	exit(0);
}

void init() {
	signal(SIGALRM, rest);
	alarm(10);
}

void print_key(unsigned int key[], int len) {
	for (int i = 0; i < len; i++) {
		printf("%02x ", key[i]);
	}
	puts("");
}

void cal(char s[], unsigned int old_key[], int i) {
	SHA1_CTX sha;
	uint8_t output[20];
	SHA1Init(&sha);
	SHA1Update(&sha, (uint8_t *)s, strlen(s));
	SHA1Final(output, &sha);
/*	
	printf("0x");
	for (int n = 0; n < 20; n++) {
		printf("%02x", output[n]);
	}
	puts("");
*/
	for (int n = 0; n < 20; n++) {
		old_key[(i + n) % 256] ^= output[n];
	}	
}

void leet(unsigned int key[], char msg[]) {
	typedef struct leetTable {
		char o;
		char c[10];
		int l;
	} leet_t;
	leet_t table[14] = {{.o = 'a', .c = "aA4", .l = 3},
		{.o = 'b', .c = "bB68", .l = 4},
		{.o = 'e', .c = "eE3", .l = 3},
		{.o = 'g', .c = "gG69", .l = 4},
		{.o = 'h', .c = "hH4", .l = 3},
		{.o = 'i', .c = "iI1", .l = 3},
		{.o = 'j', .c = "jJ7", .l = 3},
		{.o = 'l', .c = "lL1", .l = 3},
		{.o = 'o', .c = "oO09", .l = 4},
		{.o = 'p', .c = "pP9q", .l = 4},
		{.o = 's', .c = "sS5z", .l = 4},
		{.o = 't', .c = "tT17", .l = 4},
		{.o = 'y', .c = "yYj9", .l = 4},
		{.o = 'z', .c = "zZ2", .l = 3}
	}
	;
	int key_poi = 0;
	for (int i = 0; msg[i] != '\0'; i++) {
		bool changed = false;
		for (int j = 0; j < 14; j++) {
			if (msg[i] == table[j].o) {
				msg[i] = table[j].c[(key[key_poi] ^ key[(key_poi + 1) % 20]) % table[j].l];
				key_poi = (key_poi + 1) % 20;
				changed = true;
				break;
			}
		}
		if (!changed && key[key_poi] % 2 == 0 && islower(msg[i])) {
			msg[i] = toupper(msg[i]);
		}
		if (msg[i] == ' ') {
			msg[i] = '_';
		}
	}
	printf("flag{%s}\n", msg);

}
	
int main(int argc, char *argv[]) __attribute((__annotate__(("nofla nosub nobcf"))));
int main(int argc, char *argv[]) {
	if (argc == 2) {
		unsigned int key[256] = {};
		puts("Singing songs is good for mental health.");
		for (int j = 0; j < 233333; j++) {
			if (j != 0)
				puts("Mind we sing this song again?");
			for (int i = 0; lyrics[i] != NULL; i++) {
				system("echo -en '\a' > /dev/tty5");
				printf("♫\t%s\t♫\n", lyrics[i]);
				cal(lyrics[i], key, i + j * 20);
				sleep(2);
			}
		}
		printf("Key: ");
		print_key(key, 256);
		leet(key, argv[1]);
	}
	else {
		printf("Usage: %s [msg]\n", argv[0]);
	}
	return 0;
}	

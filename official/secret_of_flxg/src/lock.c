#include <stdint.h>
#include <signal.h>

#include "lock.h"

#define XOR(X, Y) X+Y - (((X)&(Y)) << 1)
#define REV(b) (((b) * 0x80200802ULL) & 0x0884422110ULL) * 0x0101010101ULL >> 32

union {
    uint64_t secret;
    uint8_t uc[8];
} u, key;

void lock(void);
void unlock(void);
static void handler(int);

#pragma GCC push_options
#pragma GCC optimize ("O0")
int check(uint64_t k){
    RANDOM_GAP;
    key.secret = k;
    signal(SIGTRAP, handler);
    raise(SIGTRAP);
    signal(SIGTRAP, SIG_IGN);
    return (u.secret != SECRET);
}
#pragma GCC pop_options

void lock(void){
    u.secret = XOR(u.secret, K * key.secret + B);
    for(int i=0;i<4;i++){
        u.uc[i] ^= REV(u.uc[7-i]);
        u.uc[7-i] ^= REV(u.uc[i]);
        u.uc[i] ^= REV(u.uc[7-i]);
    }
}

void unlock(void){
    uint64_t v = u.secret;
    v = ((v >> 1) & 0x5555555555555555) | ((v & 0x5555555555555555) << 1);
    v = ((v >> 2) & 0x3333333333333333) | ((v & 0x3333333333333333) << 2);
    v = ((v >> 4) & 0x0F0F0F0F0F0F0F0F) | ((v & 0x0F0F0F0F0F0F0F0F) << 4);
    v = ((v >> 8) & 0x00FF00FF00FF00FF) | ((v & 0x00FF00FF00FF00FF) << 8);
    v = ((v >> 16)& 0x0000FFFF0000FFFF) | ((v & 0x0000FFFF0000FFFF) << 16);
    v = ((v >> 32)                    ) | ((v)                      << 32);
    u.secret = XOR(key.secret, v);
}

static void handler(int signum) {
    if(signum == SIGTRAP){
        u.secret = SECRET;
        lock();
        unlock();
    }
}

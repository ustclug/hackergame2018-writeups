#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <string.h>
#include <unistd.h>
#include <sys/random.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/audit.h>
#include <linux/filter.h>
#include <linux/unistd.h>
#include <openssl/aes.h>

#define syscall_nr (offsetof(struct seccomp_data, nr))
#define arch_nr (offsetof(struct seccomp_data, arch))
#define REG_SYSCALL REG_RAX
#define ARCH_NR AUDIT_ARCH_X86_64

#define VALIDATE_ARCHITECTURE \
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS, arch_nr), \
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, ARCH_NR, 1, 0), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL)

#define EXAMINE_SYSCALL \
    BPF_STMT(BPF_LD+BPF_W+BPF_ABS, syscall_nr)

#define ALLOW_SYSCALL(name) \
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, __NR_ ## name, 0, 1), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW)

#define KILL_PROCESS \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL)

#define ROUNDS 10

typedef struct _T {
    uint8_t iv[16];
    uint8_t padding;
    uint8_t user[15];
    uint8_t permission;
    uint8_t hash[31];
    uint8_t garbage;
} T;

char freed;
char flag[40];
uint8_t key[16];
T data;
T io;
AES_KEY aes_key;

const unsigned char sbox[256] = {
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
};

const unsigned char mul2[256] = {
    0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1A, 0x1C, 0x1E,
    0x20, 0x22, 0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3A, 0x3C, 0x3E,
    0x40, 0x42, 0x44, 0x46, 0x48, 0x4A, 0x4C, 0x4E, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5A, 0x5C, 0x5E,
    0x60, 0x62, 0x64, 0x66, 0x68, 0x6A, 0x6C, 0x6E, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7A, 0x7C, 0x7E,
    0x80, 0x82, 0x84, 0x86, 0x88, 0x8A, 0x8C, 0x8E, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E,
    0xA0, 0xA2, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC, 0xAE, 0xB0, 0xB2, 0xB4, 0xB6, 0xB8, 0xBA, 0xBC, 0xBE,
    0xC0, 0xC2, 0xC4, 0xC6, 0xC8, 0xCA, 0xCC, 0xCE, 0xD0, 0xD2, 0xD4, 0xD6, 0xD8, 0xDA, 0xDC, 0xDE,
    0xE0, 0xE2, 0xE4, 0xE6, 0xE8, 0xEA, 0xEC, 0xEE, 0xF0, 0xF2, 0xF4, 0xF6, 0xF8, 0xFA, 0xFC, 0xFE,
    0x1B, 0x19, 0x1F, 0x1D, 0x13, 0x11, 0x17, 0x15, 0x0B, 0x09, 0x0F, 0x0D, 0x03, 0x01, 0x07, 0x05,
    0x3B, 0x39, 0x3F, 0x3D, 0x33, 0x31, 0x37, 0x35, 0x2B, 0x29, 0x2F, 0x2D, 0x23, 0x21, 0x27, 0x25,
    0x5B, 0x59, 0x5F, 0x5D, 0x53, 0x51, 0x57, 0x55, 0x4B, 0x49, 0x4F, 0x4D, 0x43, 0x41, 0x47, 0x45,
    0x7B, 0x79, 0x7F, 0x7D, 0x73, 0x71, 0x77, 0x75, 0x6B, 0x69, 0x6F, 0x6D, 0x63, 0x61, 0x67, 0x65,
    0x9B, 0x99, 0x9F, 0x9D, 0x93, 0x91, 0x97, 0x95, 0x8B, 0x89, 0x8F, 0x8D, 0x83, 0x81, 0x87, 0x85,
    0xBB, 0xB9, 0xBF, 0xBD, 0xB3, 0xB1, 0xB7, 0xB5, 0xAB, 0xA9, 0xAF, 0xAD, 0xA3, 0xA1, 0xA7, 0xA5,
    0xDB, 0xD9, 0xDF, 0xDD, 0xD3, 0xD1, 0xD7, 0xD5, 0xCB, 0xC9, 0xCF, 0xCD, 0xC3, 0xC1, 0xC7, 0xC5,
    0xFB, 0xF9, 0xFF, 0xFD, 0xF3, 0xF1, 0xF7, 0xF5, 0xEB, 0xE9, 0xEF, 0xED, 0xE3, 0xE1, 0xE7, 0xE5
};

__attribute__((constructor)) int init(){
    return mallopt(M_PERTURB, 0xAA);
}

void mix_bytes(unsigned char i0, unsigned char i1, unsigned char i2, unsigned char i3, unsigned char i4, unsigned char i5, unsigned char i6, unsigned char i7, unsigned char *output){
    register unsigned char t0, t1, t2, t3, t4, t5, t6, t7;
    register unsigned char x0, x1, x2, x3, x4, x5, x6, x7;
    register unsigned char y0, y1, y2, y3, y4, y5, y6, y7;

    t0 = i0 ^ i1;
    t1 = i1 ^ i2;
    t2 = i2 ^ i3;
    t3 = i3 ^ i4;
    t4 = i4 ^ i5;
    t5 = i5 ^ i6;
    t6 = i6 ^ i7;
    t7 = i7 ^ i0;

    x0 = t0 ^ t3;
    x1 = t1 ^ t4;
    x2 = t2 ^ t5;
    x3 = t3 ^ t6;
    x4 = t4 ^ t7;
    x5 = t5 ^ t0;
    x6 = t6 ^ t1;
    x7 = t7 ^ t2;

    y0 = t0 ^ t2 ^ i6;
    y1 = t1 ^ t3 ^ i7;
    y2 = t2 ^ t4 ^ i0;
    y3 = t3 ^ t5 ^ i1;
    y4 = t4 ^ t6 ^ i2;
    y5 = t5 ^ t7 ^ i3;
    y6 = t6 ^ t0 ^ i4;
    y7 = t7 ^ t1 ^ i5;

    x3 = (x3 & 0x80) ? (x3 << 1) ^ 0x1B : (x3 << 1);
    x0 = (x0 & 0x80) ? (x0 << 1) ^ 0x1B : (x0 << 1);

    t0 = x3 ^ y7;
    t0 = (t0 & 0x80) ? (t0 << 1) ^ 0x1B : (t0 << 1);
    t5 = x0 ^ y4;
    t5 = (t5 & 0x80) ? (t5 << 1) ^ 0x1B : (t5 << 1);

    output[0] = t0 ^ y4;
    output[5] = t5 ^ y1;

    output[1] = mul2[mul2[x4] ^ y0] ^ y5;
    output[2] = mul2[mul2[x5] ^ y1] ^ y6;
    output[3] = mul2[mul2[x6] ^ y2] ^ y7;
    output[4] = mul2[mul2[x7] ^ y3] ^ y0;
    output[6] = mul2[mul2[x1] ^ y5] ^ y2;
    output[7] = mul2[mul2[x2] ^ y6] ^ y3;
}

void perm_P(unsigned char *input, unsigned char *output){
    register unsigned char r0, r1, r2, r3, r4, r5, r6, r7, round;
    unsigned char state[64], *write = state, *read = input, *p_tmp;

    for (round = 0; round < ROUNDS; round++){
        r0 = sbox[read[ 0] ^ round];
        r1 = sbox[read[ 9]];
        r2 = sbox[read[18]];
        r3 = sbox[read[27]];
        r4 = sbox[read[36]];
        r5 = sbox[read[45]];
        r6 = sbox[read[54]];
        r7 = sbox[read[63]];

        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write);

        r0 = sbox[read[ 8] ^ round ^ 0x10];
        r1 = sbox[read[17]];
        r2 = sbox[read[26]];
        r3 = sbox[read[35]];
        r4 = sbox[read[44]];
        r5 = sbox[read[53]];
        r6 = sbox[read[62]];
        r7 = sbox[read[ 7]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+8);

        r0 = sbox[read[16] ^ round ^ 0x20];
        r1 = sbox[read[25]];
        r2 = sbox[read[34]];
        r3 = sbox[read[43]];
        r4 = sbox[read[52]];
        r5 = sbox[read[61]];
        r6 = sbox[read[ 6]];
        r7 = sbox[read[15]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+16);

        r0 = sbox[read[24] ^ round ^ 0x30];
        r1 = sbox[read[33]];
        r2 = sbox[read[42]];
        r3 = sbox[read[51]];
        r4 = sbox[read[60]];
        r5 = sbox[read[ 5]];
        r6 = sbox[read[14]];
        r7 = sbox[read[23]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+24);

        r0 = sbox[read[32] ^ round ^ 0x40];
        r1 = sbox[read[41]];
        r2 = sbox[read[50]];
        r3 = sbox[read[59]];
        r4 = sbox[read[ 4]];
        r5 = sbox[read[13]];
        r6 = sbox[read[22]];
        r7 = sbox[read[31]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+32);

        r0 = sbox[read[40] ^ round ^ 0x50];
        r1 = sbox[read[49]];
        r2 = sbox[read[58]];
        r3 = sbox[read[ 3]];
        r4 = sbox[read[12]];
        r5 = sbox[read[21]];
        r6 = sbox[read[30]];
        r7 = sbox[read[39]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+40);

        r0 = sbox[read[48] ^ round ^ 0x60];
        r1 = sbox[read[57]];
        r2 = sbox[read[ 2]];
        r3 = sbox[read[11]];
        r4 = sbox[read[20]];
        r5 = sbox[read[29]];
        r6 = sbox[read[38]];
        r7 = sbox[read[47]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+48);

        r0 = sbox[read[56] ^ round ^ 0x70];
        r1 = sbox[read[ 1]];
        r2 = sbox[read[10]];
        r3 = sbox[read[19]];
        r4 = sbox[read[28]];
        r5 = sbox[read[37]];
        r6 = sbox[read[46]];
        r7 = sbox[read[55]];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+56);

        if (round == 0)
            read = output;

        p_tmp = read;
        read = write;
        write = p_tmp;
    }
}

void perm_Q(unsigned char *input, unsigned char *output){
    register unsigned char r0, r1, r2, r3, r4, r5, r6, r7, round;
    unsigned char state[64], *write = state, *read = input, *p_tmp;

    for (round = 0; round < ROUNDS; round++){
        r0 = sbox[read[ 8] ^ 0xFF];
        r1 = sbox[read[25] ^ 0xFF];
        r2 = sbox[read[42] ^ 0xFF];
        r3 = sbox[read[59] ^ 0xFF];
        r4 = sbox[read[ 4] ^ 0xFF];
        r5 = sbox[read[21] ^ 0xFF];
        r6 = sbox[read[38] ^ 0xFF];
        r7 = sbox[read[55] ^ 0x9F ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write);

        r0 = sbox[read[16] ^ 0xFF];
        r1 = sbox[read[33] ^ 0xFF];
        r2 = sbox[read[50] ^ 0xFF];
        r3 = sbox[read[ 3] ^ 0xFF];
        r4 = sbox[read[12] ^ 0xFF];
        r5 = sbox[read[29] ^ 0xFF];
        r6 = sbox[read[46] ^ 0xFF];
        r7 = sbox[read[63] ^ 0x8F ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+8);

        r0 = sbox[read[24] ^ 0xFF];
        r1 = sbox[read[41] ^ 0xFF];
        r2 = sbox[read[58] ^ 0xFF];
        r3 = sbox[read[11] ^ 0xFF];
        r4 = sbox[read[20] ^ 0xFF];
        r5 = sbox[read[37] ^ 0xFF];
        r6 = sbox[read[54] ^ 0xFF];
        r7 = sbox[read[7] ^ 0xFF ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+16);

        r0 = sbox[read[32] ^ 0xFF];
        r1 = sbox[read[49] ^ 0xFF];
        r2 = sbox[read[ 2] ^ 0xFF];
        r3 = sbox[read[19] ^ 0xFF];
        r4 = sbox[read[28] ^ 0xFF];
        r5 = sbox[read[45] ^ 0xFF];
        r6 = sbox[read[62] ^ 0xFF];
        r7 = sbox[read[15] ^ 0xEF ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+24);

        r0 = sbox[read[40] ^ 0xFF];
        r1 = sbox[read[57] ^ 0xFF];
        r2 = sbox[read[10] ^ 0xFF];
        r3 = sbox[read[27] ^ 0xFF];
        r4 = sbox[read[36] ^ 0xFF];
        r5 = sbox[read[53] ^ 0xFF];
        r6 = sbox[read[ 6] ^ 0xFF];
        r7 = sbox[read[23] ^ 0xDF ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+32);

        r0 = sbox[read[48] ^ 0xFF];
        r1 = sbox[read[ 1] ^ 0xFF];
        r2 = sbox[read[18] ^ 0xFF];
        r3 = sbox[read[35] ^ 0xFF];
        r4 = sbox[read[44] ^ 0xFF];
        r5 = sbox[read[61] ^ 0xFF];
        r6 = sbox[read[14] ^ 0xFF];
        r7 = sbox[read[31] ^ 0xCF ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+40);

        r0 = sbox[read[56] ^ 0xFF];
        r1 = sbox[read[ 9] ^ 0xFF];
        r2 = sbox[read[26] ^ 0xFF];
        r3 = sbox[read[43] ^ 0xFF];
        r4 = sbox[read[52] ^ 0xFF];
        r5 = sbox[read[ 5] ^ 0xFF];
        r6 = sbox[read[22] ^ 0xFF];
        r7 = sbox[read[39] ^ 0xBF ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+48);

        r0 = sbox[read[ 0] ^ 0xFF];
        r1 = sbox[read[17] ^ 0xFF];
        r2 = sbox[read[34] ^ 0xFF];
        r3 = sbox[read[51] ^ 0xFF];
        r4 = sbox[read[60] ^ 0xFF];
        r5 = sbox[read[13] ^ 0xFF];
        r6 = sbox[read[30] ^ 0xFF];
        r7 = sbox[read[47] ^ 0xAF ^ round];
        mix_bytes(r0, r1, r2, r3, r4, r5, r6, r7, write+56);

        if (round == 0)
            read = output;

        p_tmp = read;
        read = write;
        write = p_tmp;
    }
}

int crypto_hash(unsigned char *out, const unsigned char *in, unsigned long long inlen){
    if (inlen >= (1ULL << 16))
        return -1;

    unsigned int msg_len = (unsigned int) inlen;
    unsigned int padded_len = ((msg_len + 9 - 1) / 64) * 64 + 64;
    unsigned char pad_block_len = padded_len-msg_len;
    unsigned char pad_block[pad_block_len];

    /* Append 1-bit */
    memset(pad_block, 0, pad_block_len);
    pad_block[0] = 0x80;

    /* Add number of blocks (note atmega128 does not have more memory so upper 40 bits are implicit '0') */
    unsigned char blocks = (padded_len >> 6);
    pad_block[pad_block_len-1] = (blocks & 0xFF);

    /* Start hashing the padded message */
    unsigned char h_state[64];
    unsigned char p_state[64];
    unsigned char q_state[64];
    unsigned char x_state[64];
    unsigned char buf[64];

    memset(h_state, 0, 64);

    h_state[62] = 0x01;

    /* Go through each block of data */
    unsigned char i, block, remaining = 0;
    unsigned int message_left_len = msg_len;
    for (block = 0; block < blocks; block++){
        if (block*64+64 < msg_len){ // one whole block
            memcpy(buf, in+64*block, 64);
            message_left_len -= 64;
        }else if (message_left_len > 0){ // part message, part padding block
            remaining = 64-message_left_len;
            memcpy(buf, in+64*block, message_left_len);
            memcpy(buf+message_left_len, pad_block, remaining);
            message_left_len = 0;
        }else{ // only padding
            memcpy(buf, pad_block+remaining, 64);
        }

        for (i = 0; i < 64; i++)
            x_state[i] = buf[i] ^ h_state[i];

        perm_P(x_state, p_state);
        perm_Q(buf, q_state);

        for (i = 0; i < 64; i++)
            h_state[i] ^= p_state[i] ^ q_state[i];
    }

    perm_P(h_state, p_state);
    for (i = 32; i < 64; i++)
        out[i-32] = h_state[i] ^ p_state[i];

    return 0;
}

void consume_lf(int d){
    if(d != '\n'){
        int c = getchar();
        while(c > 0 && c != '\n')
            c = getchar();
    }
}

void reg(uint8_t *buf){
    memset(buf, 0, 16);
    memset(&data, 0, 64);
    memset(&io, 0, 64);
    getrandom(data.iv, 16, 0);
    puts("Now, give me your name.");

    while(1){
        int c, i = 0;
        while(i < 15){
            c = getchar();
            if((c > 'a' - 1 && c < 'z' + 1) || (c > 'A' - 1 && c < 'Z' + 1) || (c > '0' - 1 && c < '9' + 1) || c == '_'){
                buf[i++] = (uint8_t) c;
                continue;
            }
            buf[i] = 0;
            break;
        }
        consume_lf(c);

        if(!strcmp((char *)buf, "root")){
            data.padding = 0xAA;
            if(freed++ > 0){
                puts("No way!\n");
                return;
            }
            puts("Not root...");
            free(buf);
            continue;
        }
        data.padding = 0;
        break;
    }
    strcpy((char *)data.user, (const char *)buf);
    if(!strcmp((char *)data.user, "root"))
        data.permission = data.padding;

    crypto_hash((uint8_t *)data.hash, (uint8_t *)&data, 32);

    AES_set_encrypt_key(key, 128, &aes_key);
    memcpy(io.iv, data.iv, 16);
    AES_cbc_encrypt(&data.padding, &io.padding, 48, &aes_key, data.iv, AES_ENCRYPT);

    puts("Here is your trial code:");
    for(int i = 0; i < 64; i++){
        printf("%02X", *((uint8_t*)&io + i));
    }
    puts("\n");
}

void trial(void){
    memset(&data, 0, 64);
    memset(&io, 0, 64);
    puts("Now, show me your power.");

    int c;
    for(int i = 0; i < 64; i++){
        c = getchar();
        if( c == '\n')
            break;
        if(c < ':')
            c -= '0';
        else
            c -= 'A' - 10;
        io.iv[i] = (c & 0xF) << 4;
        c = getchar();
        if( c == '\n')
            break;
        if(c < ':')
            c -= '0';
        else
            c -= 'A' - 10;
        io.iv[i] |= c & 0xF;
    }
    consume_lf(c);

    AES_set_decrypt_key(key, 128, &aes_key);
    memcpy(data.iv, io.iv, 16);
    AES_cbc_encrypt(&io.padding, &data.padding, 48, &aes_key, io.iv, AES_DECRYPT);

    crypto_hash((uint8_t *)io.hash, (uint8_t *)&data, 32);
    io.garbage = 0;
    data.garbage = 0;

    if(data.permission != data.padding || memcmp(io.hash, data.hash, 31)){
        puts("!!!TRIAL CODE ERROR!!!");
        exit(0);
    }else if(strcmp((char *)data.user, "root") || data.permission != 0xAA){
        puts("You are NOT powerful, yet.\n");
        return;
    }else{
        puts(flag);
        exit(0);
    }
    return;
}


static void install_syscall_filter(void)
{
    struct sock_filter filter[] = {
        /* Validate architecture. */
        VALIDATE_ARCHITECTURE,
        /* Grab the system call number. */
        EXAMINE_SYSCALL,
        /* List allowed syscalls. */
        ALLOW_SYSCALL(rt_sigreturn),
        ALLOW_SYSCALL(exit_group),
        ALLOW_SYSCALL(exit),
        ALLOW_SYSCALL(read),
        ALLOW_SYSCALL(write),
        ALLOW_SYSCALL(writev),
        ALLOW_SYSCALL(fstat),
        ALLOW_SYSCALL(getrandom),
        KILL_PROCESS,
    };
    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)){
        perror("prctl(NO_NEW_PRIVS)");
        exit(1);
    }
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)){
        perror("prctl(SECCOMP)");
        exit(1);
    }
}

int main(){
    int c;
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    getrandom(key, 16, 0);
    uint8_t *buf = calloc(1, 16);
    freed = 0;
    FILE* fp = fopen("flxg.txt", "r");
    if(fp == NULL){
        perror("Cannot open flxg.txt");
        exit(1);
    }
    fread(flag, 1, 39, fp);
    fclose(fp);

    alarm(5);
    install_syscall_filter();

    while(1){
        printf("You have two choices:\n0. Register\n1. Start Trial\n");
        c = getchar();
        if(c < 0)
            break;
        consume_lf(c);

        if(c == '0'){
            reg(buf);
            continue;
        }
        if(c == '1'){
            trial();
            continue;
        }
        puts("Time is running out. Think twice.\n");
    }

    return 0;
}

#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <algorithm>
#include <string>

#include <cctype>
#include <cstdio>

int char2idx(char c) {
    if (std::isdigit(c))
        return c - '0';
    else if (std::isupper(c))
        return c - 'A' + 10;
    else if (std::islower(c))
        return c - 'a' + 36;
    else
        return -1;
}

void printBuffer(FILE *fout, const void *buf, size_t bytes) {
    const uint8_t *ptr = (uint8_t*)buf;
    for (size_t i=0; i<bytes; i++)
        fprintf(fout, "%02hhx", ptr[i]);
}

int main() {
    std::vector<std::array<char, 32>> source[62];
    std::vector<std::array<char, 32>> sha256[62];
    char buf[64];
    std::ifstream fin("blockchain.db", std::ios::binary);

    while (fin.read(buf, sizeof(buf))) {
        char suffix = buf[31];
        int idx = char2idx(suffix);

        if (idx < 0)
            continue;

        source[idx].push_back(std::array<char, 32>());
        std::copy_n(std::begin(buf), 32,
                    std::begin(source[idx].back()));
        sha256[idx].push_back(std::array<char, 32>());
        std::copy_n(std::begin(buf) + 32, 32,
                    std::begin(sha256[idx].back()));
    }

    int maxdiff = 0;
    for (int i=0; i<62; i++) {
        int num = source[i].size();

        for (int j=0; j<num; j++) {
            for (int k=j+1; k<num; k++) {
                uint64_t *p1 = (uint64_t*)sha256[i][j].data();
                uint64_t *p2 = (uint64_t*)sha256[i][k].data();
                int diff = 256;
                diff -= __builtin_popcountll(p1[0] ^ p2[0]);
                diff -= __builtin_popcountll(p1[1] ^ p2[1]);
                diff -= __builtin_popcountll(p1[2] ^ p2[2]);
                diff -= __builtin_popcountll(p1[3] ^ p2[3]);

                if (diff >= maxdiff) {
                    maxdiff = diff;

                    std::cout << "New record! DIFF = " << (int)maxdiff << std::endl;
                    std::cout << " MSG1: ";
                    printBuffer(stdout, source[i][j].data(), 32);
                    std::cout << std::endl;
                    std::cout << "HASH1: ";
                    printBuffer(stdout, p1, 32);
                    std::cout << std::endl;

                    std::cout << " MSG2: ";
                    printBuffer(stdout, source[i][k].data(), 32);
                    std::cout << std::endl;
                    std::cout << "HASH2: ";
                    printBuffer(stdout, p2, 32);
                    std::cout << std::endl;
                }
            }
        }
    }

    return 0;
}

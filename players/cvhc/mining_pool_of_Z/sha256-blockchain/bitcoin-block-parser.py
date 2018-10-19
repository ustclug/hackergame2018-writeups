#!/usr/bin/env python3

# ./xxx.py ~/bitcoin/blocks/blk*.dat

import sys
import struct
import os
import hashlib

MAGIC_BYTES = bytes.fromhex("f9beb4d9")

def yield_blocks_from_file(path):
    with open(path, "rb") as fin:
        while True:
            magic = fin.read(4)
            if len(magic) == 0:
                break

            size = fin.read(4)
            header = fin.read(80)

            if magic != MAGIC_BYTES \
                    or len(size) != 4 \
                    or len(header) != 80:
                raise Exception("Broken file!")

            size, = struct.unpack("<I", size)
            fin.seek(size - 80, os.SEEK_CUR)

            hash_header = hashlib.sha256(header).digest()
            hash_block = hashlib.sha256(hash_header).digest()

            yield hash_header, hash_block

block_files = sys.argv[1:]
with open("blockchain.db", "wb") as f:
    for path in block_files:
        count = 0
        for hash_header, hash_block in yield_blocks_from_file(path):
            count += 1
            f.write(hash_header + hash_block)
        f.flush()
        print("%s: %d blocks found!" % (path, count))

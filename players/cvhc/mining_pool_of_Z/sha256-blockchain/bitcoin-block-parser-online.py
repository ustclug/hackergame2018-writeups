#!/usr/bin/env python3

import requests
import struct
import hashlib
import os
import time

API_BASE = "https://blockexplorer.com/api/"
BLOCK_START = "000000000000000000108f8529505b52c37af60b7b378ea0e622172e1f149a40"
DB_FILE = "blockchain.db"

def yield_block(start):
    block = start
    timeout = 1

    while True:
        print("Parsing block", block)

        try:
            req = requests.get(API_BASE + "block/" + block)
        except requests.exceptions.ConnectionError:
            failed = True
        else:
            failed = False

        if failed or req.status_code != requests.codes.ok:
            print("Failed! Retry after %d seconds" % timeout)
            time.sleep(timeout)
            timeout *= 2
            continue

        info = req.json()
        header = struct.pack("<I32s32sIII",
                             info["version"],
                             bytes.fromhex(info["previousblockhash"])[::-1],
                             bytes.fromhex(info["merkleroot"])[::-1],
                             info["time"],
                             int(info["bits"], 16),
                             info["nonce"])

        header_hash = hashlib.sha256(header).digest()
        block_hash = hashlib.sha256(header_hash).digest()
        block_hash_hex = block_hash[::-1].hex()
        assert block_hash_hex == block
        yield header_hash, block_hash
        block = info["previousblockhash"]
        timeout = 1


with open(DB_FILE, "a"):
    pass

with open("blockchain.db", "rb+") as f:
    try:
        f.seek(-64, os.SEEK_END)
    except OSError:
        f.seek(0, os.SEEK_SET)
        prev_hash = BLOCK_START
    else:
        prev_hash = f.read(64)[32:]
        prev_hash = prev_hash[::-1].hex()

    pos = f.tell()
    assert pos % 64 == 0
    assert len(prev_hash) == 64
    print("Found %d existing records" % (pos // 64))
    print("Start from:", prev_hash)

    iters = yield_block(prev_hash)
    next(iters)
    for header_hash, block_hash in iters:
        f.write(header_hash + block_hash)

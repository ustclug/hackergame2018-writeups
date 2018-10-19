#!/usr/bin/env python3

import requests
import struct
import hashlib
import os
import time
import hashlib

DB_FILE = "blockchain.db"
with open("blockchain.db", "rb") as f:
    while True:
        data = f.read(64)

        if len(data) == 0:
            break
        elif len(data) != 64:
            raise Exception("Bad file!")

        header_hash = data[:32]
        block_hash = data[32:]
        validate_block_hash = hashlib.sha256(header_hash).digest()
        print("%s -> %s" % (header_hash.hex(), block_hash.hex()))
        if validate_block_hash != block_hash:
            raise Exception("Bad file!")

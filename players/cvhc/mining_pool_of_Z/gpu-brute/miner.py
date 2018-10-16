#!/usr/bin/env python3

import hashlib
import requests
import time
import sys
import string
import random
import base64
import subprocess

COIN_IDX = {
    "md5": 0,
    "sha1": 1,
    "sha256": 2, }
SUFFIX_LEN = {
    "md5": 16,
    "sha1": 4,
    "sha256": 1 }
DIFFICULTY = {
    "md5": 102,
    "sha1": 140,
    "sha256": 199 }
HASH_FUNC = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256 }

coin = sys.argv[1]
session = requests.Session()

coin_idx = COIN_IDX[coin]
hash_func = HASH_FUNC[coin]
target_diff = DIFFICULTY[coin]

while True:
    req = session.post("http://202.38.95.46:12006/getjob")
    job = req.json()
    suffix = job["suffix"][:SUFFIX_LEN[coin]]
    print("suffix:", suffix)

    timeout = job["expire"] - time.time() - 5
    print("Timeout:", timeout)
    try:
        out = subprocess.check_output(
            ["./gpu-brute", coin, suffix, str(16777216)],
            timeout=timeout)
    except subprocess.TimeoutExpired as exp:
        out = exp.output.decode()

    prev_lines = [ "", "" ]
    for line in reversed(out.split("\n")):
        line = line.strip()
        if line.startswith("New record! DIFF = "):
            diff = int(line.split()[-1])
            print("DIFF = %d (target: %d)" % (diff, target_diff))

            buf1 = bytes.fromhex(prev_lines[0])
            nonce1 = buf1[:-len(suffix)]
            buf2 = bytes.fromhex(prev_lines[1])
            nonce2 = buf2[:-len(suffix)]

            data = {
                "coin": coin_idx,
                "nonce1": base64.b64encode(nonce1).decode(),
                "nonce2": base64.b64encode(nonce2).decode(), }
            req = session.post("http://202.38.95.46:12006/submitjob", data=data)
            print(req.json())
            break
        elif line.startswith("MSG1"):
            prev_lines[0] = line.split()[-1]
        elif line.startswith("MSG2"):
            prev_lines[1] = line.split()[-1]

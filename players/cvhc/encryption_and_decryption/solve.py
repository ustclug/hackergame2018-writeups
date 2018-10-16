#!/usr/bin/env python3

import subprocess
import string
import numpy as np
import sympy

# Figure out A, B in Ax + B = y
test_input = bytearray(10)
proc = subprocess.run("./a.out", input=test_input, stdout=subprocess.PIPE)
B = np.frombuffer(proc.stdout, dtype=np.uint8)
A = np.zeros((10, 10), dtype=np.uint8)

for i in range(10):
    test_input[i] = 1
    proc = subprocess.run("./a.out", input=test_input, stdout=subprocess.PIPE)
    test_input[i] = 0
    tmp = np.frombuffer(proc.stdout, dtype=np.uint8)
    A[:, i] = (tmp - B) % 64

# Calculate A's inverse in GF(64)
A_ = sympy.Matrix(A)
A_inv = A_.inv_mod(64)
A_inv = np.array(A_inv).astype(np.uint8)

# Check our result
val_x = np.array([16, 20, 8, 2, 10, 63, 1, 17, 14, 22], dtype=np.uint8)
val_y = np.array([26, 12, 17, 10, 40, 37, 37, 52, 59, 37], dtype=np.uint8)
val_y_check = (A @ val_x + B) % 64
assert np.all(val_y == val_y_check)
val_x_check = A_inv @ (val_y - B) % 64
assert np.all(val_x == val_x_check)

# Hacker game
b64_chars = string.ascii_uppercase \
            + string.ascii_lowercase \
            + string.digits + "-_"
cipher = "JzRVPiVpqo4iDM8celyueIs4ff4DKeG3EMKihzuH"
cipher = np.array([b64_chars.index(c) for c in cipher], dtype=np.uint8).reshape(-1, 10)
plain = A_inv @ (cipher - B).T % 64
plain = "".join([b64_chars[i] for i in plain.T.flatten()])
print(plain)


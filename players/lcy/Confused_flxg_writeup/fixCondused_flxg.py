#!/usr/bin/env python3

import base64

gotlist = "39 65 45 54 77 5F 34 5F 64 5F 66 68 3C 34 58 55 7F 43 21 4B 7F 20 43 76 5F 20 4C 4D 7A 53 70 7D 56 4D 65 47 4C 5D 71 43 18 6F 47 48 42 18 1C 4D 74 45 01 69 00 4D 5B 6D".split()

flxg = ""
ccc = 0
for i in gotlist:
    flxg = flxg + str(chr(int("0x"+i,base=16)^ccc))
    ccc = ccc + 1

print("We got xor:" + flxg)

flxg = flxg[::-1]
print("We reverse it, we get:" + flxg)

flxg = base64.b64decode(bytes(flxg,'utf-8'))

print("We will get the flag:" + str(flxg))

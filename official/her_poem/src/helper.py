#!/usr/bin/env python3
# This script helps you decode "her poem"

from codecs import decode

fin = open("poem.txt", "r")
fout = open("poem.out", "w")

for i in fin:
    data = "begin 666 <data>\n" + i + " \nend\n"
    decode_data = decode(data.encode("ascii"), "uu")
    print(decode_data)
    fout.write(decode_data.decode("ascii") + "\n")

fin.close()
fout.close()
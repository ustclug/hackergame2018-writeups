import string
import base64
import bitarray

def cal_one_line(length):
        leftover = length * 4 % 3
        if leftover == 1: # 16 bits
                return 16
        elif leftover == 2: # 2 bits
                return 8
        else:
                return 0

f = open("poem.txt", "r")
enc_lines = f.read().splitlines()
print(enc_lines)

# find out the hidden FLAG!
def find_hidden_bit(bit_len, bs):
    if bit_len == 8:
        ch_0 = ord(bs[-2]) - 32; ch_1 = ord(bs[-1]) - 32
        hidden_bit = ch_0 & 0b11
        print(bin(hidden_bit))
        return '{0:02b}'.format(hidden_bit) + '{0:06b}'.format(ch_1)
    else:
        ch_0 = ord(bs[-3]) - 32; ch_1 = ord(bs[-2]) - 32; ch_2 = ord(bs[-1]) - 32
        hidden_bit = ch_0 & 0b1111
        print(bin(hidden_bit))
        return '{0:04b}'.format(hidden_bit) + '{0:06b}'.format(ch_1) + '{0:06b}'.format(ch_2)

ba = bitarray.bitarray()
for i in enc_lines:
    len_i = ord(i[0]) - 32
    insert_bit_len = cal_one_line(len_i)
    print(insert_bit_len)
    if insert_bit_len == 0:
        continue
    ba.extend(find_hidden_bit(insert_bit_len, i))
print(ba)
print(ba.tostring())
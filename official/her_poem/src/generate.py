import base64
import string
import bitarray
from codecs import encode

ori_lines = [
        "---------",
        "There is something in this world",
        "that no one has ever seen before.", 
        "It is gentle and sweet.", 
        "Maybe if it could be seen,",
        "everyone would fight over it.",
        "That is why the world hid it,",
        "so that no one could get their hands",
        "on it so easily.",
        "However, someday, someone will find it.",
        "The person who deserves it the most",
        "will definitely find it.",
        "---------",
        "Do you like this school?",
        "I really, really love it.",
        "But nothing can stay unchanged.",
        "Fun things... Happy things...",
        "They can't all possibly stay unchanged.",
        "Even so,",
        "can you go on loving this place?",
        "---------",
        "Sometimes I wonder,",
        "what if this town was alive?",
        "What if it had thoughts and feelings",
        "like one of us?",
        "If it did,",
        "I think it would want to make the people",
        "who live here happy.",
        "---------",
        "Expectations are what you have",
        "when you have given up.",
        "Expectations are born from", 
        "a despairingly large difference in skill.",
        "---------",
        "A joke only lasts for a moment,",
        "if it leaves a misunderstanding,",
        "it becomes a lie.",
        "---------",
        "If someone didn't have any pride,",
        "wouldn't they also be lacking",
        "in self-confidence?",
        "If someone was free of greed,",
        "wouldn't they have trouble",
        "supporting their family?",
        "And if people didn't envy one another,",
        "wouldn't they stop inventing new things?",
        "---------",
        "If I don't have to do it, I won't.",
        "If I have to do it, I'll make it.",
        "---------",
        "/* Here is the end of my poem.",
        "Have you ever found my FLAG? :) */",
        ]
flag = b"flag{STegAn0grAPhy_w1tH_uUeNc0DE_I5_50_fun}"

def cal_one_line(length):
        leftover = length * 4 % 3
        if leftover == 1: # 16 bits
                return 16
        elif leftover == 2: # 2 bits
                return 8
        else:
                return 0

def cnt_bit_len(l):
        return sum(map(lambda x: cal_one_line(len(x)), l))

print(cnt_bit_len(ori_lines))

for i in ori_lines:
        if len(i) > 45: # "M"
                print("line:", i, "is too long.")
                raise ValueError

if cnt_bit_len(ori_lines) != len(flag) * 8:
        print("requires {} bits.".format(len(flag) * 8))
        raise ValueError

encoded_lines = list(map(lambda x: encode(x.encode("ascii"), "uu").splitlines()[1], ori_lines))

print(encoded_lines)

def insert_flag(flag, encoded):
        bit_flag = bitarray.bitarray()
        bit_flag.frombytes(flag)
        bit_flag_taken = 0
        print(bit_flag)
        ret = list(map(bytearray, encoded))
        # for j, i in enumerate(ret):
        #         len_i = i[0] - 32
        #         insert_bit_len = cal_one_line("a" * len_i)
        #         if insert_bit_len == 0:
        #                 continue
        #         if insert_bit_len == 2:
        #                 ch = i[-2]
        #                 new_ch = ((ch - 32) | (int(bit_flag[bit_flag_taken:bit_flag_taken + 2].to01(), 2))) + 32
        #                 ret[j][-1] = new_ch
        #         else:
        #                 ch = i[-3]
        #                 new_ch = ((ch - 32) | (int(bit_flag[bit_flag_taken:bit_flag_taken + 4].to01(), 2))) + 32
        #                 ret[j][-1] = new_ch
        for i, j in enumerate(ret):
                len_this_line = j[0] - 32
                insert_len = cal_one_line(len_this_line)
                if insert_len == 0:
                        continue
                elif insert_len == 8:
                        ch_0 = j[-2] - 32; ch_1 = j[-1] - 32
                        assert ch_1 == 0 # ch_1 should be space (" ", 32)
                        ch_0 |= int(bit_flag[bit_flag_taken:bit_flag_taken + 2].to01(), 2)
                        bit_flag_taken += 2
                        ch_1 = int(bit_flag[bit_flag_taken:bit_flag_taken + 6].to01(), 2)
                        bit_flag_taken += 6
                        ret[i][-2] = ch_0 + 32; ret[i][-1] = ch_1 + 32
                else:
                        ch_0 = j[-3] - 32; ch_1 = j[-2] - 32; ch_2 = j[-1] - 32
                        assert (ch_1 == 0 and ch_2 == 0)
                        ch_0 |= int(bit_flag[bit_flag_taken:bit_flag_taken + 4].to01(), 2)
                        bit_flag_taken += 4
                        ch_1 = int(bit_flag[bit_flag_taken:bit_flag_taken + 6].to01(), 2)
                        bit_flag_taken += 6
                        ch_2 = int(bit_flag[bit_flag_taken:bit_flag_taken + 6].to01(), 2)
                        bit_flag_taken += 6
                        ret[i][-3] = ch_0 + 32; ret[i][-2] = ch_1 + 32; ret[i][-1] = ch_2 + 32
        
        return list(map(lambda x: bytes(x).decode("ascii"), ret))

output = insert_flag(flag, encoded_lines)
# output = list(map(lambda x: x.decode("ascii"), encoded_lines))
print(output)

f = open("poem.txt", "w")
# f.writelines(output)
for i in output:
        f.write(i + "\n")
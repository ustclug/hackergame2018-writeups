#!/usr/bin/python3

import re
import sympy

__author__ = "ustc_zzzz"

bf_code = """
/* author: @ustc_zzzz */ call(`,[->>+++++++>>+++++>>+++>>++>>++++>++++++<<+++<<+++++++++<<++++++++<<
++++++<<++++++++<]>[->>+++++>>+++++++++>>+++++++++>>++>>++++<+++++++++<<++++<<++++<<++<<++<]<,[->>++
+++>>++++++++>>++++++>>+++++++>>+++++++>++++++<<++++++<<++++++++<<+++<<+++<<++++++++<]>[->>++++++++>
>+++>>+++++++>>++++>>+++++++++<++++++<<+++++++++<<++<<+++++++++<<++++++++<]<,[->>++++++++>>+++++++>>
++>>++>>+++++++++>+++<<++++<<+++<<+++++<<++++++++<<++++++++<]>[->>++++>>++++++++>>++++++>>++++++>>++
+++<++++<<+++++++++<<++++++++<<+++++++<<++++<]<,[->>+++++>>+++++++++>>+++>>++++>>++++>+++<<++++++++<
<++++++<<+++++<<++++++<<++++++++<]>[->>++++++>>++++++>>+++++>>++++++++>>+++++++<++++++++<<++++++<<++
+++<<+++<<+++++++<]<,[->>+++++++>>++++>>++++>>+++>>+++++++>+++++++<<+++++++++<<+++++<<+++++<<+++++++
<<++++++++<]>[->>+++>>++++>>++++>>+++++>>++++++<++++<<+++<<++++++++<<+++++++<<+++++<]<,[->>+++++>>++
>>++++>>+++>>++++++>++<<+++++++<<++++<<+++++++++<<+++++++<<++++++++<]>[->>++>>+++++++++>>+++++>>++++
++++>>+++++++++<+++++++<<++<<++++<<+++<<++<]<,[->>++++++>>+++++++>>+++>>++++++>>++++++++>++<<++++<<+
++<<++++++++<<++++++<<++++++++<]>[->>++++++>>++>>+++++++++>>++++>>++++++<+++++<<++++<<++++++++<<++++
<<+++++++<]<,[->>+++++++++>>++++++++>>++++++>>+++++++>>+++++++++>++<<++++++++<<+++++<<+++++<<+++<<++
++++++<]>[->>+++++++++>>+++++++>>+++++++++>>++++>>++<+++++++<<+++++++++<<++<<+++<<++++++++<]<,[->>++
>>++++++++>>++>>++++++>>+++++>++++<<++++<<+++++++<<+++++++<<++++++++<<++++++++<]>[->>+++++++>>++>>++
++++++>>+++++++>>++++<++<<+++<<+++++++<<+++++<<++<]<,[->>+++++++++>>+++++++>>+++++>>++++>>++>+++++<<
+++++<<++<<++<<+++++<<++++++++<]>[->>++++++++>>++++++>>++>>+++++>>+++++++++<++++++++<<++++++++<<++++
<<++++<<+++++++++<]>++.>++++++.>++++++++.>++++++++.>+++.>+++++.>+++++.>+++++++.>++++.>+++++++++.`)"""


def to_matrix(code):
    i = re.compile("[+]+").finditer(code.replace("\n", ""))
    m = [[0 for k in range(11)] for j in range(11)]
    for j in range(10):
        for k in [0, 2, 4, 6, 8, 9, 7, 5, 3, 1]:
            m[j][k] += len(next(i).group(0))
        factor = len(next(i).group(0))
        for k in [1, 3, 5, 7, 9, 8, 6, 4, 2, 0]:
            m[j][k] += factor * len(next(i).group(0))
    for k in range(10):
        m[10][k] += len(next(i).group(0))
    m[10][10] = 1
    return m


def decrypt(matrix):
    base64_mapping = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

    def to_output(output):
        transformed_output = output[:4, :10]
        return "".join([base64_mapping[o % 64] for o in transformed_output])

    def from_input(input):
        transformed_input = [base64_mapping.index(i) for i in input]
        return sympy.Matrix(4, 10, transformed_input).row_join(sympy.ones(4, 1))

    inv_matrix = sympy.Matrix(matrix).inv_mod(64)
    return lambda input: to_output(from_input(input).multiply(inv_matrix))


if __name__ == "__main__":
    fn = decrypt(to_matrix(bf_code))
    assert(fn("aMRKoll07lcf49SIuPrNg8v5bMctTkfrQmchaEkF")
           == "QUICK_BROWN_FOXES_JUMP_OVER_THE_LAZY_DOG")
    assert(fn("p9dJ4Jsrj3oDy_KxMJ1N750NvUBtXVUGNPVALq5l")
           == "quick-brown-foxes-jump-over-the-lazy-dog")
    assert(fn("ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
           == "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    print("flag{" + fn("JzRVPiVpqo4iDM8celyueIs4ff4DKeG3EMKihzuH") + "}")

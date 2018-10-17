
# data = open('encrypt.bf', 'rb').read().replace('\n', '')

# pos = data.find('++')
# while(pos >= 0):
    # i = pos
    # while(data[i] == '+'):
        # i += 1
    # nums = i - pos
    # data = data[:pos] + '+' + str(nums) + data[i:]
    # pos = data.find('++')
# open('br.bf', 'wb').write(data)
nums = [[7, 2, 5, 8, 8, 4, 5, 7, 7, 5, 5, 2, 6, 7, 9, 8, 2, 2, 9, 9], [6, 5, 3, 8, 8, 4, 6, 6, 7, 3, 7, 2, 6, 6, 3, 9, 8, 7, 5, 8], [5, 2, 8, 9, 7, 7, 9, 3, 4, 7, 2, 3, 7, 4, 8, 3, 8, 5, 7, 4], [8, 9, 3, 3, 5, 8, 5, 6, 5, 4, 9, 9, 8, 2, 5, 7, 7, 2, 2, 6], [3, 4, 6, 2, 2, 8, 3, 5, 4, 8, 4, 4, 3, 8, 6, 2, 2, 7, 5, 4], [9, 9, 8, 7, 3, 6, 6, 5, 5, 4, 4, 5, 3, 9, 5, 9, 7, 8, 2, 2], [2, 4, 7, 9, 2, 9, 4, 6, 3, 3, 3, 2, 6, 4, 7, 9, 6, 3, 4, 8], [3, 2, 6, 4, 4, 6, 8, 8, 9, 5, 7, 8, 4, 4, 8, 4, 4, 7, 5, 5], [4, 9, 7, 6, 9, 4, 4, 8, 7, 4, 6, 7, 8, 5, 9, 7, 5, 2, 2, 8], [6, 4, 6, 9, 3, 5, 3, 7, 7, 6, 2, 9, 2, 6, 2, 2, 4, 4, 5, 9]]
last = [2, 6, 8, 8, 3, 5, 5, 7, 4, 9]
base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
def enc(arr):
    ret = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(10):
        for j in range(10):
            ret[j] += arr[i]*nums[j][i*2] + arr[i]*8*nums[j][i*2+1]
    for i in range(10):
        # ret[i] += last[i]
        ret[i] %= 64
    return ret

def dec_1(outputs):
    for i in range(10):
        outputs[i] -= last[i]
        if(outputs[i] < 0):
            outputs[i] += 64
    return outputs
outputs = dec_1([26, 12, 17, 10, 40, 37, 37, 52, 59, 37])
inputs = [16, 20, 8, 2, 10, 63, 1, 17, 14, 22]
import numpy as np
from libnum import invmod

# for i in range(10):
    # inp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # inp[i] = 1
    # print enc(inp)
# [23, 46, 21, 16, 35, 17, 34, 19, 12, 38],
# [5,  3,  16, 27, 22, 0,  15, 38, 55, 14],
# [40, 40, 63, 5,  2,  51, 10, 52, 41, 43],
# [61, 54, 33, 53, 43, 46, 52, 8,  4,  59],
# [47, 31, 60, 37, 4,  37, 27, 49, 39, 55],
# [21, 23, 26, 17, 36, 44, 19, 7,  62, 10],
# [62, 54, 39, 24, 3,  11, 38, 36, 48, 50],
# [9,  11, 32, 61, 22, 13, 15, 40, 1,  18],
# [18, 0,  48, 23, 58, 7,  30, 60, 21, 36],
# [17, 5,  39, 50, 37, 18, 4,  45, 2,  13]
enc_mart = np.matrix(np.array([[23, 46, 21, 16, 35, 17, 34, 19, 12, 38],[5, 3, 16, 27, 22, 0, 15, 38, 55, 14],[40, 40, 63, 5, 2, 51, 10, 52, 41, 43],[61, 54, 33, 53, 43, 46, 52, 8, 4, 59],[47, 31, 60, 37, 4, 37, 27, 49, 39, 55],[21, 23, 26, 17, 36, 44, 19, 7, 62, 10],[62, 54, 39, 24, 3, 11, 38, 36, 48, 50],[9, 11, 32, 61, 22, 13, 15, 40, 1, 18],[18, 0, 48, 23, 58, 7, 30, 60, 21, 36],[17, 5, 39, 50, 37, 18, 4, 45, 2, 13]])).T
def mod_det(mat, m):
    y = len(mat)
    x = len(mat[0])
    ret = 0L
    # print x, y
    if(x == 1):
        return int(mat[0][0])%m
    if(x == 2):
        return int(mat[0][0]*mat[1][1] - mat[0][1]*mat[1][0])%m
    if(x == y):
        for i in range(x):
            tmp_mat = np.delete(mat, 0, 0)
            tmp_mat = np.delete(tmp_mat, i, 1)
            ret += ((-1)**i)*mat[0][i]*mod_det(tmp_mat, m)
            ret %= m
    return ret
def mod_inv(mat, m):
    y = len(mat)
    x = len(mat[0])
    ret = np.zeros((y,x)).astype(int)
    mat_val = mod_det(mat, m)
    inv_val = invmod(mat_val, m)
    for i in range(x):
        for j in range(y):
            tmp_mat = np.delete(mat, j, 0)
            tmp_mat = np.delete(tmp_mat, i, 1)
            ret[j][i] = (-1**(i+j))*(mod_det(tmp_mat, m)*inv_val)%m
            if(ret[j][i] < 0):
                ret[j][i] += m
            print i, j
    return ret
#[16, 20, 8, 2, 10, 63, 1, 17, 14, 22]
# print (enc_mart*np.matrix(np.array(inputs)).T).T%64
# print mod_det(np.array(enc_mart), 64)#5
# print invmod(5, 64)
# print mod_det(np.array([[1,1],[1,2]]), 2)#%64
# dec_mart = np.matrix(mod_inv(np.array(enc_mart), 64))
dec_mart = np.matrix("""
[[ 2 64 29 41 27 26 14  3 25 25]
 [17 20  3 63 24 55 31 53 26 37]
 [34 38 25 22 11 52 12 16  8 46]
 [57 43 25 19 11 10 60 51 57 19]
 [17 56 32 49  2 10 47 53 51 52]
 [45 29 57 32 15 54 44 11 30 53]
 [15 34 22  4 57 32 53 48 62 24]
 [61 41  4 22  9 37 41 35 17 18]
 [45 29 32 40 36 52 19 49 53 31]
 [24 61 52 18  4 28 13 28 64 12]]""").reshape(10,10)
print dec_mart
pwd = ['JzRVPiVpqo','4iDM8celyu','eIs4ff4DKe','G3EMKihzuH']
flag = ''
for w in pwd:
    out = []
    for c in w:
        out.append(base64chars.index(c))
    for i in range(10):
        out[i] -= last[i]
        if(out[i] < 0):
            out[i] += 64
    inp = np.array((dec_mart*np.matrix(np.array(out)).T).T%64)[0]
    for i in range(10):
        flag += base64chars[int(inp[i])]
print flag
# print np.array(inputs)
# print (dec_mart*np.matrix(np.array(outputs)).T).T%64

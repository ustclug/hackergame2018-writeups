### 加密算法和解密算法

做题时并没有发现有SymPy这种好东西，在分析出加密矩阵后手写了在模空间求矩阵的逆的函数，而且还贼慢，跑了一段时间才出来结果。。

	import numpy as np
	from libnum import invmod
	
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
	
	dec_mart = np.matrix(mod_inv(np.array(enc_mart), 64))
	
	base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
	pwd = ['JzRVPiVpqo','4iDM8celyu','eIs4ff4DKe','G3EMKihzuH']
	last = [2, 6, 8, 8, 3, 5, 5, 7, 4, 9]
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
	# h1ll-c1ph3r-w1th-10x10-r3v3rs1bl3-matr1x

从分析encrypt.bf开始的代码详见dec.py。

[返回](../)
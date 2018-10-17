### 困惑的flxg小程序  

用ida打开后，打开字符串列表，并查找对正确提示信息"祝贺你，你输入的flxg是正确的！"的引用，可以找到关键函数sub_14000498F；分析可知该函数先从1400054D8处取出56个字节，并将输入的字符串做base64编码然后倒转，之后倒转后的每个字节再和下标异或去和1400054D8处取出的56个字节作对比；于是反过来先将1400054D8处的56个字节每个字节和下标异或再倒转再base64解码就可以得到flag。

	import base64
	
	a='39654554775F345F645F66683C3458557F43214B7F2043765F204C4D7A53707D564D65474C5D7143186F474842181C4D74450169004D5B6D'.decode('hex')
	
	b = ''
	i = 0
	for c in a:
	    b += chr(i ^ ord(c))
	    i += 1
	b = b[::-1]
	print b
	print base64.b64decode(b)
	# flxg{Congratulations_U_FiNd_the_trUe_flXg}

[返回](../)
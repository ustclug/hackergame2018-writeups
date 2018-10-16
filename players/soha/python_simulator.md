[返回](./README.md)

## 0x08 猫咪克星

用人的手速肯定不行（但我还是天真的用手来了几次），所以我专门写了个 Python 程序来做题。刚开始觉得很简单就是个eval，后来发现太狡猾了他们，还有 `exit()` ， `sleep(100)` 这种万恶的语句来让我们的 eval 爆炸。

机智的我使用了替换大法！最后的程序是这样的

```python
from socket import *
tcpClient=socket(AF_INET,SOCK_STREAM)
tcpClient.connect(("202.38.95.46",12009))

while True:
	data=tcpClient.recv(1024).decode(encoding="utf-8") 
	print(data)
	try:
		if "flag{" in data:
			exit()
		result=eval(data.replace("exit()","0").replace("sleep(100)","sleep(0)"))
		rtn=str(result)+"\n"
		print(rtn)
		tcpClient.send(rtn.encode(encoding="utf-8"))
	except Exception as e:
		pass

tcpClient.close()
```

拿到了！

![Snipaste_2018-10-09_21-25-05.png](./images/909917520.png)

# 猫咪克星

by fjw

啊看这个这么显然的就是想让你用 Python `eval()` 那我就来一个呗。

自己试着跑一下看看规律，然后首先要处理交互问题。基于我在 GitHub 上做了半年多的一个大型开源项目的经验(谦虚地不放链接)，第一想法是 `subprocess.Popen` 了。把 `nc` 打开然后对它的标准输入输出进行读写。

```python
import subprocess as sp

p = sp.Popen(CMD, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

print(p.stdout.readline())  # 过滤掉第一行
```

接下来放个循环干一下试试：

```python
while True:
    i = p.stdout.readline().strip().decode("utf-8")
    print(i)
    t = str(eval(i))
    print(t)
    p.stdin.write((t + "\n").encode("utf-8"))
    p.stdin.flush()
```

（注：那个 `p.stdin.flush()` 坑了我好久，原来写入换行符没有自动 flush 的。。。）

很快就出现问题了，那个 `i` 可能包含奇怪的东西，例如 `exit()` 需要过滤。当然，更保险的办法是验证一下表达式是否合法，然后再运行。还是考虑到我有那个大型开源项目的经验 (这次毫不谦虚地把[链接](https://github.com/Charcoal-SE/SmokeDetector)放了出来，滑稽)，我选择 `regex` （注：需要从 PyPI 下载安装，当然也可以直接用自带的 `re` 替换）。

数一数正常表达式中会出现的字符以及需要替换的东西，列出两个正则：

```python
import regex
validator = regex.compile(r"""^(?:[0-9()+*/=^&%<>|!\s-]|int)*$""")
replacer = regex.compile(r"""exit\(\)""")
```

同时修改那个有点危险的循环，加入一个 `input()` 让我有机会观察异常表达式：

```python
while True:
    i = p.stdout.readline().strip().decode("utf-8")
    print(i)
    if validator.search(i):
        t = str(eval(i))
    else:
        i = replacer.sub("None", i)  # <<<<<<<<<<<<<<<<
        print("Replaced: {}".format(i))
        if validator.search(i):
            t = str(eval(i))
        else:
            t = input()
    if t.strip() == "stop":
        break
    print(t)
    p.stdin.write((t + "\n").encode("utf-8"))
    p.stdin.flush()
```

等等我忘了把自己替换出来的 `None` 给加进验证器里了：

```python
validator = regex.compile(r"""^(?:[0-9()+*/=^&%<>|!\s-]|int|None)*$""")
```



再跑几回，把可能出现的异常表达式都加进 `replacer` 里面：

```python
replacer = regex.compile(r"""(exit\(\)|__import__\('time'\).sleep\(\d+\)|__import__\('os'\).system\('find ~'\)|print\('[\\x0-9a-f]+'\))""")
```

最后发现 flag 并停止，把这个也加进去，得到最终代码：

```python
import subprocess as sp
import regex

CMD = "nc 202.38.95.46 12009".split()

p = sp.Popen(CMD, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

print(p.stdout.readline())

validator = regex.compile(r"""^\s*(?:[0-9()+*/=^&%-<>|!\s]|int|None)*\s*$""")
replacer = regex.compile(r"""(exit\(\)|__import__\('time'\).sleep\(\d+\)|__import__\('os'\).system\('find ~'\)|print\('[\\x0-9a-f]+'\))""")

while True:
    i = p.stdout.readline().strip().decode("utf-8")
    print(i)
    if validator.search(i):
        t = str(eval(i))
    elif i.startswith("flag{"):
        print("Flag found, end.")
        exit(0)
    else:
        i = replacer.sub("None", i)
        print("Replaced: {}".format(i))
        if validator.search(i):
            t = str(eval(i))
        else:
            t = input()
    if t.startswith("."):
        break
    print(t)
    p.stdin.write((t + "\n").encode("utf-8"))
    p.stdin.flush()
```

运行，安全通过，得到 flag:

```
flag{'Life_1s_sh0rt_use_PYTH0N'*1000}
Flag found, end.
```


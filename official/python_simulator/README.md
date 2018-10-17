# 猫咪克星

欢迎来到猫咪系列题目之**猫咪克星**。

这道题是一道非常简单的题目，主要是想让同学们学会一些 Python 编程技巧，同时理解 `eval` 函数的危险性。

## 分析

根据题目描述

> 给你一些 Python 3 表达式，如果你能正确计算出来，你就通过了验证。
>
> 赶快使用命令 nc 202.38.95.46 12009 来开始吧

我们使用题目中提供的命令来连接服务器

```
$ nc 202.38.95.46 12009
You have only 30 seconds
(((134-13)|(1&2))*((23^51)^(18>>86)))
```

远程服务器告诉我们只有 30 秒的时间，然后显示出一个 Python 3 的表达式。如果我们随便输入一个答案并且按回车，会得到 `Your answer is wrong!` 的提示，然后程序退出。如果我们使用 `python3` 命令开启一个 Python 交互式环境，然后输入我们的表达式，再把得到结果输入回 `nc` 命令那里，则会得到新的表达式

```
$ python3
Python 3.7.0 (default, Jun 29 2018, 20:13:13)
[Clang 9.1.0 (clang-902.0.39.2)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> (((134-13)|(1&2))*((23^51)^(18>>86)))
4356
```

```
$ nc 202.38.95.46 12009
You have only 30 seconds
(((134-13)|(1&2))*((23^51)^(18>>86)))
4356
((int(43>=1)^(2**2))-((120<<84)&int(10<2)))
```

我们如果继续手工计算，会发现表达式很多，30 秒的时间内做不完，所以我们需要用程序自动化完成这一切。

我们需要解决两个问题：

1. 如何在程序中模拟 nc 命令的行为，连接服务器
2. 如何在程序中把一个 Python 3 的表达式（字符串）计算成它的结果

对于第一个问题，我们知道 nc 命令实际上就是用 tcp 协议连接了服务器的端口，我们可以在程序中直接建立 socket 连接来与服务器交互。但是，这种方式比较原始，需要自己解决很多问题。我们可以使用 Python 的 telnetlib、pwntools 等库来方便地与 socket 连接交互，还可以使用 popen、pexpect 等库来启动一个 nc 进程并且与进程交互。我们这里使用一种更简便的方法，用 socat 命令。socat 可以用来把一个程序的标准输入输出和一个网络连接对接起来，这样我们的解题脚本就不需要处理连接服务器的问题了，而只需要正常地使用 `input()` 读入数据并且使用 `print()` 输出。

对于第二个问题，Python 的 `eval` 函数可以把表达式（字符串）求值，例如

```
>>> eval('(((134-13)|(1&2))*((23^51)^(18>>86)))')
4356
```

## 解答

我们可以编写代码如下：

```python
#!/usr/bin/env python3

import sys

input()
while True:
    expr = input()
    print(expr, file=sys.stderr)
    ans = eval(expr)
    print(ans, file=sys.stderr)
    print(ans)
```

将以上代码保存为 `sol.py` 然后执行 `socat exec:./sol.py tcp:202.38.95.46:12009`

我们发现，程序执行一半会停下。从输出中可以看出，表达式会包含一些数学运算之外的函数调用，例如 `__import__('time').sleep(100)` 等。

我们可以用字符串替换的方式把这些表达式替换成它们的返回值。值得注意的是，`exit` 函数并没有返回值，这是这道题的一处缺陷，我们把它当做 None 或者任何不等于正整数的值即可。

最终的程序如下：

```python
#!/usr/bin/env python3

import sys

tricks=[
        "__import__('os').system('find ~')",
        "__import__('time').sleep(100)",
        r"print('\x1b\x5b\x33\x3b\x4a\x1b\x5b\x48\x1b\x5b\x32\x4a')",
        'exit()'
]

def removetricks(s):
    for t in tricks:
        s = s.replace(t,'None')
    return s

input()

for i in range(100):
    print(i, file=sys.stderr)
    expr = input()
    print(expr, file=sys.stderr)
    ans = eval(removetricks(expr))
    print(ans, file=sys.stderr)
    print(ans)

print(input(), file=sys.stderr)
```

以上保存为 `sol.py` 然后执行 `socat exec:./sol.py tcp:202.38.95.46:12009` 即可

除了字符串替换外，我们也可以使用 `eval` 的第二个参数来将当前作用域内的函数替换掉，代码如下：

```python
import sys

def f(*args, **kwargs):
    return None

class C:
    def __getattr__(self, x):
        return f

input()
while True:
    expr = input()
    print(expr, file=sys.stderr)
    ans = eval(expr,{'__import__':lambda x:C(),'exit':f,'print':f})
    print(ans, file=sys.stderr)
    print(ans)
```

但是要注意，即使把所有内置对象都替换掉，也不意味这 `eval` 任意的输入就是安全的，详见 [Python 沙箱逃逸](https://ctf-wiki.github.io/ctf-wiki/pwn/linux/sandbox/python-sandbox-escape/)

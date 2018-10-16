# 猫咪克星

欢迎来到猫咪系列题目之**猫咪克星**。

这道题是一道非常简单的题目，主要是想让同学们学会一些 Python 编程技巧。

**TODO：连接远程服务器的若干种方法、如何通过替换库函数解题**

先贴上解题程序，明天补细节

```python
#!/usr/bin/env python3 -u

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

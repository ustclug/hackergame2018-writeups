# 猫咪克星

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

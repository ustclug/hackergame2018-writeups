#!/usr/bin/env python3 -u

import signal
import random
import math

def timeout(signum, frame):
    print('Timeout!')
    exit()

signal.signal(signal.SIGALRM, timeout)
signal.alarm(30)
print('You have only 30 seconds')

def rint():
    return str(int(math.e ** random.uniform(0, 5)))

def rbigint():
    digit = random.randrange(64,128)
    return str(random.randrange(2**digit, 2**(digit+1)))

binops=['+','-','*','&','|','^']
nonbigops=['**','<<','>>']
boolops=['==','!=','>','<','>=','<=']

def rexp(n=3, trick=False):
    if n:
        return rbinop(n, trick)
    else:
        if not trick:
            return rint()
        else:
            if random.randrange(100)<20:
                return rtrickexp()
            else:
                return rint()

def rbigexp(n=2):
    if n:
        return rbigbinop(n)
    else:
        return rbigint()

def rbinop(n, trick=False):
    e1 = rexp(n-1, trick)
    e2 = rexp(n-1, trick)
    if random.randrange(100) > 20:
        if n==1:
            op = random.choice(binops+nonbigops)
        else:
            op = random.choice(binops)
        return '('+e1+op+e2+')'
    else:
        op = random.choice(boolops)
        return 'int('+e1+op+e2+')'

def rbigbinop(n):
    e1 = rbigexp(n-1)
    e2 = rbigexp(n-1)
    op = random.choice(binops)
    return '('+e1+op+e2+')'

tricks=[
        "__import__('os').system('find ~')",
        "__import__('time').sleep(100)",
        r"print('\x1b\x5b\x33\x3b\x4a\x1b\x5b\x48\x1b\x5b\x32\x4a')",
        'exit()'
]

def rtrickexp():
    op = random.choice(['==','!='])
    e1 = random.choice(tricks)
    e2 = rint()
    if random.randrange(2):
        e1, e2 = e2, e1
    return 'int('+e1+op+e2+')'

def removetricks(s):
    for t in tricks:
        s = s.replace(t,'None')
    return s

for i in range(100):
    if i < 30:
        expr = rexp()
    elif i < 50:
        expr = rbigexp()
    else:
        expr = rexp(trick=True)
    print(expr)
    ans = int(input())
    #ans = eval(removetricks(expr))
    #print(ans)
    if ans != eval(removetricks(expr)):
        print('Your answer is wrong!')
        exit()

flag="flag{'Life_1s_sh0rt_use_PYTH0N'*1000}"
print(flag)

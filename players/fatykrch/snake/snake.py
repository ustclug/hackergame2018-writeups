from pwn import *
connectstr = "202.38.95.46 12009"

connectstr = connectstr.split(' ')
p = remote(connectstr[0], connectstr[1])

def ret_1():
    return 1
def ret_0():
    return 0
def ret_1_arg(arg):
    return 1
def ret_0_arg(arg):
    return 0

exit = ret_0
__import__('time').sleep = ret_0_arg
__import__('os').system = ret_0_arg

p.recvline()
while(1):
    exp = p.recvline()
    print exp
    p.send(str(eval(exp.replace('print', 'ret_0_arg')))+'\n')
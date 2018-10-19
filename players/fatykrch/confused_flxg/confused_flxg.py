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
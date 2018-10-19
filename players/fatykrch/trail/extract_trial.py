
from hexdump import hexdump
from PIL import Image
# data = open('emm', 'rb').read()
base64chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/'
trial = Image.open("trial.webp")
trial.save("trial.png")
print trial.size

t = Image.open("trial2.png")
white = (255,255,255)
data = ''

bit = 0
a = 0
for j in range(629):
    for i in range(642):
        pixel = t.getpixel((i, j))
        if(pixel != white and pixel[0]^pixel[2]):
            a *= 2
            a += pixel[1]&1
            bit += 1
            if(bit == 8):
                data += chr(a)
                a = 0
                bit = 0
open("trialdata", 'wb').write(data)
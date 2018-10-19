
from PIL import Image

data = open('malbolge.txt', 'rb').read()
# print len(data)
# 2^2 * 139 * 277
width = 277
height = 4*139
image = Image.new('RGB', (width+1, height+1), (255, 255, 255))
for i in xrange(width*height):
    if(data[i] == ' '):
        image.putpixel((width-i/height, i%height), (255, 255, 255))
    else:
        image.putpixel((width-i/height, i%height), (0, 0, 0))
image.save("233.jpg")
"""

mmmummm  mmmm  mmmmm          mmmm  mmmmmm   mmm  mmmmm  mmmmmmmmmmmmm
   #    m"  "m #   "#        #"   " #      m"   " #   "# #        #
   #    #    # smmm#"        "#mmm  #mmtmm #      #mmmm" cmmmmm   #
   #    #    # #                 "# #      #      #   "m #        #
   #     #mm#  #             "mmm#" #mmmmm  "mmm" #    " #mmmmm   #
   
"""

# There are two parts (TODOs) remaining to be filled. Please read through the code.

from __future__ import print_function, division
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import random

from main import Net

def solve():
    model = load_model()
    image = Image.open('target.png')
    image = convert2tensor(image)
    modifier = Variable(torch.from_numpy(np.zeros((30,30)).astype('f')))
    modifier.requires_grad = True
    target = Image.open('target.png')
    target = convert2tensor(target)
    target_inputs = preprocess_image(target)
    target_pred = model(target_inputs)
    tlab  = torch.Tensor([0,0,0,0,0,0,0,0,0,0])
    tlab[4] = 1
    optimizer = optim.Adam([modifier], lr=0.1)
    CONFIDENCE = 5
    for i in range(1000):
        inputs = torch.clamp(torch.clamp(modifier, -0.195, 0.195)+target_inputs, 0, 1)
        pred = model((inputs-0.1307)/0.3081)
        real = torch.sum(tlab*pred, 1)
        other = torch.max((1-tlab)*pred - (tlab*10000), 1)
        loss1 = torch.sum(inputs != target_inputs)
        loss2 = F.l1_loss(inputs, target_inputs)
        loss3 = torch.max(torch.abs(inputs-target_inputs))
        loss_label = torch.max(torch.Tensor([0]), other[0]-real+CONFIDENCE)
        # loss = loss_label+loss1+loss2+loss3
        loss = loss_label+loss2+loss3
        # print(dir(optimizer))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if(i%100 == 0):
            print("")
            print(pred)
            print(loss.item(),loss_label.item(),loss1.item(),loss2.item(),loss3.item())
    # TODO: Part 1
    # Add your code here. Feel free to import any modules you like.
    # Helpful info:
    # 0. Please use the **latest** version of pytorch & torchvision
    # 1. Use `torch.clamp(x, 0, 1)` to clip x's value between [0, 1]
    # 2. This function expects the pixel values of a returned image are between [0, 1]
    # 3. Set `x.requires_grad = True` if you want to get the gradient of `x`
    return input2image(inputs, image)

def convert2tensor(image):
    return torch.from_numpy(np.array(image).astype('f') / 255.)

def convert2image(arr):
    return Image.fromarray((arr.detach().numpy() * 255).astype(np.uint8), mode='L')

def input2image(arr, image):
    for x in range(0,30):
        for y in range(0, 30):
            image[10+y*20][10+x*20] = arr[0][0][y][x]
    return image
    
def preprocess_image(arr):
    ret = Variable(torch.from_numpy(np.zeros((30,30)).astype('f')))
    for x in range(0,30):
        for y in range(0, 30):
            ret[y][x] = arr[10+y*20][10+x*20]
    return ret.reshape(1, 1, 30 ,30)
    # image = convert2image(arr)
    # image = image.resize((30, 30), resample=Image.NEAREST)
    # return convert2tensor(image).reshape(1, 1, 30 ,30)

def load_model():
    model = Net()
    model.load_state_dict(torch.load('model.pth'))
    model.eval()
    return model

def check():
    model = load_model()

    target = convert2tensor(Image.open('target.png'))
    sample = convert2tensor(Image.open('sample.png'))
    if torch.sum(target != sample) >= 600 * 600 * 0.002:
        print('Input l1 hacking is detected! Game over.')
    if F.l1_loss(target, sample) >= 0.001:
        print('Input l2 hacking is detected! Game over.')
    if (torch.max(torch.abs(target - sample))) >= 0.2:
        print(torch.max(torch.abs(target - sample)))
        print('Input l0 hacking is detected! Game over.')
    target = (preprocess_image(target)-0.1307)/0.3081
    sample = (preprocess_image(sample)-0.1307)/0.3081
    print(model(target))
    print(model(sample))
    truth = torch.argmax(model(target))
    hack = torch.argmax(model(sample))
    print(int(truth), int(hack))
    if int(truth) == int(hack):
        print('Fail to hack. Game over.')
    else:
        print('Cong! You win!!!')


if __name__ == '__main__':
    output = solve()
    convert2image(output).save('sample.png')
    # You have to pass this check!
    check()

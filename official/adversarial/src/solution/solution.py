"""

mmmummm  mmmm  mmsmm          mmmm  mmmmmm   mtm  mmcmm  mmmmmmmmmmmmm
   #    m"  "m #   "#        #"   " #      m"   " #   "# #        #
   #    #    # #mmm#"        "#mmm  #mmmmm #      #mmmm" #mmmmm   #
   #    #    # #                 "# #      #      #   "m #        #
   #     #mm#  #             "mmm#" #mmmmm  "mmm" #    " #mmmmm   #
   
"""

from __future__ import print_function, division
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F

from main import Net

def solve():
    model = load_model()
    image = Image.open('target.png')
    image = convert2tensor(image)
    inputs = preprocess_image(image)
    label = torch.tensor([6], dtype=torch.long)
    
    # A solution for part 1
    inputs.requires_grad = True
    x = (inputs - 0.1307) / 0.3081  # scale mean & std 
    output = model(x)
    loss = F.nll_loss(output, label)
    loss.backward()
    x_grad = torch.sign(inputs.grad.data)
    epsilon = 0.18
    inputs = torch.clamp(inputs + epsilon * x_grad, 0, 1)
    
    inputs = inputs.reshape(30, 30)

    for i in range(30):
        for j in range(30):
            image[int((i + 0.5) * 20), int((j + 0.5) * 20)] = inputs[i, j]

    return image

def convert2tensor(image):
    return torch.from_numpy(np.array(image).astype('f') / 255.)

def convert2image(arr):
    return Image.fromarray((arr.detach().numpy() * 255).astype(np.uint8), mode='L')
    
def preprocess_image(arr):
    image = convert2image(arr)
    image = image.resize((30, 30), resample=Image.NEAREST)
    return convert2tensor(image).reshape(1, 1, 30 ,30)

def load_model():
    model = Net()
    model.load_state_dict(torch.load('model.pth'))
    model.eval()
    return model

def check():
    model = load_model()

    target = convert2tensor(Image.open('target.png'))
    sample = convert2tensor(Image.open('sample.png'))
    assert torch.sum(target != sample) < 600 * 600 * 0.002, 'Input hacking is detected! Game over.'
    assert F.l1_loss(target, sample) < 0.001, 'Input hacking is detected! Game over.'
    assert (torch.max(torch.abs(target - sample))) < 0.2, 'Input hacking is detected! Game over.'
    target = preprocess_image(target)
    sample = preprocess_image(sample)
    # A solution for part 2
    target = (target - 0.1307) / 0.3081 
    sample = (sample - 0.1307) / 0.3081

    truth = torch.argmax(model(target))
    hack = torch.argmax(model(sample))
    assert int(truth) != int(hack), 'Fail to hack. Game over.'
    print('Cong! You win!!!')


if __name__ == '__main__':
    output = solve()
    convert2image(output).save('sample.png')
    # You have to pass this check!
    check()

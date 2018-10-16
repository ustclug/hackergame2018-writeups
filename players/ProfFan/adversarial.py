"""

mmmummm  mmmm  mmmmm          mmmm  mmmmmm   mmm  mmmmm  mmmmmmmmmmmmm
   #    m"  "m #   "#        #"   " #      m"   " #   "# #        #
   #    #    # smmm#"        "#mmm  #mmtmm #      #mmmm" cmmmmm   #
   #    #    # #                 "# #      #      #   "m #        #
   #     #mm#  #             "mmm#" #mmmmm  "mmm" #    " #mmmmm   #
   

flag= flag{Go down the rabbit hole of deep learning}
"""

# There are two parts (TODOs) remaining to be filled. Please read through the code.

from __future__ import print_function, division
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import datasets, transforms
import cv2

from main import Net

def fgsm_attack(image, epsilon, data_grad):
    # Collect the element-wise sign of the data gradient
    sign_data_grad = data_grad.sign()
    # Create the perturbed image by adjusting each pixel of the input image
    perturbed_image = image + epsilon*sign_data_grad
    # Adding clipping to maintain [0,1] range
    #perturbed_image = torch.clamp(perturbed_image, 0, 1)
    # Return the perturbed image
    return perturbed_image

def solve():
    # MNIST Test dataset and dataloader declaration
    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('../data', train=False, download=True, transform=transforms.Compose([
                transforms.Resize((30, 30)),
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,)),
                ])), 
            batch_size=1, shuffle=True)

    model = load_model()
    image = Image.open('target.png')
    image = convert2tensor(image)
    inputs = preprocess_image(image)

    inputs = (inputs - 0.1307) / 0.3081
    label = torch.tensor([6], dtype=torch.long)
    # TODO: Part 1
    # Add your code here. Feel free to import any modules you like.

    # Helpful info:
    # 0. Please use the **latest** version of pytorch & torchvision
    # 1. Use `torch.clamp(x, 0, 1)` to clip x's value between [0, 1]
    # 2. This function expects the pixel values of a returned image are between [0, 1]
    # 3. Set `x.requires_grad = True` if you want to get the gradient of `x`
    # torch.clamp(inputs, 0, 1)
    inputs.requires_grad = True
    # raise NotImplementedError('You have to implement this segment by yourself.')
    output = model(inputs)

    init_pred = output.max(1, keepdim=True)[1]
    print(init_pred)
    # Calculate the loss
    loss = F.nll_loss(output, label)

    # Zero all existing gradients
    model.zero_grad()

    # Calculate gradients of model in backward pass
    loss.backward()

    for dif in np.arange(0, 1., 0.05):
        
        print("DIF: ", dif)
        # Collect datagrad
        perturbed_r = fgsm_attack(inputs, dif, inputs.grad.data)
        perturbed = perturbed_r * 0.3081 + 0.1307
        perturbed = torch.clamp(perturbed, 0, 1)

        if torch.argmax(model((perturbed - 0.1307)/0.3081)) != label:
            return perturbed.reshape((30,30))

    raise ("SHIT!")

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

def postprocess(x,orig_r):
    ratio = 20
    print("Ratio:", ratio)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            orig_r[i*ratio + (ratio//2)][j*ratio + (ratio//2)] = x[i][j]
    return orig_r

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def check():
    model = load_model()

    target = convert2tensor(Image.open('target.png'))
    sample = convert2tensor(Image.open('target.png'))
    rsample = convert2tensor(Image.open('miniture.png'))

    sample = postprocess(rsample, sample)    
    # sample = convert2tensor(Image.open('miniture.png').resize((600,600),2))
    
    for i in range(0,600):
        for j in range(0,600):
            if sample[i][j] - target[i][j] >= 0.2:
                sample[i][j] = target[i][j] + 0.196
            if target[i][j] - sample[i][j] >= 0.2:
                sample[i][j] = target[i][j] - 0.16
    convert2image(sample).save("sample.png")
    assert (torch.max(torch.abs(target - sample))) < 0.2, 'Input hacking is detected! Game over.'
    assert torch.sum(target != sample) < 600 * 600 * 0.002, 'Input hacking is detected! Game over.'
    assert F.l1_loss(target, sample) < 0.001, 'Input hacking is detected! Game over.'
    target = preprocess_image(target)
    sample = preprocess_image(sample)
    target = (target - 0.1307) / 0.3081
    
    sample = (sample - 0.1307) / 0.3081
    # TODO: Part 2
    #raise NotImplementedError('Two lines of codes is lost here. Inspect `main.py` and fill them!')
    print(type(target.numpy()))
    #cv2.imshow("target", target.numpy().reshape(30,30))
    #cv2.imshow("orig", sample.numpy().reshape(30,30))
    #cv2.waitKey()

    print(softmax(model(target).data.numpy()[0]))
    print(softmax(model(sample).data.numpy()[0]))
    truth = torch.argmax(model(target))
    hack = torch.argmax(model(sample))
    print(truth)
    print("H:", hack)
    assert int(truth) != int(hack), 'Fail to hack. Game over.'
    print('Cong! You win!!!')


if __name__ == '__main__':
    output = solve()
    convert2image(output).save('miniture.png')
    # You have to pass this check!
    check()

# 这个文件和答案无关，只是展示获取 target.png 的方式
from __future__ import print_function
import torch
from torchvision import datasets, transforms
import numpy as np
from PIL import Image

test_loader = torch.utils.data.DataLoader(
        datasets.MNIST('data', train=False, transform=transforms.Compose([
            transforms.Resize((30, 30)),
            transforms.ToTensor(),
            # transforms.Normalize((0.1307,), (0.3081,)),
])), batch_size=1, shuffle=False)

for i, (data, target) in enumerate(test_loader):
    if i != 534:
        continue
    else:
        data = (np.array(data).reshape(30, 30) * 255).astype(np.uint8)
        img = Image.fromarray(data, mode='L')
        img = img.resize((600, 600), resample=Image.BILINEAR)
        img.save('target.png')
        break

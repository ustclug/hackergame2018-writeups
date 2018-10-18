import io
import time
from flask import Flask, request

import numpy as np
from PIL import Image
import torch
import torch.nn.functional as F

from main import Net

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # Limit file size.

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

def check(sample_file):
    time.sleep(1) # negative optimization
    model = load_model()

    target = convert2tensor(Image.open('target.png'))
    sample = convert2tensor(Image.open(sample_file))
    assert torch.sum(target != sample) < 600 * 600 * 0.002, 'Input hacking is detected! Game over.'
    assert F.l1_loss(target, sample) < 0.001, 'Input hacking is detected! Game over.'
    assert (torch.max(torch.abs(target - sample))) < 0.2, 'Input hacking is detected! Game over.'
    target = preprocess_image(target)
    sample = preprocess_image(sample)
    target = (target - 0.1307) / 0.3081
    sample = (sample - 0.1307) / 0.3081
    truth = torch.argmax(model(target))
    hack = torch.argmax(model(sample))
    assert int(truth) != int(hack), 'Fail to hack. Game over.'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            in_memory_file = io.BytesIO()
            file.save(in_memory_file)
            check(in_memory_file)
            return "flag{Go down the rabbit hole of deep learning}"
        except:
            return '<meta http-equiv="refresh" content="3;url=/"/>FAIL (return in 3 sec...)'
    return '''
    <!doctype html>
    <title>Adversarial</title>
    <h1>Upload sample.png</h1>
    <p>(界面美工师带着正版Adobe全家桶跑路了)</p>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="上传选择的文件 (文件大小 < 1MB)">
    </form>
    '''

if __name__ == '__main__':
    app.secret_key = 'this_is_not_the_real_key_on_the_server'
    app.run(threaded=True, host='0.0.0.0', port=5000)

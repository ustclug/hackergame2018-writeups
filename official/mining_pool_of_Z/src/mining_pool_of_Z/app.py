import base64
import hashlib
import random
import string
import time
import logging
import uuid

from logging.handlers import RotatingFileHandler
from flask import Flask, session, render_template, jsonify, request
from functools import wraps

app = Flask(__name__)

suffix_lengths = [16, 4, 1]
thresholds = [102, 140, 199]  # these numbers are carefully chosen, please don't modify
flags = ['flag{md5_7cfa0da2c09776ae}',
         'flag{sha1_21d0e7b1be5a3cae}',
         'flag{sha256_02938baf7abc9cd3}']


def userid():
    if 'uid' not in session:
        session['uid'] = uuid.uuid4()
    return session['uid']


def log(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        r = f(*args, **kwargs)

        form_repr = []
        for k, v in request.form.items():
            if len(v) > 1024:
                form_repr.append((k, v[:1024] + '...'))
            else:
                form_repr.append((k, v))

        app.logger.info('%s: user=%s data=%s result=%s',
                        request.full_path,
                        userid(),
                        form_repr,
                        r.get_data()
                        )
        return r

    return wrapper


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getjob', methods=['POST'])
@log
def getjob():
    suffix = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(max(suffix_lengths))])
    expire = time.time() + 60
    session['suffix'] = suffix
    session['expire'] = expire
    return jsonify({
        'suffix': suffix,
        'expire': expire
    })


def difficulty(nonce1, nonce2, algo):
    hash_func = [hashlib.md5, hashlib.sha1, hashlib.sha256][algo]
    hash_digit = [128, 160, 256]
    hash1 = int(hash_func(nonce1).hexdigest(), 16)
    hash2 = int(hash_func(nonce2).hexdigest(), 16)
    hash_xor = hash1 ^ hash2
    d = 0
    for i in range(hash_digit[algo]):
        if (hash_xor >> i) & 1 == 0:
            d += 1
    return d


@app.route('/submitjob', methods=['POST'])
@log
def submitjob():
    try:
        nonce1 = base64.b64decode(request.form['nonce1'])
        nonce2 = base64.b64decode(request.form['nonce2'])
        coin = int(request.form['coin'])
    except:
        return jsonify({
            'success': False,
            'info': 'input is not valid'
        })
    if 'expire' not in session or session['expire'] < time.time():
        return jsonify({
            'success': False,
            'info': 'job expired or does not exist'
        })
    elif nonce1 == nonce2:
        return jsonify({
            'success': False,
            'info': 'nonce should not be the same'
        })
    elif coin not in [0, 1, 2]:
        return jsonify({
            'success': False,
            'info': 'coin variant does not exist'
        })
    else:
        suffix = session['suffix'].encode()[:suffix_lengths[coin]]
        diff = difficulty(nonce1 + suffix, nonce2 + suffix, coin)
        if coin == 0 and diff == 128:
            return jsonify({
                'success': False,
                'info': "Don't trick me by MD5 collisions!"
            })
        if diff >= thresholds[coin]:
            return jsonify({
                'success': True,
                'info': flags[coin]
            })
        else:
            return jsonify({
                'success': True,
                'info': format(
                    'Your difficulty = %s, target difficulty = %s. Please reach target difficulty to get the flag!'
                    % (diff, thresholds[coin]))
            })


if __name__ == '__main__':
    handler = RotatingFileHandler('/log/app.log', maxBytes=1024 * 1024 * 100, backupCount=100)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.secret_key = 'this_is_not_the_real_key_on_the_server'
    app.run('0.0.0.0', 5000, threaded=True)

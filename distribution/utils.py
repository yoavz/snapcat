from time import time
from Crypto.Cipher import AES
import hashlib
import requests

# github.com/martinp/pysnap and gibsonsec.org/snapchat

URL = 'https://feelinsonice-hrd.appspot.com/bq/'

def pkcs5_pad(data, blocksize=16):
    pad_count = blocksize - len(data) % blocksize
    return data + (chr(pad_count) * pad_count).encode('utf-8')

def encrypt(data):
    BLOB_ENCRYPTION_KEY = 'M02cnQ51Ji97vwT4'
    cipher = AES.new(BLOB_ENCRYPTION_KEY, AES.MODE_ECB)
    return cipher.encrypt(pkcs5_pad(data))

def timestamp():
    return int(round(time() * 1000))

def request_token(auth_token, timestamp):
    secret = "iEk21fuwZApXlz93750dmW22pw389dPwOk"
    pattern = "0001110111101110001111010101111011010001001110011000110001000110" 
    first = hashlib.sha256(secret + auth_token).hexdigest()
    second = hashlib.sha256(str(timestamp) + secret).hexdigest()
    bits = [first[i] if c == "0" else second[i] for i, c in enumerate(pattern)]
    return "".join(bits)

def static_token(timestamp):
    static = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"
    return request_token(static, timestamp)

def login(username, password):
    if not username or not password:
        return False

    t = timestamp()

    data = {
                'username': username,
                'timestamp': t,
                'req_token': static_token(t),
                'password': password
            }

    r = requests.post(URL + 'login', data=data, headers={"User-agent": None})

    if (r.status_code != 200):
        print 'Login HTTP post failed'
        return False

    return r.json()

def upload_img(username, auth_token, media_id, path):
    with open(path) as f:
        img_data = f.read()

    t = timestamp()
    data = {
        'username': username,
        'timestamp': t,
        'req_token': request_token(auth_token, t),
        'media_id': media_id,
        'type': 0, # 0 for image
    }

    r = requests.post(URL + 'upload', data=data, files={'data': encrypt(img_data)}, headers={"User-agent": None})

    return r

def send_img(username, auth_token, media_id, recipient):
    t = timestamp()
    data = {
        'username': username,
        'timestamp': t,
        'req_token': request_token(auth_token, t),
        'media_id': media_id,
        'recipient': recipient,
        'time': 5,
        'zipped': "0",
    }

    r = requests.post(URL + 'send', data=data, headers={"User-agent": None})

    return r

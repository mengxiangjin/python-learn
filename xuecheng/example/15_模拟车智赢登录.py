import base64
import hashlib
import random
import uuid

import requests
from Crypto.Cipher import DES3


def encodeMD5(pwd):
    m = hashlib.md5()
    m.update(pwd.encode('utf-8'))  # md5加密 必须为字节格式，可能会有盐
    return m.hexdigest()

def pad(text):
    return text + (8 - len(text) % 8) * chr(8 - len(text) % 8)

def des3(text,key,iv):
    plaintext = pad(text).encode("utf-8")
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    result = cipher.encrypt(plaintext)
    return base64.b64encode(result).decode("utf-8")

def get_udid():
    # "imei|当前时间|deviceId"  des加密  加密的key与iv通过反编译、hook 得知 iv = b'appapich',key=b'appapiche168comappapiche168comap'
    #deviceId 437665
    now_time = random.randint(5136066335773, 7136066335773)
    text = f'sssss|{now_time}|437665'
    return des3(text,b'appapiche168comappapiche168comap'[0:24], b'appapich')


# encode3Des 算法
def des3(data_string):
    BS = 8
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    # 3DES的MODE_CBC模式下只有前24位有意义
    key = b'appapiche168comappapiche168comap'[0:24]
    iv = b'appapich'

    plaintext = pad(data_string).encode("utf-8")

    # 使用MODE_CBC创建cipher
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    result = cipher.encrypt(plaintext)
    return base64.b64encode(result).decode('utf-8')


def get_sign(encrypt_pwd,udid,username):
    head = 'W@oC!AH_6Ew1f6%8'
    sb = f'{head}_appidatc.androidappversion3.27.0channelidcsypwd{encrypt_pwd}udid{udid}username{username}{head}'
    print(sb)
    return encodeMD5(sb).upper()

if __name__ == '__main__':
    username = "18953675221"
    pwd = "111111"

    url = 'https://dealercloudapi.che168.com/tradercloud/sealed/login/login.ashx'

    headers = {
        'User-Agent': 'okhttp/3.14.9'
    }

    imei = '846f63c5-777e-4ad3-82ec-158a98c4a637'  # 随机uuid
    nano_time = 5136066335778  # 开机时间
    device_id = '358908'  # 可以为空，也可以358908
    udid = des3(f"{imei}|{nano_time}|{device_id}")
    encrypt_pwd = encodeMD5(pwd)
    sign = get_sign(encrypt_pwd, udid,username)

    print(sign)

    data = {
        'username': username,
        '_appid': 'atc.android',
        'appversion': '3.27.0',
        'channelid': 'csy',
        'pwd': encrypt_pwd,
        'udid': udid,
        '_sign': sign
    }
    resp = requests.post(url, headers=headers,data=data,verify=False)
    print(resp.text)
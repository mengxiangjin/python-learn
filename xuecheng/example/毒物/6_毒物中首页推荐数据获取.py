import time
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import random


def create_android_id():
    data_list = []
    for i in range(1, 9):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return "".join(data_list).lower()


def md5(data_bytes):
    hash_object = hashlib.md5()
    hash_object.update(data_bytes)
    return hash_object.hexdigest()


def aes_encrypt(data_string):
    key = "d245a0ba8d678a61"
    aes = AES.new(
        key=key.encode('utf-8'),
        mode=AES.MODE_ECB,
    )
    raw = pad(data_string.encode('utf-8'), 16)
    return aes.encrypt(raw)


uid = create_android_id()
ctime = str(int(time.time() * 1000))

param_dict = {"loginToken": "", "platform": "android", "timestamp": ctime, "uuid": uid, "v": "4.74.5"}

ordered_string = "".join(["{}{}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])
aes_string = aes_encrypt(ordered_string)
aes_string = base64.encodebytes(aes_string)
aes_string = aes_string.replace(b"\n", b"")
sign = md5(aes_string)
param_dict['newSign'] = sign

res = requests.post(
    url="https://app.dewu.com/api/v1/app/user_core/users/getVisitorUserId",
    headers={
        "duuuid": uid,
        "duimei": "",
        "duplatform": "android",
        "appId": "duapp",
        "timestamp": ctime,
        'duv': '4.74.5',
        'duloginToken': '',
        'dudeviceTrait': 'Pixel+2+XL',
        'shumeiid': '202308011759568af1c8fc75c211e7f876664d9493202d0055aeeb3dd6e38c',
        'User-Agent': 'duapp/4.74.5(android;11)'

    },
    json=param_dict,
    verify=False
)
x_auth_token = res.headers['X-Auth-Token']

reply_param_dict = {
    "lastId": "1",
    "limit": "20",
    # "newSign": ""
}
import copy

new_dict = copy.deepcopy(reply_param_dict)
new_dict.update(
    # {"loginToken": "", "platform": "android", "timestamp": str(int(time.time() * 1000)), "uuid": uid, "v": "4.84.0"})
    {"loginToken": "", "platform": "android", "timestamp": str(int(time.time() * 1000)), "uuid": uid, "v": "4.74.5"})
ordered_string = "".join(["{}{}".format(key, new_dict[key]) for key in sorted(new_dict.keys())])

aes_string = aes_encrypt(ordered_string)
aes_string = base64.encodebytes(aes_string)
aes_string = aes_string.replace(b"\n", b"")
sign_string = md5(aes_string)
reply_param_dict['newSign'] = sign_string

res = requests.get(
    url="https://app.dewu.com/sns-rec/v1/recommend/all/feed/",
    params=reply_param_dict,
    headers={
        "X-Auth-Token": x_auth_token,
        'User-Agent': 'duapp/4.74.5(android;11)'
    },
    verify=False
)
print(res.text)
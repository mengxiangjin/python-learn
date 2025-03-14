import time
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus
import base64
import json
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
print(ordered_string)
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
print(res.headers)
x_auth_token = res.headers['X-Auth-Token']
print(x_auth_token)

# Bearer eyJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2OTcyMDY4NzQsImV4cCI6MTcyODc0Mjg3NCwiaXNzIjoiZDBmYWVjMzU5ZDdjOTAxMiIsInN1YiI6ImQwZmFlYzM1OWQ3YzkwMTIiLCJ1dWlkIjoiZDBmYWVjMzU5ZDdjOTAxMiIsInVzZXJJZCI6MjAxMjA0MDUzNiwiaXNHdWVzdCI6dHJ1ZX0.FHV-XOcmrNlS3dr4MxXEQpih9gwwIrYDHQMisL2y25yX66YGXHyb6SsJLnuf2QLUDJ-Vwg1XOuRc9je7g6V34tx_MOBn9v-lhR0ba9qySaL16r7kX4-eBRS2ewUXNuPJtI_F7dTCB83IB6vdjT6biP7dhuY0c4E1d-4hdhGw76RsNiBpA0hog5AvI8fe93LbeUiXVBxbq0bgEza4LWg0lBjKZuIpF7K48E-cUXD1dbiASDvYKKsncyK9sF6GvAj3-6W9A0ro1X3em68bG3BBDdzZXl_WGhbB3TQiMvIXqOatZLAiBJQekor8EiQW5OseIoyMzL7fbknkoN2E03MWuA

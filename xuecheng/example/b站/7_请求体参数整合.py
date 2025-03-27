import base64
import hashlib
import json
import re
import random
import string
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}
movie_url = "http://www.bilibili.com/video/BV1HC4y1v7gW/?spm_id_from=333.337.search-card.all.click"


# aid,cid对应视频
def get_aid_cid():
    res = requests.get(movie_url,
                       verify=False, headers=headers)
    data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', res.text)
    data_dict = json.loads(data_list[0])

    aid = data_dict['aid']
    cid = data_dict['videoData']['cid']
    print(f'aid:{aid}')
    print(f'cid:{cid}')
    return aid, cid


def base64_encrypt(data_string):
    data_bytes = bytearray(data_string.encode('utf-8'))
    data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
    for i in range(1, len(data_bytes)):
        data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
    res = base64.encodebytes(bytes(data_bytes))
    return res.strip().strip(b"==").decode('utf-8')

def create_random_mac(sep=":"):
    """ 随机生成mac地址 """
    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
    return mac

def gen_sn():
    return "".join(random.sample("123456789" + string.ascii_lowercase, 10))


def get_sign_value(params,salt):
    obj = hashlib.sha256()
    obj.update(params.encode('utf-8'))
    obj.update(salt.encode('utf-8'))
    return obj.hexdigest()


def aes_encrypt(data_string,key,iv):
    aes = AES.new(
        key=key.encode('utf-8'),
        mode=AES.MODE_CBC,
        iv = iv.encode('utf-8'),
        #可能有iv
    )
    raw = pad(data_string.encode('utf-8'), 16)
    # return aes.encrypt(raw)
    return [hex(item)[2:] for item in aes.encrypt(raw)] #返回的是一个列表，十六进制


# 拿到请求体内容
def get_request_body(params,key,iv):
    res = aes_encrypt(params,key,iv)
    print(res)
    pass

if __name__ == '__main__':
    aid,cid = get_aid_cid()
    mac_string = create_random_mac(sep="")
    sn = gen_sn()
    prev_did = "{}|||{}".format(mac_string, sn)
    did = base64_encrypt(prev_did)
    print(f'did:{did}')

    data = {
        "aid": aid,
        "cid": cid,
        "did": did,
        "auto_play": "0",
        "build": "6240300",
        "epid": "",
        "from_spmid": "search.search-result.0.0",
        "ftime": str(int(time.time() - random.randint(100, 5000))),
        "lv": "0",
        "mid": "0",
        "mobi_app": "android",
        "part": "1",
        "sid": "0",
        "spmid": "main.ugc-video-detail.0.0",
        "stime": str(int(time.time())),
        "sub_type": "0",
        "type": "3"
    }
    sb = "&".join([f'{key}={data[key]}' for key in sorted(data)])
    print(sb)
    sign_value = get_sign_value(sb, "9cafa6466a028bfb")
    sb = sb + f'&sign={sign_value}'
    print(f'sign:{sign_value}')
    print(sb)
    get_request_body(sb,"fd6b639dbcff0c2a1b03b389ec763c4b","77b07a672d57d64c")
    pass
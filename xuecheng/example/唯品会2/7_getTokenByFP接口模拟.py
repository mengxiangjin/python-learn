import random
import time
import uuid
from base64 import b64encode
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
from urllib.parse import quote_plus
import requests
import hashlib

requests.packages.urllib3.disable_warnings()  # https 会有红色警告，去掉

# ====================== 注册设备 ======================
mars_cid = device_token = str(uuid.uuid4())
android_id = ''.join(["%x" % random.randint(1, 15) for i in range(16)])
build_model = "Pixel 2 XL"
ctime = str(int(time.time()))


def sha1(data_string):
    # sha1加密
    hash_object = hashlib.sha1()
    hash_object.update(data_string.encode('utf-8'))
    arg7 = hash_object.hexdigest()
    return arg7

device_token = str(uuid.uuid4())
param_dict = {
    'app_name': 'achievo_ad',
    'app_version': '7.83.3',
    'device_token': device_token,
    'status': 1,
    'warehouse': 'null',
    'manufacturer': 'Google',
    'device': build_model,
    'os_version': '30',
    'channel': 'oziq7dxw:::',
    'vipruid': '',
    'regPlat': '0',
    'regid': '',
    'rom': 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)',
    'skey': '6692c461c3810ab150c9a980d0c275ec',

}

ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])

salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{ordered_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.get(
    url="https://mp.appvipshop.com/apns/device_reg",
    params=param_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },verify=False
)
print("1.注册设备", res.text)


# ====================== getTokenByFP ======================
res = requests.get(
    url="https://vcsp-api.vip.com/token/getTokenByFP?vcspKey=4d9e524ad536c03ff203787cf0dfcd29",
    headers={
        "vcspauthorization": "vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387"
    },verify=False
)

print(res.text)
vsp_dict = res.json()['data']

# ====================== generate_token ======================

dinfo = '{"ah1":"","ah2":"","ah3":"","ah4":"wifi","ah5":"1080_2189","ah6":1804800,"ah7":8,"ah8":7742595072,"ah9":"%s","ah10":"","ah11":"","ah12":"","ah13":"","as1":"10","as2":"","as3":"","as4":"%s","as5":"","as6":"","as7":"29","ac1":"%s"}' % (
    build_model, android_id, device_token)

data_dict = {
    "app_name": "shop_android",
    "app_version": "7.83.3",
    "client_type": "android",
    "dinfo": quote_plus(dinfo),
    "mars_cid": mars_cid,
    "phone_model": build_model,
    "session_id": "{}_shop_android_{}".format(mars_cid, ctime),
    "sys_version": "29",
    "vcspKey": "4d9e524ad536c03ff203787cf0dfcd29",
    "vcspToken": vsp_dict['vcspToken']
}

data = "&".join(["{}={}".format(key, data_dict[key]) for key in sorted(data_dict.keys())])
iv = ''.join(["%x" % random.randint(1, 15) for i in range(16)])

obj = hashlib.md5()
obj.update(b'aee4c425dbb2288b80c71347cc37d04b')
key = obj.digest()

aes = AES.new(
    key=key,
    mode=AES.MODE_CBC,
    iv=iv.encode('utf-8')
)
raw = pad(data.encode('utf-8'), 16)
encrypt_bytes = aes.encrypt(raw)
total_bytes = iv.encode('utf-8') + encrypt_bytes
edata = b64encode(total_bytes).decode('utf-8')

body_dict = {
    'api_key': "23e7f28019e8407b98b84cd05b5aef2c",
    'did': "",
    'edata': edata,
    'eversion': "0",
    'skey': "6692c461c3810ab150c9a980d0c275ec",
    'timestamp': int(time.time())
}

body_string = "&".join(["{}={}".format(key, body_dict[key]) for key in sorted(body_dict.keys())])
# print(body_string)
salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{body_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.post(
    url="https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token",
    data=body_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },
    verify=False
)
print("3.token", res.text)
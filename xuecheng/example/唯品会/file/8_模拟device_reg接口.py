import requests
import uuid

import hashlib


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
    'device': 'Pixel 2 XL',
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
    # headers={
    #     "Authorization": "OAuth api_sign={}".format(api_sign)
    # },
    verify=False
)
print(res.text)
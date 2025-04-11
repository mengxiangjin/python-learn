import time
import requests
import base64
import hashlib
import hmac
from urllib.parse import quote_plus
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_v1_5, AES
from base64 import b64encode


def sign(g7timestamp):
    key = "1KMrg0dfufc0wpnXEJacEQX1YEUYA0Ja"
    message = """POST
    {}
    /inside.php""".format(g7timestamp)
    message = message.encode('utf-8')
    key = key.encode('utf-8')
    result = hmac.new(key, message, hashlib.sha1).digest()
    _sig = base64.b64encode(result).decode()
    return quote_plus(_sig)


def encrypt(data_string):
    def c(data_text):
        array = "0123456789ABCDEF"
        data_list = []
        for b in data_text.encode('utf-8'):
            data_list.append(array[(b & 240) >> 4])
            data_list.append(array[b & 15])
        return "".join(data_list)

    rsa_pub_key = """-----BEGIN PUBLIC KEY-----
    MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsAwGz+E7PEppCUWrM46wf9Sj2Zv+dlSIjwGtMoG9iG36HFYy0BC+uAgNDun0joo4UFW0qejyc2ExjFXBRiYENnseY3jb9qI0c3thAj2qd5iofGCWaRO1DA707xwD7MOjvHur7c7nvBNv+vwWFvMDiZzj4JqaaV8ZNTT2oO9+aJQIDAQAB
    -----END PUBLIC KEY-----"""
    key = RSA.importKey(rsa_pub_key)
    cipher = PKCS1_v1_5.new(key)
    encrypt_bytes = cipher.encrypt(data_string.encode('utf-8'))
    cipher_text = b64encode(encrypt_bytes).decode('utf-8')
    cipher_text = cipher_text.replace(r"\n", "")
    result = c(cipher_text)
    print(result)
    return result


def run():
    g7timestamp = str(int(time.time() * 1000))

    mobile = "18953675221"
    password = "lqz12345"

    param_dict = {
        "t": "json",
        "m": "mobileinfo",
        "f": "driverLogin",
        "g7timestamp": g7timestamp,
        "app": "1",
        "ua": "android",
        "appclientversion": "4.1",
        "referer": "d507c00281c733bd693e5049ea33ad7e", # 固定的
        "sign": sign(g7timestamp)
    }

    body_dict = {
        "mobile": encrypt(mobile),
        "password": encrypt(password),
        "equipment": "google"
    }

    res = requests.post(
        url="https://g7s.ucenter.huoyunren.com/inside.php",
        params=param_dict,
        data=body_dict,
        verify=False
    )
    print(res.json())


if __name__ == '__main__':
    run()
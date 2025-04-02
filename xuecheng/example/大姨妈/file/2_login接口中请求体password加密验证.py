import base64
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def md_5(data):
    md5 = hashlib.md5()
    md5.update(data.encode('utf-8'))
    res = md5.hexdigest()
    return res

def encrypt(password,phone,salt):
    obj = AES.new(key=phone.encode('utf-8'), mode=AES.MODE_CBC, iv=salt.encode('utf-8'))
    raw = pad(password.encode('utf-8'), 16)
    res = obj.encrypt(raw)
    base64_str = base64.b64encode(res)
    return base64_str.decode('utf-8')


if __name__ == '__main__':
    pas = 'zj123456'
    phone = '15655549539'
    password = encrypt(pas,md_5(phone)[:16].lower(),'yoloho_dayima!%_')
    print(password)

# P0H0qk3BfiiBrKZ1WUVGFQ==
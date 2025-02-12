import hashlib
import time
import requests


def get_md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()  # 16进制字符串

if __name__ == '__main__':
    username = input('输入用户名：')
    password = input('输入密码：')
    password = get_md5(password)
    sign = get_md5(f'{username}jin')

    datas = {
        "username": username,
        "password": password,
        "sign": sign
    }

    current_time =(str)((int) (time.time()))
    header_sign = get_md5(current_time)
    headers = {
        'Ctime': current_time,
        'sign': header_sign
    }
    resp = requests.post('http://192.168.2.206:8080/login', data=datas,verify=False,headers=headers)
    print(resp.json())
    pass
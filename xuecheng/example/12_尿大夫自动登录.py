import hashlib
import time

import requests


def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

def get_sign():
    current_time = int(time.time())
    sign_1 = md5(f'niaodaifu{current_time}')[12:30]
    sign_2 = md5(f'android{current_time}')[12:26]
    return sign_1 + sign_2



if __name__ == '__main__':
    # phone = input('请输入手机号：')
    # password = input('请输入密码：')
    phone = '18953675221'
    password = 'lqz12345'
    sign = get_sign()

    current_time = int(time.time())
    data = {
        'password': 'lqz12345',
        'mobile': '18953675221',
        'channel': 'android',
        'sign': sign,
        'time': current_time,
        'mechanism': 0,
        'platform': 1
    }

    url = 'https://api.niaodaifu.cn/v4/site/loginnew'
    res = requests.post(url,data = data,verify=False)
    print(res.json())

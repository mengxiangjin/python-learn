import uuid

import requests

if __name__ == '__main__':
    url = 'https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm'
    appkey = deviceIdentify = uuid.uuid1()
    username = input('请输入账号：')
    password = input('请输入密码：')
    data = {
        "appkey": appkey,
        'appVersion': '9.0.30',
        'areaId': '3404',
        'channelCode': '0',
        'cpsId': 'xiaomi',
        'deviceIdentify': deviceIdentify,
        'deviceType': 'ANDROID',
        'deviceTypeExtra': '0',
        'equipmentType': 'Pixel 2 XL',
        'lati': '31.837927',
        'longi': '117.13491',
        'netEnv': 'wifi',
        'passWord': password,
        'pushToken': 'Aow1dlRUja87IAUSbyWppAZkWSZxT9-rRCjEUXpbY_yU',
        'screenReslolution': '1440x2712',
        'supportWebp': '1',
        'sysVersion': '11',
        'userName': username
    }
    resp = requests.post(url, data=data,verify=False)
    print(resp.json())

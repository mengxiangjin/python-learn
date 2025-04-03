import uuid

import requests

if __name__ == '__main__':
    url = 'https://newappuser.jiuxian.com/messages/mobileCode.htm'
    appkey = deviceIdentify = uuid.uuid1()
    username = input('请输入账号：')
    code = input('请输入验证码：')
    params = {
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
        'code': code,
        'mobile': username,
        'netEnv': 'wifi',
        'pushToken': 'Aow1dlRUja87IAUSbyWppAZkWSZxT9-rRCjEUXpbY_yU',
        'screenReslolution': '1440x2712',
        'supportWebp': '1',
        'sysVersion': '11',
        'type': '3'
    }
    headers = {
        "secure": "false",
        'user-agent': "okhttp/3.14.9",
        'Connection': "keep-alive"
    }

    app_key = device_identify = uuid.uuid1()
    resp = requests.get(
        url = url,
        params=params,
        headers=headers,
        verify=False
    )
    print(resp.json())

        
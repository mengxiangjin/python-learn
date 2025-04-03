import base64
import uuid
import requests
import ddddocr
import cv2
import numpy as np

if __name__ == '__main__':
    url = 'https://newappuser.jiuxian.com/messages/graphCode.htm'
    appkey = deviceIdentify = uuid.uuid1()
    username = input('请输入账号：')
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
        'mobie': username,
        'netEnv': 'wifi',
        'pushToken': 'Aow1dlRUja87IAUSbyWppAZkWSZxT9-rRCjEUXpbY_yU',
        'screenReslolution': '1440x2712',
        'supportWebp': '1',
        'sysVersion': '11',
        'type': '5'
    }
    headers = {
        "secure": "false",
        'user-agent': "okhttp/3.14.9",
        'Connection': "keep-alive"
    }

    app_key = device_identify = uuid.uuid1()
    resp = requests.get(
        url=url,
        params=params,
        headers=headers,
        verify=False
    )
    status = resp.json()['success']
    if status == '1':
        print("验证码获取成功")
        image_str = resp.json()['result']["imgCode"]
        print(image_str)
        base64_str = base64.b64decode(image_str)
        with open('验证码.png', 'wb') as f:
            f.write(base64_str)
        ocr = ddddocr.DdddOcr()
        code = ocr.classification(base64_str)
        print(code)

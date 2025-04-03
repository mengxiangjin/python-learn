import time
import uuid
import requests
import base64
import ddddocr

def fetch_image_code(mobile, app_key, device_identify):
    res = requests.get(
        url="https://newappuser.jiuxian.com/messages/graphCode.htm",
        params={
            "appKey": app_key,
            "appVersion": "9.0.30",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "type": "4"
        },
        headers={
            "secure": "false",
            'user-agent': "okhttp/3.14.9",
            'Connection': "keep-alive"
        },
        verify=False
    )

    image_str = res.json()['result']["imgCode"]

    img = base64.b64decode(image_str)

    with open('验证码.png', 'wb') as f:
        f.write(img)

    ocr = ddddocr.DdddOcr(show_ad=False)
    code = ocr.classification(img)
    return code

def check_image_code(mobile, code, app_key, device_identify):
    res = requests.get(
        url='https://newappuser.jiuxian.com/messages/mobileCode.htm',
        params={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "code": code,
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "type": "1"
        },
        verify=False
    )
    data_dict = res.json()

    # {'result': '', 'errCode': '', 'success': '1', 'errMsg': ''}
    # {'result': '', 'errCode': '1200013', 'success': '0', 'errMsg': '验证码输入错误'}
    # print(data_dict)
    return data_dict.get('success') == "1"

def start_login(username,yzm_code,appkey,deviceIdentify):
    url = 'https://newappuser.jiuxian.com/user/loginMobileFast.htm'
    headers = {
        "secure": "false",
        'user-agent': "okhttp/3.14.9",
        'Connection': "keep-alive"
    }
    datas = {
        "appkey": appkey,
        'appVersion': '9.0.30',
        'areaId': '3404',
        'channelCode': '0',
        'cpsId': 'xiaomi',
        'deviceIdentify': deviceIdentify,
        'deviceType': 'ANDROID',
        'deviceTypeExtra': '0',
        'equipmentType': 'Pixel 2 XL',
        'mobile': username,
        'lati': '31.837927',
        'longi': '117.13491',
        'netEnv': 'wifi',
        'pushToken': 'Aow1dlRUja87IAUSbyWppAZkWSZxT9-rRCjEUXpbY_yU',
        'screenReslolution': '1440x2712',
        'supportWebp': '1',
        'sysVersion': '11',
        'verifyCode': yzm_code
    }
    resp = requests.post(
        url=url,
        headers=headers,
        data=datas,
        verify=False
    )
    return resp.json()

if __name__ == '__main__':
    username = input('请输入账号：')
    appkey = deviceIdentify = uuid.uuid1()
    while True:
        res_code = fetch_image_code(username,appkey,deviceIdentify)
        print("识别的code：",res_code)
        if res_code == '':
            continue
        res = check_image_code(username,res_code,appkey,deviceIdentify)
        if res:
            break
    yzm_code = input('请输入验证码：')
    res_json = start_login(username,yzm_code,appkey,deviceIdentify)
    print(res_json)

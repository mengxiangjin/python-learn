import hashlib
import time

import requests
import execjs
import time
import re
import os


brand_id = 'ab0b98137b57439fbdeee594e386079c'
sign_key = 'jGZH2Yf77YHpcyeZ'


def get_video_sign(video_page):
    now_time = int(time.time())
    encrypt_data = f'/live/live/video/anchor/{video_page}/10-{now_time}-{brand_id}-0-{sign_key}'
    encrypt_res = encrypt(encrypt_data, 32)
    sign = f'{now_time}-{brand_id}-0-{encrypt_res}'
    print("get_video_sign --->", sign)
    return sign


def get_follow_sign(followPage):
    now_time = int(time.time())
    encrypt_data = f'/user/follow/followlist/{followPage}/10-{now_time}-{brand_id}-0-{sign_key}'
    encrypt_res = encrypt(encrypt_data, 32)
    sign = f'{now_time}-{brand_id}-0-{encrypt_res}'
    print("get_follow_sign --->", sign)
    return sign


def get_token_sign():
    now_time = int(time.time())
    encrypt_data = f'/oauth/oauth/login-{now_time}-{brand_id}-0-{sign_key}'
    encrypt_res = encrypt(encrypt_data, 32)
    sign = f'{now_time}-{brand_id}-0-{encrypt_res}'
    print("get_token_sign --->", sign)
    return sign


# 基本固定
def get_request_headers():
    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'token': 'aiya_e9e8e51c-e254-4d32-9dd0-e7fb95d058d989',  #重要
        'appversion': '{"uid":"218904","systemModel":"Pixel 2 XL","appType":"1","appVer":"3.9.3","phoneBrand":"google","version":"3.9.3","deviceId":"63bd2e866c6ef324","systemVersion":"11","versionCode":"20250729"}',
        'versionname': '3.9.3',
        'versioncode': '20250729',
        'clienttype': 'Android',
        'Referer': 'https://proapi.taolu.cloud'
    }
    return headers


#固定的请求参数
def get_request_params(anchorUserId,current_page):
    params = {
        'uid': '218904',
        'systemModel': 'Pixel 2 XL',
        'appType': '1',
        'appVer': '3.9.3',
        'phoneBrand': 'google',
        'version': '3.9.3',
        'deviceId': '63bd2e866c6ef324',
        'systemVersion': '11',
        'versionCode': '20250729',
        'anchorUserId': anchorUserId,
        'sign': get_video_sign(current_page)
    }
    return params


def encrypt(input_str: str, length: int = 32):
    try:
        md5_hex = hashlib.md5(input_str.encode('utf-8')).hexdigest()
        if length == 16:
            return md5_hex[8:24]  # 取16位
        else:
            return md5_hex  # 返回32位
    except Exception as e:
        print(f"加密错误: {e}")
        return None

def get_login_token():
    url = 'https://proapi.taolu.cloud/oauth/oauth/login'
    json_data = {
        'password': 'zj1435145737',
        'userName': '15655549539',
        'verifyCode': ''
    }

    params = {
        'uid': '218904',
        'appType': '1',
        'appVer': '3.9.3',
        'phoneBrand': 'google',
        'version': '3.9.3',
        'deviceId': '63bd2e866c6ef324',
        'systemVersion': '11',
        'versionCode': '20250729',
        'systemModel': 'Pixel 2 XL',
        'sign': get_token_sign()
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'appversion': '{"uid":"218904","systemModel":"Pixel 2 XL","appType":"1","appVer":"3.9.3","phoneBrand":"google","version":"3.9.3","deviceId":"63bd2e866c6ef324","systemVersion":"11","versionCode":"20250729"}',
        'versionname': '3.9.3',
        'versioncode': '20250729',
        'clienttype': 'Android',
        'Referer': 'https://proapi.taolu.cloud'
    }

    resp = requests.post(url, headers=headers, params=params, json=json_data)
    print(f'返回的数据--->{resp.json()}')


def write_yuan():

    # 文件夹路径
    folder_path = r"G:\缘彼S大大"

    # 获取文件夹下所有文件和文件夹的名称
    try:
        all_items = os.listdir(folder_path)

        # 过滤出只是文件（不包括子文件夹）
        files_only = [item for item in all_items
                      if os.path.isfile(os.path.join(folder_path, item))]

        # 写入到result.txt文件中
        with open("result.txt", "w", encoding="utf-8") as f:
            for filename in files_only:
                f.write(filename + "\n")

        print(f"成功输出 {len(files_only)} 个文件名到 result.txt")

    except FileNotFoundError:
        print(f"错误：找不到文件夹 {folder_path}")
    except PermissionError:
        print(f"错误：没有权限访问文件夹 {folder_path}")
    except Exception as e:
        print(f"发生错误：{e}")

# 使用示例
if __name__ == "__main__":
    get_follow_sign(10)
    get_video_sign(1)
    write_yuan()
    # get_login_token()


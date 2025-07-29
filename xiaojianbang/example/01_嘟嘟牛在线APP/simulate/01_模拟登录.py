import json
import time

import requests

from xiaojianbang.tools.Utils import Utils


#实际就是POST请求中添加Encrypt参数
#   1.根据已知的Map参数添加sign键值对
#   2.map[sign]值是原map中的键值对进行拼接后通过MD5加密后得到的字符串
#   3.map内容转为JSON格式字符串，通过DES加密（Des的key值为固定值经过MD5加密后取前8个字节）后、然后Base64编码成字符串
#   4.得到的字符串即为Encrypt值
#   5.Base64解码resp.text后DES解密即为真正的toast信息
def get_encrypt(datas):
    key = '65102933'
    iv = '32028092'

    #key用md5加密取了前八个字节作为des加密的key
    des_key = Utils.MD5_BYTE(key)[:8]
    res = Utils.DES_ENCRYPT(datas, des_key, iv)
    print(res)
    return Utils.base64_to_str(res)


def decrypt(text):
    key = '65102933'
    iv = '32028092'

    # key用md5加密取了前八个字节作为des加密的key
    des_key = Utils.MD5_BYTE(key)[:8]

    text = Utils.base64_decode(text)
    res_json = Utils.DES_DECRYPT(text, des_key, iv)
    return res_json


def get_data(para):
    list_items = [f'{key}={para[key]}' for key in list(para.keys())]
    list_items.sort()
    result = '&'.join(list_items)
    result = f'{result}&key=sdlkjsdljf0j2fsjk'

    #构造字符串用来MD5加密生成sign
    sign = get_sign(result)
    print(f'sign值：{sign}')

    #sign加入到原map中，排序后转为json字符串返回
    para['sign'] = sign
    new_para = dict(sorted(para.items()))
    res = json.dumps(new_para, ensure_ascii=False)
    return res


#获取签名
def get_sign(result):
    res = Utils.MD5_HEX(result)
    return str(res).upper()


if __name__ == '__main__':
    phone_number = input('请输入手机号码：')
    password = input('请输入密码：')

    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)',
        'Content-Type': 'application/json; charset=utf-8'
    }

    login_url = 'http://api.dodovip.com/api/user/login'

    current_time_millis = int(time.time() * 1000)

    para = {
        'username': phone_number,
        'userPwd': password,
        'equtype': 'ANDROID',
        'loginImei': 'Androidnull',
        'timeStamp': f'{current_time_millis}'
    }
    json_str = get_data(para)
    print(f'json_str值：{json_str}')
    encrypt = get_encrypt(json_str)
    print(f'encrypt值：{encrypt}')

    body = {
        'Encrypt': encrypt
    }
    resp = requests.post(url=login_url, headers=headers, json=body)
    print(resp.text)
    #需要解密
    result = decrypt(resp.text)
    print(result)

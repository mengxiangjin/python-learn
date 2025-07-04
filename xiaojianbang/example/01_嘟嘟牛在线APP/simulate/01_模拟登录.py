import json
import time
from xuecheng.encryption.Utils import Utils



def get_encrypt(datas):
    key = '65102933'
    iv = '32028092'
    des_key = Utils.MD5(key)
    print(des_key)
    pass

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
    res = json.dumps(new_para,ensure_ascii=False)
    return res


#获取签名
def get_sign(result):
    res = Utils.MD5(result)
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




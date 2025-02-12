import requests
import utils

# 1 发送验证码
phone = input('请输入手机号：')
imei = utils.gen_imei()
data = {"phone": "%s" % phone}
headers = {
    'user-agent': 'chuangqi.o.137.com.iqilu.app137/0.0.28.108',
    'orgid': '137',
    'cq-agent': '{"os":"android","imei":"%s","osversion":"11","network":"none","version":"0.0.28.108","core":"1.6.4"}' % imei,
    'Cookie': 'orgid=137',
}
res = requests.post('https://app-auth.iqilu.com/member/phonecode', json=data, verify=False, headers=headers)
res_data = res.json()['data']

# 2 验证码登录-=====》接码平台
code = input('请输入手机收到的验证码：')
data = {
    "phone": "%s" % phone,
    "code": "%s" % code,
    "key": res_data,  # 上一次发送手机验证码接口返回的那个data base64编码
    "password": "",
    "captcha": "",
    "captchaKey": ""
}
res = requests.post('https://app-auth.iqilu.com/member/login', json=data, verify=False, headers=headers)

print(res.text)

import requests
import utils

phone = input('请输入手机号：')
data = {"phone": "%s" % phone}
headers = {
    'user-agent': 'chuangqi.o.137.com.iqilu.app137/0.0.28.108',
    'orgid': '137',
    'cq-agent': '{"os":"android","imei":"%s","osversion":"11","network":"none","version":"0.0.28.108","core":"1.6.4"}' % utils.gen_imei(),
    'Cookie': 'orgid=137',
}
res = requests.post('https://app-auth.iqilu.com/member/phonecode', json=data, verify=False, headers=headers)
print(res.text)

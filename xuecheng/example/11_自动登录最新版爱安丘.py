import requests
from utils import gen_imei,header_str_to_dict,encrypt_data

session = requests.session()
imei = gen_imei()   # 随机生成imei
header_s = '''
encrypt	1
orgid	137
User-Agent	null chuangqi.o.137.com.iqilu.app137/1.0.5
platform	android
imei	d2b63fe7dd79f8bc
CQ-AGENT	{"os":"android","brand":"google","imei":"%s","osversion":"11","network":"wifi","version":"1.0.5","core":"2.2.1.1"}
cq-token	
Content-Type	application/json; charset=UTF-8
Host	app-auth.iqilu.com
Accept-Encoding	gzip
Cookie	orgid=137; redirectToken=18806862d60c48bd9842e6dc2327372a-87343990; redirect=
Content-Length	93
Connection	keep-alive
'''
header = header_str_to_dict(header_s)
phone = input('请输入手机号：')
password = input('请输入密码：')

password = encrypt_data(password)
data = {"codeKey": "", "password": password, "code": "", "phone": phone, "key": ""}

#json=data 与data=data区别：data= 会自动设置为 application/x-www-form-urlencoded。
#json= 会自动设置为 application/json。
res = session.post('https://app-auth.iqilu.com/member/login?e=1', headers=header, json=data, verify=False)
print(res.text)

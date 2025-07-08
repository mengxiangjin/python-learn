import requests, json
import execjs

import _locale
_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'utf8'])

f = open('demo.js', 'r')
demo_list = f.readlines()
print(list(range(0, len(demo_list))))
jscode = ""
for i in range(0, len(demo_list)):
    jscode += demo_list[i]
f.close()

js = execjs.compile(jscode)
cipherText = js.call('encrypt', '15968079477', 'a12345678')
print(cipherText)

url = 'http://api.dodovip.com/api/user/login'
data = json.dumps({"Encrypt": cipherText})
headers = {
    "content-type": "application/json; charset=utf-8",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Pixel Build/QP1A.191005.007.A3)"
}
r = requests.post(url=url, data=data, headers=headers)
print(r)
print(r.text)
print(type(r.text))
print(r.content)

cipherText = js.call('decrypt', r.text)
print(cipherText)

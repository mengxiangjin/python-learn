import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'Mobile-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjcxMTMyMDA2MDczNjA2MTQ1IiwiZXhwIjoxNjkyMzcwOTk2LCJpYXQiOjE2OTIzNjczOTYsInVzZXJJZCI6IjE2NzExMzIwMDYwNzM2MDYxNDUiLCJ1c2VybmFtZSI6IjE3NzE3ODIzMjQ0In0.EvemzUvZPHr2eF4AERxQeLhZfUW1H6Gvbn-xnxgmpn4', # 登录成功返回的token
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)'
}

data = {
    "cityNo": "",
    "keyword": "石榴",
    "limit": 10,
    "orderByContent": "",
    "page": 1,
    "enabled": 1
}

res = requests.post('https://miappshop.jshulin.com/pro/searchByPage', json=data, verify=False, headers=headers)
print(res.text)

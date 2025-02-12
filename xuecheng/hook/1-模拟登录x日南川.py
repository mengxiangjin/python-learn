import requests

data = {
    'appId': '32',
    'hashSign': '5cbcd0d5aa6e8c465c9eda4c178e467e',
    'imgUrl': '',
    'lat': '29.568295',
    'lng': '106.559123',
    'loginName': '18956875221',
    'nickName': '',
    'openId': '',
    'place': '重庆',
    'pwd': '734f7fb5e505a3dd35c29d3af4795c79',
    'sessionId': '1cda109e-a35b-46c0-9161-21f3dd67ad63',
    'token': '',
    'type': '',
}
# 发送请求，发现返回 ：感谢您的反馈，应用防火墙会尽快进行分析和确认
# 说明模拟的不像
# 请求地址，请求体都是了---》请求头：
headers = {
    'sessionid': '1cda109e-a35b-46c0-9161-21f3dd67ad63',
    'token': '',
    't': '1692190592030',
    'sign': 'a7da03d417519e1a059de13c4747eeea',
    'cqlivingappclienttype': '1',
    'cqlivingappclientversion': '2031',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.10.0',  # 必须带的
    'content-length': '236',
    'content-type': 'application/x-www-form-urlencoded'
}
res = requests.post('https://api.cqliving.com/login.html', data=data, verify=False, headers=headers)
print(res.text)

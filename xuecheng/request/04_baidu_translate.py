import json

import requests

#百度翻译
if __name__ == '__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    data = {
        'from': 'en',
        'query': 'luck',
        'source': 'txt',
        'to': 'zh'
    }

    url = 'https://fanyi.baidu.com/transapi'
    resp = requests.post(url,headers=headers,data=data)
    json_data = resp.json()
    print(json_data)
    print(json.loads(json_data['result'])['content'][0])

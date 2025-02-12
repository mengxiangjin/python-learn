import requests

if __name__ == '__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'key': 'value'
    }
    datas = {
        'test': 'one'
    }
    url = 'http://www.baidu.com'
    resp = requests.get(url,headers=headers,data=datas)
    print(resp.request.headers)
    print(resp.request.url)
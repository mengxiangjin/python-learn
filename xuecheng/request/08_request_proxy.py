import requests

if __name__ == '__main__':
    proxy = {
        'http': 'http://47.102.185.210:8091',
        'https': 'http://47.102.185.210:8091',
    }
    resp = requests.get('http://httpbin.org/ip', proxies=proxy)
    print(resp.text)
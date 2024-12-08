import requests


url = 'https://movie.douban.com/j/chart/top_list'
params = {
    'type' : 24,
    'interval_id' : '100:90',
    'action': '',
    'start' : 20,
    'limit' : 20
}

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

resp = requests.get(url,params=params,verify=False,headers=headers)
print(resp.json())
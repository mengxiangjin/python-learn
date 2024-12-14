import json

import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = 'https://blog.csdn.net/a497785609/article/details/45308817'


    header = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        # 'Referer': 'https://blog.csdn.net/a497785609/article/details/45308817'
    }
    r = requests.get(url,headers=header)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    target = soup.find('span',attrs= {
        'style': 'font-size:10px'
    })
    str_str = target.string.replace('\n','').replace('\r','').replace('\t','').replace('\r','').replace('\\','')

    print(str_str[str_str.index('['):])
    with open('new_city.json', 'w', encoding='utf-8') as f:
        json.dump(str_str[str_str.index('['):], f, ensure_ascii=False)

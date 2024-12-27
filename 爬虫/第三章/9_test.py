import json
import time

import requests
from bs4 import BeautifulSoup


#https://www.nowmsg.com/findzip/cn_youbian_2022.asp?pid0=110000000000

list = []

def test(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.find('tbody').find_all('tr')
    for tr in trs:
        a = tr.find('a')
        data = {
            'name': a.string,
            'code': tr.find_all('td')[2].string
        }
        list.append(data)
    with open('test.json', 'w', encoding='utf-8') as f:
        json.dump(list, f, ensure_ascii=False)

if __name__ == '__main__':
    url = 'https://www.nowmsg.com/findzip/cn_youbian_2022.asp'
    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    target = soup.find('div',attrs={'class':'well col-xs-12 col-sm-12'})
    target_list = target.find_all('a',attrs={})
    for target in target_list:
        real_url = url + '?' + str(target.get('href')).split('?')[-1]
        print(real_url)
        test(real_url)
        time.sleep(1)

    response.close()
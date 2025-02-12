import requests

from lxml import etree

#金投网数据
if __name__=='__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    url = 'https://cang.cngold.org/c/2022-06-14/c8152503.html'
    resp = requests.get(url,headers=headers)
    resp.encoding = 'utf-8'

    tree = etree.HTML(resp.text)
    tbody = tree.xpath('//table[@border="1"]/tbody/tr')[1:]
    for tr in tbody:
        print(tr.xpath('./td/text()'))

import requests
from lxml import etree

#豆瓣top250电影信息
if __name__ == '__main__':
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        "cookie": "bid=5vStbboxJiA; _ga=GA1.1.1864941792.1708510577; __utmv=30149280.27849; douban-fav-remind=1; _ga_RXNMP372GL=GS1.1.1709112405.3.0.1709112405.60.0.0; viewed=\"4836697_35301417\"; ll=\"118183\"; _pk_id.100001.4cf6=88f6d0eb1ffb590a.1730190180.; dbcl2=\"278463150:FufdaptAQ9k\"; push_noty_num=0; push_doumail_num=0; ck=rCuF; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1736819158%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DvcwEfgt4bRE2qIyahCe9ScuBGCKRQo0Yn3JaBIHjXgbwe2urIt5VL75jPkxS3_KmIa3i66KMkj_154h_Lvd5jqNg1OqTFPLpTCX8oNvhZLPG8VL-S8JGvlDjVj4fBWC7MMTLyU51kn1HdZmtY4_QHXCkv1z5mC8P1psegXfsyj_%26wd%3D%26eqid%3Db511fa7a001ffb05000000066780e9f3%22%5D; _pk_ses.100001.4cf6=1; __utma=30149280.1864941792.1708510577.1718862695.1736819158.3; __utmb=30149280.0.10.1736819158; __utmc=30149280; __utmz=30149280.1736819158.3.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.1864941792.1708510577.1736819158.1736819158.1; __utmb=223695111.0.10.1736819158; __utmc=223695111; __utmz=223695111.1736819158.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ap_v=0,6.0; __yadk_uid=zYb2ezW6bKofMqPxv5YyujULQ8SXAvkw"
    }

    url = 'https://movie.douban.com/top250'

    start = 0
    while start < 250:
        page_url = f'{url}?start={str(start)}&filter='
        response = requests.get(page_url,headers=headers)
        root_tree = etree.HTML(response.text)
        item_list = root_tree.xpath('//div[@class="item"]')
        for item in item_list:
            print(item.xpath('./div/a/img/@src')[0])
            print(str.join("",item.xpath('./div[@class="info"]//text()')).replace('\n','').replace(' ',''))
        start += 25

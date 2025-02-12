import time
import re
import requests
from lxml import etree

#获取各章节
def get_chapter(title,url):
    response = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    response.encoding = 'utf-8'
    tree = etree.HTML(response.text)
    a = tree.xpath('//div[@class="contbox cont11"]//a')
    for item in a:
        href = item.xpath('@href')[0]
        title = item.xpath('./text()')[0]
        get_chapter_content(str(title),f'https://www.shicimingju.com{str(href)}')
        time.sleep(2)
    pass

#获取各章节内容
def get_chapter_content(title,url):
    response = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print(title)
    response.encoding = 'utf-8'
    tree = etree.HTML(response.text)
    content = tree.xpath('//div[@class="text p_pad"]//text()')

    c = re.sub(r'\s+', "", "".join(content))
    print(c)



if __name__ == '__main__':
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    url = 'https://www.shicimingju.com/bookmark/sidamingzhu.html'
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'

    tree = etree.HTML(response.text)
    #获取四大名著标题以及超链接
    root_tree = tree.xpath('//div[@class="list clear theme2 theme3"]/a')
    for item in root_tree:
        title = item.xpath('.//p//text()')[0]
        href = item.xpath('.//@href')[0]
        get_chapter(title,f'https://www.shicimingju.com{href}')
        time.sleep(1)



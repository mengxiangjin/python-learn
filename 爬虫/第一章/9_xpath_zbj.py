import requests
from lxml import etree

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

url = 'https://www.zbj.com/fw/?type=new&kw=saas'
resp = requests.get(url,headers=headers)

tree = etree.HTML(resp.text,etree.HTMLParser())
divs = tree.xpath('//*[@id="__layout"]/div/div[3]/div/div[4]/div/div[2]/div/div[2]/div')
for div in divs:
    price = str(div.xpath('./div/div[@class="bot-content"]/div[1]/span/text()')[0]).strip('¥')
    name = 'saas'.join(div.xpath('./div/div[@class="bot-content"]/div[2]/a/span/text()'))
    company_name = div.xpath('./div/div[5]/div/div/div/text()')
    print(name)
resp.close()
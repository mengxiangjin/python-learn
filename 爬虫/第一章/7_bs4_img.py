import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

url = 'https://www.vcg.com/creative-image/shenian/'
resp = requests.get(url,headers=headers)
resp.encoding = 'utf-8'

#获取每张图片详情url
soup = BeautifulSoup(resp.text, 'html.parser')
a_list = soup.find_all('a',attrs= {
    'class':'imgWaper'
})
href_list = []
for img in a_list:
    href_list.append(img.get('href'))

#请求url，获取src地址
src_list = []
i = 0
for href in href_list:
    i = i+1
    if i == 10:
        break
    tem_res = requests.get(url=href,headers=headers)
    print(tem_res.text)
    soup = BeautifulSoup(tem_res.text, 'html.parser')
    ele = soup.find('img',attrs= {
        'class':'iyuan jss29'
    })
    src_list.append('https' + ele.get('src'))
    tem_res.close()

#下载图片
i = 0
while i < len(src_list):
    with open(str(i) + '.png', 'wb') as f:
        resp = requests.get(url=src_list[i], headers=headers)
        f.write(resp.text)
        f.close()
        resp.close()

resp.close()

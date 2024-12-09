import requests
import re
import logging



url = 'https://dytt89.com/'
headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

resp = requests.get(url=url,verify=False,headers=headers)
resp.encoding = 'gb2312'
# print(resp.text)

obj1 = re.compile(r'2024必看热片.*?<ul>(?P<content>.*?)</ul>',re.S)
obj2 = re.compile(r"href='/(?P<href>.*?)'",re.S)
obj3 = re.compile(r'◎片　　名(?P<title>.*?)<br />.*?'
                  r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<download_url>.*?)"',re.S)

url_list = []
it = obj1.finditer(resp.text)
logging.captureWarnings(True)

for i in it:
    content = i.group('content').strip()
    itt = obj2.finditer(content)
    for it in itt:
        url_list.append(url + it.group('href'))

for i in url_list:
    resp = requests.get(url = i, headers=headers,verify=False)
    resp.encoding = 'gb2312'
    res = obj3.search(resp.text)
    print(res.group('title').strip())
    print(res.group('download_url').strip())

resp.close()
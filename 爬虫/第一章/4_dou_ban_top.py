import requests
import re
import csv

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

url = 'https://movie.douban.com/top250'

resp = requests.get(url=url,headers=headers)
obj = re.compile(r'<li>.*?<span class="title">(?P<title>.*?)</span>.*?<br>(?P<time>.*?)&nbsp.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                 r'.*?<span>(?P<nums>.*?)人评价',re.S)
iter = obj.finditer(resp.text)


f = open('top_movie.csv',mode='w',encoding='utf-8')
csv_writer = csv.writer(f)
for i in iter:
    print(i.group('title') + i.group('time').strip() + ' ' + i.group('score') + ' ' + i.group('nums'))
    dic = i.groupdict()
    dic['time'] = dic['time'].strip()
    csv_writer.writerow(dic.values())

f.close()
resp.close()








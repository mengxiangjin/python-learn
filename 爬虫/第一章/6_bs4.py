import requests
from bs4 import BeautifulSoup


#stripped_strings：bs4当中返回目标中所有非标签的字符串，自动去除空格，返回的是生成器
#string：bs4当中返回目标中第一个非标签的字符串
#strings：bs4当中返回目标中所有非标签的字符串
# get('href') 获取属性值

# 表格数据
lst = []

url = 'https://www.weather.com.cn/textFC/hd.shtml'
resp = requests.get(url)
resp.encoding = 'utf-8'

soup = BeautifulSoup(resp.text, 'html.parser')
# 解析
conMidtab = soup.find('div', attrs= {
    'class': 'conMidtab'
})
tables = conMidtab.find_all('table')
for table in tables:
    trs = table.find_all('tr')[2:]
    for index, tr in enumerate(trs):
        data = {
        }
        tds = tr.find_all('td')
        if index == 0:
            city_label = tds[1]
        else:
            city_label = tds[0]
        city_name = list(city_label.stripped_strings)[0]
        city_temperature = tds[-2].string
        data['city_name'] = city_name
        data['city_temperature'] = city_temperature
        lst.append(data)
print(lst)
resp.close()


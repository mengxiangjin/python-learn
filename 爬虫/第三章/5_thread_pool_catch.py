#抓取北京新发地菜价
import math
import time
import csv

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

url = 'http://wrb.xinfadi.com.cn/getPriceData.html'

#动态改变current当前页的值，获取到全部数据，存入csv中


result_data = []
def getDatas(current):
    datas = {
        'limit': 20,
        'current': current + 1,
        'pubDateStartTime': '2024/12/12',
        'prodPcatid': 1186
    }

    req = requests.post(url,data=datas)
    json_data = req.json()
    print(f'----->after{datas['current']} over !! {json_data['list']}')
    for data in json_data['list']:
        prodName = data['prodName']
        lowPrice = data['lowPrice']
        highPrice = data['highPrice']
        avgPrice = data['avgPrice']
        place = data['place']
        result_data.append([prodName, lowPrice, highPrice, avgPrice, place])
    req.close()


def saveDatas():
    with open('vegetable_price.csv', 'w', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for data in result_data:
            csv_writer.writerow(data)

datas = {
    'limit': 20,
    'current': 1,
    'pubDateStartTime': '2024/12/12',
    'prodPcatid': 1186
}
req = requests.post(url,data=datas)
# print(req.json())
#先拿到当前分类的总数据条目
total_count = req.json()['count']

#线程个数
thread_counts = math.ceil(total_count / 20)
with ThreadPoolExecutor(max_workers=thread_counts) as executor:
    for i in range(thread_counts):
        executor.submit(getDatas, current = i)
        time.sleep(0.2)
saveDatas()
print('over')
print(len(result_data))
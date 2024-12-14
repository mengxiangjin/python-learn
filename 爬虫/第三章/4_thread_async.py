import asyncio
import json
import time

async def func1(time):
    print(f'开始下载')
    # time.sleep(time)
    await asyncio.sleep(time)
    print(f'下载完成')
async def main():
    await func1(2)
    await func1(3)
    await func1(4)
    pass

if __name__ == '__main__':
    # print(f'start:{time.strftime('%X')}')
    # asyncio.run(main())
    # print(f'end:{time.strftime('%X')}')
    res = []
    with open('city.json','r',encoding='utf-8') as f:
        citys = json.load(f)
        for i in range(0,len(citys)):
            city = citys[i]
            city['id'] = i
            city['']
            print(city)
            res.append(city)
    with open('new_city.json','w',encoding='utf-8') as f:
        json.dump(res,f,ensure_ascii=False)

import asyncio
import aiohttp
import time


async def download_img(url):
    aiohttp_session = aiohttp.ClientSession()
    name = url.rsplit('/', 1)[1]

    #with 需要将aiohttp自动close，async固定写法
    async with aiohttp_session.get(url) as resp:
        if resp.status == 200:
            with open(name, 'wb') as f:
                #resp.content.read() 读取二进制数据，异步操作，需要await(减少等待时间)
                f.write(await resp.content.read())

async def main():

    #添加任务
    url = [
        'https://i2.hdslb.com/bfs/archive/67724ff239ff193a07a52db9ddcb33d509c19086.jpg',
        'https://i1.hdslb.com/bfs/archive/055e923416bdce66cacdef34e18dece90a595309.jpg',
    ]
    list = []
    for item in url:
        list.append(asyncio.create_task(download_img(item)))

    #执行多协程任务
    await asyncio.gather(*list)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
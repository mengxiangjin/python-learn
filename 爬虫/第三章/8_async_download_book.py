import aiofiles
import aiohttp
import requests
import json
import asyncio

import time
#单线程多协程下载小说

headers = {
    'Referer': 'http://dushu.baidu.com/pc/reader?gid=4306063500&cid=1569782244',
    'cookie': 'PSTM=1718759368; BIDUPSID=F58A46A308785029783651BB2A27BF39; BAIDUID=3981665FC6FCCF4FD14C153D697697C1:SL=0:NR=10:FG=1; MCITY=-127%3A; delPer=0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=qbLOJexroG33__5JHBPAEHtYovi1z3QTDYrEOwXPsp3LGJLVY5Q-EG0PtshG1BA-oxcOogKKWmOTH7vS_gt2O-OuOu1qGMaRqsDJtf8g0M5; BCLID=6467659352210216638; H_BDCLCKID_SF=tRk8oDLhJIvDqTrP-trf5DCShUFsWtRiB2Q-XPoO3K85_UAGyx7IWq-kyhOk2b50t6Lebxbgy4op8P3y0bb2DUA1y4vpX6QIHmTxoUJ2-bnnhqoqqtnW-U4ebPRiL-r9Qg-fLfO75--K8T6O5fnhDJ_1XfQNbRJRWjnhVn0MBCK0hD0wD6Daj5PVKgTa54cbb4o2WbCQQfKM8pcN2b5oQTJyBnPtBfvGymT4aPbwa-QEhtFR0qOUWJDkXpJvQnJjt2JxaqRCyC5GKq5jDh3MKPk1Dt5Ce4ROK2Oy0hvcQb6cShP65lbrbn3XXgc9-xRtt66x2Rj4-4OUO4bIe-t2XjQhDHt8J5-OtR3aQ5rtKRTffjrnhPF3b580XP6-hnjy3b7Ubnj_WqnIhJ7HybOZhPt_DhjvWh3Ry6r42-39LPO2hpRjyxv4WfLQ54oxJpOJB5RMWxc7HR7WfU3vbURv3Pug3-Af-qJd55PH256vbl7hhtjjXtQCKJtvylOhqP-jBRIEoC0XtK0WhDvPKITD-tFO5eT22-usaanr2hcHMPoosIO50-Q8yxkY2Gj4Bn3kaK7KoPQ9BMbUotoHXnJi0btQDPvxBf7pymTjLq5TtUJM8PJThq6rqt4b5nJyKMniQKj9-pP5bfOreP-4XIcc5f40DqQxW4oN-67RatbDfn028DKuDjtBD65LjaRabK6aKC5bL6rJabC3qJosXU6q2bDeQN-eyh4tWebGbpjNWPbZDPQYDJC50q0vWq54WbbvLT7johRTWqR4oD5hqfonDh83KU7xJxjCHCOO3h7O5hvvSn6O3MAb5ltmbp8HWKr9bmOto4jTBRjCqtOeyROte-bQXH_E5bj2qRCJoK_53f; H_PS_PSSID=61027_61390_61393_61388_60853_61507_61359_61610; H_WISE_SIDS=61027_61390_61393_61388_60853_61507_61359_61610; MAWEBCUID=web_FpgeYzUCfMcqcOSNQJOmArevRyFdiJIPmpkTGxWJUTeZNfvaDH; __bid_n=19401eeff529024bee8be8; PSINO=7; BA_HECTOR=8h2haka125al01ak842k20202hh3011jmq5mc1v',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

#http://dushu.baidu.com/api/pc/getChapterContent
async def download_book(bid,cid,title):
    #单线程下多协程拼接url请求
    print(f'{title} {cid}')
    data = {
        'book_id': bid,
        'cid': f'{bid}|{cid}',
        'need_bookinfo': 1
    }
    json_data = json.dumps(data)

    #aiohttp 异步请求
    async with aiohttp.ClientSession() as session:
        url = f'http://dushu.baidu.com/api/pc/getChapterContent?data={json_data}'
        print(url)
        async with session.get(f'http://dushu.baidu.com/api/pc/getChapterContent?data={json_data}',headers=headers) as resp:
            json_data = await resp.json()
            content = json_data['data']['novel']['content']
            #异步aio
            async with aiofiles.open(f'./xiyouji/{title}.txt','w',encoding='utf-8') as f:
                await f.write(content)
            pass
    pass

async def main():
    bid = '4306063500'
    url = 'http://dushu.baidu.com/api/pc/getCatalog?data={"book_id":"4306063500"}'
    response = requests.get(url)
    #获取西游记每个章节的title、cid
    resp = response.json()
    tasks = []
    for item in resp['data']['novel']['items']:
        title = item['title']
        cid = item['cid']
        tasks.append(asyncio.create_task(download_book(bid, cid, title)))
    await asyncio.gather(*tasks)
    response.close()
    pass

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)  #速度很快，大约0.5秒结束，同步得需要15秒左右



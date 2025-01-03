import requests


if __name__ == '__main__':
    #文件地址
    url = 'https://v.cdnlz3.com/20241226/31476_29851eae/2000k/hls/'
    m3u8_url = f'{url}/mixed.m3u8'
    resp = requests.get(m3u8_url)
    with open('mixed.m3u8', 'w',encoding='utf-8') as f:
        f.write(resp.text)
    resp.close()

    #读取文件、获取下载列表
    ts_list = []
    with open('mixed.m3u8', 'r') as f:
        lines = f.readlines()
        for line in lines:
            content = line.strip('\n')
            if content.startswith('#'):
                continue
            ts_list.append(f'{url}{content}')
    for index,value in enumerate(ts_list):
        name = f'./movie/{index+1}.ts'
        with open(name,'wb') as f:
            res = requests.get(value)
            f.write(res.content)
        print(f'index:{index} total:{len(ts_list)}')


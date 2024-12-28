import requests


if __name__ == '__main__':
    #文件地址
    url = 'https://v.cdnlz3.com/20241226/31476_29851eae/2000k/hls/mixed.m3u8'
    resp = requests.get(url)
    with open('mixed.m3u8', 'w',encoding='utf-8') as f:
        f.write(resp.text)
    resp.close()

    #读取文件、获取下载列表
    with open('mixed.m3u8', 'r') as f:
        lines = f.readlines()
        for line in lines:
            content = line.strip('\n')
            print(repr(line))

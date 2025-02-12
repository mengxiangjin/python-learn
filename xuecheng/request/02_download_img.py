import requests

if __name__ == '__main__':
    url = 'https://img-blog.csdnimg.cn/42dd61494317448cb858eb7426e032f5.png'
    resp = requests.get(url)
    print(resp.content)
    with open('./file/img.png', 'wb') as f:
        f.write(resp.content)
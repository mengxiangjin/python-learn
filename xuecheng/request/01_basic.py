import requests

if __name__ == '__main__':
    url = 'http://www.17k.com'
    response = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print(response)
    print(response.status_code) #状态码
    print(response.encoding) #响应编码
    response.encoding = 'utf-8' #设置响应编码
    print(response.text) #响应字符串内容
    print(response.content) #二进制内容
    print(response.content.decode('utf-8')) #二进制解码
    print(response.url) #访问的地址
    # print(response.json()) #返回的必须为json格式，否则会报错
    print(response.headers) #响应头
    print(response.request.headers) #请求头
    print(response.request.url) #请求的url（返回的是可能会经过重定向后的url）
    print(response.ok)
    pass
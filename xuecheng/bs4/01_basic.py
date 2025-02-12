from bs4 import BeautifulSoup

if __name__ == '__main__':
    data=''
    with open('./file/douban.lxml','r',encoding='utf-8') as f:
        data=f.read()
    soup = BeautifulSoup(data,'lxml')

    #找第一个div标签，找不到即返回None
    print(soup.find('div'))
    print('---------------------------')

    #attrs：获取该标签的属性值
    print(soup.find('div').attrs)
    print('---------------------------')

    #获取具体的属性值
    print(soup.find('div').attrs['id'])
    print('---------------------------')

    #获取标签内的文本内容 以下五种都可
    print(soup.find('title').string.strip())
    print(soup.find('title').text.strip())
    print(soup.find('title').get_text().strip())
    print(soup.find('title').stripped_strings)
    print(next(soup.find('title').strings).strip())   #以生成器方式返回  for、list 进行获取 next() 获取生成器的值
    print('---------------------------')

    #查找第一个div标签且class=download
    print(soup.find('div',attrs={'class':'download'}))
    print('---------------------------')

    #输出美观
    print(soup.find('div',attrs={'class':'download'}).prettify())
    print('---------------------------')

    #获取所有 返回list
    print(soup.find_all('div',attrs={'class':'download'}))
    #获取所有的div与a
    print(soup.find_all(['div','a']))

    print('---------------------------')
    #选择器 class=download的标签
    print(soup.select('.download'))
    #id=download的标签
    print(soup.select('#download'))

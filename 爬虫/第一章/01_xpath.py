from lxml import etree


#加载本地html
parser = etree.HTMLParser(encoding='utf-8')
tree = etree.parse('./dir/douban.html',parser=parser)
print(tree)

#加载html字符串
with open('dir/douban.html', 'r', encoding='UTF-8') as f:
    data = f.read()
tree = etree.HTML(data)
print(tree)

#绝对路径查找a标签的文字，符合该路径的都会返回，list
print(tree.xpath('/html/body/div/div/div/a/text()'))


#获取符合条件的list对象，循环打印对应的文本
a_list = tree.xpath('/html/body/div/div/div/a')
print(a_list)
for a in a_list:
    print(a.text)
    #节点对象转换为标签(str)
    print(etree.tostring(a,encoding='UTF-8').decode('UTF-8'))

#相对路径 获取所有的a标签list
a_list = tree.xpath('//a')
print(a_list)

#所有a标签的直接子文本
a_list = tree.xpath('//a/text()') #<a>百度</a>
print(a_list)
#所有a标签的子文本
a_list = tree.xpath('//a//text()') #<a>百度</a>  <a><p>百度</p></a>
print(a_list)

#获取第一个div下面的a标签直接文本
print(tree.xpath('/html/body/div/div/div[1]/a/text()'))

#根据属性名匹配条件筛选
print(tree.xpath('//ul[@class="list-col list-activities"]/li/a'))
#获取a标签的href值
print(tree.xpath('//ul[@class="list-col list-activities"]/li/a/@href'))
#获取最后一个li标签中的a标签href值
print(tree.xpath('//ul[@class="list-col list-activities"]/li[last()]/a/@href'))
print(tree.xpath('//ul[@class="list-col list-activities"]/li[position<3]/a/@href'))

#属性名and
print(tree.xpath('//span[@class="book-activity-label" and @id="test_id"]/text()'))
#属性名or
print(tree.xpath('//span[@class="book-activity-label" or @id="test_id"]/text()'))
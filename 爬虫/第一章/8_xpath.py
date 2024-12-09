from lxml import etree

#text() 拿到标签的文本，返回list
#bookstore/book//title/text()：//代表book下面寻找title，（包括孙子，曾孙子所有后代）,返回所有的text[]
#bookstore/book/title/text()： /代表book下面寻找儿子title，返回其儿子title的text[]
#bookstore/book/*/abc/text()： *：通配符，任意的节点
#bookstore/book[1]/abc/text()： [1]:xPath下标是从1开始的，拿到第一个book节点下面的abc节点
#bookstore/book[1]/abc[@href='aaa']/text(): [1]:xPath下标是从1开始的，拿到第一个book节点下面的abc节点且abc节点的属性值href='aaa'的节点下面的文本
#bookstore/book[1]/abc/@href： 获取abc标签中的href值，key非value


tree = etree.parse('xml/1_xpath.xml', etree.XMLParser())
root = tree.xpath('/bookstore/book/title/text()')
print(root)
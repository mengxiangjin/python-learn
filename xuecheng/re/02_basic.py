import re

# match
# search
# findall
if __name__ == '__main__':
    #search扫描整个字符串进行匹配，只匹配一次，成功即返回否则返回None
    re_result = re.search('[a]', 'aba')
    #获取匹配到结果
    reuslt = re_result.group()
    print(reuslt)

    print(re.search('\\d{3}','123abcd4'))
    print(re.search('\\d{4}','123abcd4'))
    print(re.search('\\d{1,}','123abcd4'))

    print(re.search('^\\d','123abcd4'))
    print(re.search('^\\d','a23abcd4'))

    #match从字符串开头进行匹配，若开头不匹配，直接返回None
    print(re.match('\\d','abc123'))
    print(re.match('\\d{3}','123abc123'))


    #findall匹配所有命中的 ()获取某一内容
    str = '<b>luch</b> <b>is</b> <b>a</b> <b>word</b> <p>big</p>'
    print(re.findall('<b>(.*?)</b>', str))
    print(re.findall('<b>.*?</b>', str))
    print(re.findall('(<b>(.*?)</b>)', str))

    #finditer 匹配所有命中，返回迭代器
    iter = re.finditer('<b>(.*?)</b>', str)
    for match in iter:
        print(match.group())


    str = """
        <A href="http://www.baidu.com">baidu</A>
        <a href="http://www.xinlang.com">xin
lang</a>
        <a href="http://www.baidu.com">sougou</a>
    """
    print(re.findall('<[Aa] href=".*?</[Aa]>', str))    #xinlang之间有回车 .*?无法匹配到
    print(re.findall('<[Aa] href="(.*?)</[Aa]>', str))    #xinlang之间有回车 .*?无法匹配到
    print(re.findall('<[Aa] href="(.*?)</[Aa]>', str,re.S))    #xinlang之间有回车 .*?无法匹配到 re.S修正符，匹配到换行符
    print(re.findall('<[a] href="(.*?)</[a]>', str,re.S|re.I))    #xinlang之间有回车 .*?无法匹配到 re.S修正符，匹配到换行符 re.I:不区分大小写


    #起名称 .*?代表的值取名称
    str = """
        <b>luck</b>
    """
    print(re.search('<b>(?P<name>.*?)</b>', str).group('name'))
    print(re.search('<b>(.*?)</b>', str).group())
    print(re.search('<b>(.*?)</b>', str).groups())

    #拆分
    print(re.split('\\d','a1f4g4b'))
    print(re.split('\\d','a12f433g4b'))

    #替换 \s所有的空白符替换
    s = 'hell \t sadas \nsdsf\nsd'
    print(re.sub('\s','',s))

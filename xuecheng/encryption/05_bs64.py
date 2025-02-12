#长度必须为4的倍数，不是=补齐，所以结尾的=不可能超过3个

import base64

# 编码
# 以后只要看到结尾有 =  就是base64编码，base64编码的长度，必须是4的倍数，如果不是4的倍数，使用=补齐
# 所以结尾的= 不会超过3个
res=base64.b64encode(b'hello world')  #aGVsbG8gd29ybGQ=  以后只要看到结尾有 =  就是base64编码，base64编码的长度，必须是4的倍数，如果不是4的倍数，使用=补齐
print(res)

# 解码
res=base64.b64decode('aGVsbG8gd29ybGQ=')
print(res)

# 补充：base64的用途在哪
'''
1 网络上传递数据 字符串形式
2 有些图片，使用base64编码   12306
'''
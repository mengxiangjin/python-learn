

# 今日内容

# 1 python还原各种加密算法

```python
# 以后破解app ，会遇到各种各样的加密方式---》以后再遇到类似的加密---》直接把代码拿过去改一下即可
1 单向加密(不可解密)：md5，sha 系列
2 对称加密(加密秘钥和解密秘钥是一样的)：AES,DES
3 非对称加密(公钥和私钥)：RSA，DSA
4 补充算法：base64  （它不是加密，它是编码解码）
```

## 1.1 md5

```python
import hashlib
m = hashlib.md5()
m.update('helloworld'.encode("utf8")) # bytes格式  可能会加盐
print(m.hexdigest())
```

## 1.2 sha1

```python
import hashlib
sha1 = hashlib.sha1()
sha1.update('helloword'.encode('utf-8')) 
print(sha1.hexdigest())
```

## 1.3 des加密

```python
# 前端提交的数据加密了，请求体中加密了---》一般使用AES,DES---》要在后端解密

# pip3 install pycryptodomex
# DES是一个分组加密算法，典型的DES以64位为分组对数据加密，加密和解密用的是同一个算法。它的密钥长度是56位（因为每个第8 位都用作奇偶校验），密钥可以是任意的56位的数，而且可以任意时候改变。

from Cryptodome.Cipher import DES
key = b'88888888'
data = "hello world"
count = 8 - (len(data) % 8)
plaintext = data + count * "="
des = DES.new(key, DES.MODE_ECB)
ciphertext = des.encrypt(plaintext.encode())
print(ciphertext)
plaintext = des.decrypt(ciphertext)
plaintext = plaintext[:(len(plaintext)-count)]
print(plaintext)

```



## 1.4 RSA加密

```python
# 安装模块
pip3 install rsa

import rsa
# 返回 公钥加密、私钥解密
public_key, private_key = rsa.newkeys(1024)
print(public_key)
print(private_key)

# plaintext = b"hello world"
# ciphertext = rsa.encrypt(plaintext, public_key)  # 公钥加密
# print('公钥加密后：',ciphertext)
# plaintext = rsa.decrypt(ciphertext, private_key) # 私钥解密
# print('私钥解密：',plaintext)

### 使用私钥签名
plaintext = b"hello world"
sign_message = rsa.sign(plaintext, private_key, "MD5")
print('私钥签名后：',sign_message)

## 验证私钥签名
plaintext = b"hello world"
method = rsa.verify(b"hello world", sign_message, public_key)
# method = rsa.verify(b"hello world1", sign_message, public_key) # 报错Verification failed
print(method)
```



## 1.5 base64编码和解码

```python
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
```



# 2  抓包逆向案例

## 3.1 金树林app

### 3.1.1 目标

```python
# 1 发送验证码
# 2 自动注册
# 3 自动登录
# 4 查询商品信息

# app的获取
	-豌豆荚下载
    -老师给的软件中获取
# 前置步骤
	1 下载apk后安装到手机上   adb install  apk名字
    2 打开charles
    3 手机端配置好手机抓包(https的包)
    	-root，配置都需要做完
```

### 3.1.2 发送验证码

```python
# 具体操作步骤
	1 打开app后，输入手机号，发送验证码
    2 看charles的抓包
    
# 请求地址
https://miappshop.jshulin.com/memberLogin/phoneCode
# 请求方式
get
# 请求头（没有特殊的，可以不带）

# 请求参数
?phone=18953675221&serviceType=5
```

**python实现金树林发送验证码**

```python
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)'
}
res = requests.get('https://miappshop.jshulin.com/memberLogin/phoneCode?phone=%s&serviceType=5' % '18953675221',
                   verify=False, headers=headers)
print(res.text)
```

###  3.1.3 自动注册

```python
# 请求地址：https://miappshop.jshulin.com/memberLogin/memberRegister
# 请求方式：post
# 请求头：user-agent
# 请求体：
{"phone":"18953675221","fid":"","password":"lqz12345","phoneCode":"802827"}



####代码实现

import requests
import urllib3
### 使用接码平台---》用个手机号接码
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)'
}
# 通过上面的发送验证码拿到
data = {"phone": "18953675221", "fid": "", "password": "lqz12345", "phoneCode": "147426"}
res = requests.post('https://miappshop.jshulin.com/memberLogin/memberRegister', json=data, verify=False,headers=headers)
print(res.text)

```

###  3.1.3 自动登录

```python
# 请求地址：https://miappshop.jshulin.com/memberLogin/login
# 请求方式：post
# 请求头：user-agent
# 请求体：
{"password":"lqz12345","username":"17717823244"}


```

**pyton代码**

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)'
}
data={"password":"lqz12345","username":"17717823244"}
res=requests.post('https://miappshop.jshulin.com/memberLogin/login',json=data,verify=False,headers=headers)
print(res.text)
```

### 3.1.4 查询商品信息

```python
# 请求地址：
https://miappshop.jshulin.com/pro/searchByPage
    
# 请求方式：
post
# 请求头：
user-agent
Mobile-Token:登录后返回的
# 请求体：
{
	"cityNo": "",
	"keyword": "石榴",
	"limit": 10,
	"orderByContent": "",
	"page": 1,
	"enabled": 1
}
```

**python实现**

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'Mobile-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjcxMTMyMDA2MDczNjA2MTQ1IiwiZXhwIjoxNjkyMzcwOTk2LCJpYXQiOjE2OTIzNjczOTYsInVzZXJJZCI6IjE2NzExMzIwMDYwNzM2MDYxNDUiLCJ1c2VybmFtZSI6IjE3NzE3ODIzMjQ0In0.EvemzUvZPHr2eF4AERxQeLhZfUW1H6Gvbn-xnxgmpn4', # 登录成功返回的token
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)'
}

data = {
    "cityNo": "",
    "keyword": "石榴",
    "limit": 10,
    "orderByContent": "",
    "page": 1,
    "enabled": 1
}

res = requests.post('https://miappshop.jshulin.com/pro/searchByPage', json=data, verify=False, headers=headers)
print(res.text)

```







## 3.2 爱安丘app(v228版本)



### 3.2.1 爱安丘发送手机验证码

```python
# 目标---v228---》放在软件中了
	发送验证码登录
    
    
# 1 把app安装到手机
# 2 打开charles抓包，我们发现抓不到
# 3 抓不到的原因是，它使用了验证证书
	-1 官网下载：LSposed https://github.com/LSPosed/LSPosed/releases
    -2 把下载好的zip push 到手机上：LSPosed-v1.8.6-6712-zygisk-release.zip
    -3 使用面具刷入
    -4 在手机上装JustTrustMe.apk 
    	adb install JustTrustMe.apk 
    -5 打开LSposed，选择模块--》进入--》点中爱安丘app，让它信任，这样就可以抓包了
#4 登录功能，发送短信验证码
	-请求地址是：https://app-auth.iqilu.com/member/phonecode
    -请求方式：post
    -请求体：{"phone":"18953675221"}
    -请求头：
    orgid	137
cq-agent:	{"os":"android","imei":"bae6495482efee22","osversion":"11","network":"none","version":"0.0.28.108","core":"1.6.4"}
Cookie:orgid=137
    
    
# 5 使用python模拟发送获取验证码的请求

```

**python代码**

```python
import requests
import utils

phone = input('请输入手机号：')
data = {"phone": "%s" % phone}
headers = {
    'user-agent': 'chuangqi.o.137.com.iqilu.app137/0.0.28.108',
    'orgid': '137',
    'cq-agent': '{"os":"android","imei":"%s","osversion":"11","network":"none","version":"0.0.28.108","core":"1.6.4"}' % utils.gen_imei(),
    'Cookie': 'orgid=137',
}
res = requests.post('https://app-auth.iqilu.com/member/phonecode', json=data, verify=False, headers=headers)
print(res.text)

# {"code":1,"data":"CA4fE6pRJY/xEZYctFjp2Xdv5KdGLxuNVXI+qLQ+yYQ="}
```









![image-20230818204043751](imgs/day04-课堂笔记.assets/image-20230818204043751.png)

![image-20230818204159525](imgs/day04-课堂笔记.assets/image-20230818204159525.png)





### 3.2.2 imei解释

```python
IMEI（International Mobile Equipment Identity）是【国际移动设备识别码】的缩写，它是一个唯一标识符，用于识别移动设备，如手机、平板电脑等。IMEI由15位数字组成，每一位都有特定的含义

# IMEI的规则如下：
前六位（TAC）：型号核准号码，用于识别设备的制造商和设备类型。
接下来的两位（FAC）：最终装配代码，表示设备的最终装配站。
后面的六位（SNR）：串号，表示设备的序列号。
最后一位（SP）：校验位，用于验证IMEI的有效性


# 使用python模拟生成
# 生成方式1 
"".join(random.choices('0123456789abcdef', k=15))
# 生成方式2 
```

### 3.2.3 验证码登录

```python
# 请求地址：
https://app-auth.iqilu.com/member/login
# 请求方式：post
# 请求体：
{
	"phone": "18953675221",
	"code": "151011",
	"key": "9eXW8/QJxmQnhmyoewmbpoJLT5nxbUeVDLE5Ryt7Grg=", # 上一次发送手机验证码接口返回的那个data base64编码
	"password": "",
	"captcha": "",
	"captchaKey": ""
}
# 请求头：
	跟之前一样
    
    
    
# 使用python 模拟登录

```

**Python代码**

```python
import requests
import utils

# 1 发送验证码
phone = input('请输入手机号：')
imei = utils.gen_imei()
data = {"phone": "%s" % phone}
headers = {
    'user-agent': 'chuangqi.o.137.com.iqilu.app137/0.0.28.108',
    'orgid': '137',
    'cq-agent': '{"os":"android","imei":"%s","osversion":"11","network":"none","version":"0.0.28.108","core":"1.6.4"}' % imei,
    'Cookie': 'orgid=137',
}
res = requests.post('https://app-auth.iqilu.com/member/phonecode', json=data, verify=False, headers=headers)
res_data = res.json()['data']

# 2 验证码登录-=====》接码平台
code = input('请输入手机收到的验证码：')
data = {
    "phone": "%s" % phone,
    "code": "%s" % code,
    "key": res_data,  # 上一次发送手机验证码接口返回的那个data base64编码
    "password": "",
    "captcha": "",
    "captchaKey": ""
}
res = requests.post('https://app-auth.iqilu.com/member/login', json=data, verify=False, headers=headers)

print(res.text)

```





### 3.2.4 接码平台

```python
# 可以接收手机验证码的平台---》这些东西违法--》小心点
	-免费--不稳定
    -收费的--靠谱
    

# 免费收费大全
https://w3h5.com/post/619.html
    
# 例如 接收中国短信（免费的不稳定）
https://www.goinsms.xyz/cn.php
https://smscoders.com/china_phones
# 自行找收费的，注意别被骗，收费的都会带api接口
```

![image-20230818192133330](imgs/day04-课堂笔记.assets/image-20230818192133330.png)

![image-20230818192227305](imgs/day04-课堂笔记.assets/image-20230818192227305.png)



![image-20230818192506833](imgs/day04-课堂笔记.assets/image-20230818192506833.png)

![image-20230818192521411](imgs/day04-课堂笔记.assets/image-20230818192521411.png)

![image-20230818192534314](imgs/day04-课堂笔记.assets/image-20230818192534314.png)







# 3 抓包+反编译逆向案例

## 3.1 爱安丘app（最新版）

```python
# 用户名密码登录

# 换成最新版
# 抓包分析
	-请求地址：https://app-auth.iqilu.com/member/login?e=1
    -请求方式：post
    -请求体：
    {
	"codeKey": "",
	"password": "Gq7piXQy+YGPZ7yzBeElEA==",  # 加密了，是base64
	"code": "",
	"phone": "18953675221",
	"key": ""
    }
    -请求头：跟老版本一样
    
    
# 咱们得目标：破解密码的加密---》反编译apk---》根据关键字搜索加密方式
	-关键词：password    "password"    "password
	-优先用url搜索：会唯一  member/login
    
    
#1  搜索---》一路查找，定位到了--》java不太懂，听我讲即可
public static String aesPassword(String str) {
	return Base64.encodeToString(EncryptUtils.encryptAES(str.getBytes(), getMD5(PRIVATE_KEY + getSecret() + BaseApp.orgid).getBytes(), "AES/CBC/PKCS7Padding", "0000000000000000".getBytes()), 2);
    }

# 1 使用：encryptAES 对传入的字符串加密(明文密码)
# 2 getMD5(PRIVATE_KEY + getSecret() + BaseApp.orgid).getBytes()  得到aes加密的秘钥，固定的
# 3 "AES/CBC/PKCS7Padding" 加密方式
# 4 iv：偏移量    0000000000000000
# 6 转成base64编码


# 2 需要知道aes加密的秘钥，秘钥是固定的--》hook得到---》getMD5
####1 手机端启动frida-serve
adb shell
su
cd /data/local/tmp/
ls
./frida-server

####2 设置端口转发
adb forward tcp:27042 tcp:27042
adb forward tcp:27043 tcp:27043

```

![image-20230818222002159](imgs/day04-课堂笔记.assets/image-20230818222002159.png)



![image-20230818222051400](imgs/day04-课堂笔记.assets/image-20230818222051400.png)



![image-20230818222227318](imgs/day04-课堂笔记.assets/image-20230818222227318.png)



![image-20230818222326012](imgs/day04-课堂笔记.assets/image-20230818222326012.png)





# 4 Java 介绍

```python
# 1 反编译出来的代码，都是java代码，能够读懂java代码，才能看懂加密逻辑
# 2 接下来就要学习 java
	-找到加密算法---》自己实在读不懂---》chatgpt实现---》得到python代码--》拿来测试，跟抓包抓到的比较
    
    
# 3 java 语言---》编译型语言
	-java se ：java基础，变量，函数，面向对象，网络，多线程。。。
    -java ee: web开发--》咱们用不到，不学
    -java me（弃用了）：早些年用，现在已经不用了，它不是安卓---》山寨机--》打开一个游戏--》弹出java的图标
    -安卓 sdk包：用来做安卓开发，需要你有java se 基础
    	-java se +安卓 sdk包
        
        
 # 4 java 集成开发工具包  sdk
	-jdk:java 集成开发工具包 ---》我们做开发一定要装这个玩意--》最新版是23 ---》咱们用8--》反编译回来都是8的代码
    -jre：java 运行环境，正常来讲，java开发完代码，放在电脑上运行，要装它---》但是好多人都直接装jdk
    	-你会看到无论开发还是运行java，大家都装jdk，其实是不用的，只运行，用jre就够了
        -jdk包含jre
    -jvm：java 虚拟机 ，java编译后得到字节码文件，字节码文件必须运行在java虚拟机上，
    	-在不同的操作上装jvm，于是java 跨平台，因为不同平台装了不用平台的jvm
        
    -jdk包含了jre，jre包含了jvm
    
    
# 5 正常来讲，编译型语言，不能跨平台
	-python --》解释型--》运行在python解释器上---》无论开发还是运行，都要装python解释器
    -c，go，c++---》编译型-->代码直接编译成可执行文件---》不需要装任何东西--》直接运行在操作系统之上
    -java 很特殊---》java编译后，不是可执行文件---》字节码文件---》不能直接运行在操作系统之上---》需要运行在jvm之上---》
    
# 6 java是编译型还是解释型？
	-编译型
    
    
# 7 咱们已经装过了 jdk  8
java -version
java version "1.8.0_371"
Java(TM) SE Runtime Environment (build 1.8.0_371-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.371-b11, mixed mode)

```




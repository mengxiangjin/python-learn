# 今日内容



# 1 配置charles抓取https包

```python
# 学习过了charles抓取手机app的http包---》爱学生案例
	-真机和模拟器
# 后期咱们做的app，大部分都是https包---》今日南川，车智赢
```



## 1.1 模拟器安装charles证书抓取https包（安卓版本要7以下）

```python
# 注意：安卓版本
	-pixel 2xl---》安卓11版本
    -模拟器：mumu，有两款
    	-最新12---》安卓版本是12
        -老版本6版本---》安卓版本是6--》mac和win选择装这个版本
        
# 使用mumu模拟器老版本：6版本作为讲课
	-安卓7以下的设备，安装证书后，不需要移动证书，直接就可以使用---》老版本6版本
    -安卓7以上设备，安装证书后，需要移动证书，才能使用---》真机
    
    
# 要抓取https的包，必须安装证书（charles的证书）---》客户端--》真机，模拟器
	-https=http+ssl
    -ssl：非对称加密，需要有证书
```



```python
###具体步骤---》模拟老版本安卓6---》####
1 打开charles--》help---》SSLProxying---》InstallCharles Root Certificate on a Mobile...
2 打开手机，配置好代理--之前讲过
3 手机浏览器访问：chls.pro/ssl
4 下载完成后，点击，起个名字，安装
5 安卓完成后，就可以抓取https的包了
```

![image-20230613174851004](imgs/day03-课堂笔记.assets/image-20230613174851004.png)

![image-20230613175000594](imgs/day03-课堂笔记.assets/image-20230613175000594.png)

![image-20230816202032163](imgs/day03-课堂笔记.assets/image-20230816202032163.png)



## 1.2 真机安装证书，抓取https包(安卓版本大于7)

```python
# 1 真机配置好代理
# 2 手机浏览器访问：chls.pro/ssl
# 3 下载证书---》安装到手机上（直接装装不了--》设置中做）---》用户证书
	下载后，手机打开：安全---》加密与凭据---》安装证书---》安装完成
# 4 能够看到用户证书（用户证书）

# 5 转成系统证书才能抓https包
# 6 move-cert模块---》手机必须root---》安装面具--》安装模块
	-movecert-1.9-4.zip 放到手机上 ---》adb push 
    -使用面具安装，选择模块，找到那个zip，安装---》重启
    -重启完成后，会发现，用户证书里没有了，放到了系统证书中了
# 7 到此可以抓取https的包了
```

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613181740583.png" alt="image-20230613181740583" style="zoom:50%;" />

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613181808528.png" alt="image-20230613181808528" style="zoom:50%;" />

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613181904592.png" alt="image-20230613181904592" style="zoom:50%;" />

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613181957192.png" alt="image-20230613181957192" style="zoom:50%;" />



![image-20230816203552898](imgs/day03-课堂笔记.assets/image-20230816203552898.png)

![image-20230816204041645](imgs/day03-课堂笔记.assets/image-20230816204041645.png)





## 1.2 上述配好，如果抓包出现乱码

```python
# 1 charles上
# 2 proxy---》proxy ssl settings
# 3 按如下配置

```

![image-20230816204723408](imgs/day03-课堂笔记.assets/image-20230816204723408.png)

![image-20230816204826695](imgs/day03-课堂笔记.assets/image-20230816204826695.png)

## 1.3 用户证书和系统证书

```python
在 Android 系统中，有两种类型的证书：用户证书（User Certificates）和系统证书（System Certificates）。

用户证书（User Certificates）：用户证书是由特定用户生成或颁发的数字证书。这些证书通常用于用户身份验证和安全通信。用户证书可以用于加密和解密数据，数字签名以及建立安全连接。用户证书通常由用户自己创建，例如，用于加密电子邮件、VPN连接或身份验证。

系统证书（System Certificates）：系统证书是由 Android 系统或设备制造商预装的证书。这些证书通常用于系统级别的安全功能，如应用程序签名验证、SSL/TLS 连接等。系统证书通常用于验证应用程序的真实性和完整性，以确保它们没有被篡改或恶意修改。这些证书由 Android 操作系统或设备制造商管理和维护。

系统证书包括以下几种类型：

代码签名证书：用于验证应用程序的签名，以确保应用程序的真实性和完整性。
安全通信证书：用于建立 SSL/TLS 连接，保护设备和服务器之间的通信安全。
根证书：根证书用于验证其他证书的真实性。Android 系统预装了一组根证书，用于验证 SSL/TLS 通信中的服务器证书。
用户证书和系统证书在安全和身份验证方面扮演不同的角色。用户证书由用户自己管理，用于个人身份验证和加密通信。而系统证书由操作系统或设备制造商管理，用于验证应用程序和保护系统级别的通信安全。
```



## 1.4 用户证书转成系统证书

```python
# 1 将move cert压缩包传到手机（任意好找的一个目录 `/sdcard/Download/`）
adb push /Users/lqz/soft/movecert-1.9-4.zip  /sdcard/Download
# 2 使用面具，刷入
	按照下图步骤
  
# 3 重启手机

# 4 手机打开：安全--》加密与凭据---》信任的凭据
	-此时可以看到用户级别证书移动到系统级别了
  
# 5 此时可以愉快抓https包了
```



<img src="imgs/day03-课堂笔记.assets/image-20230613182733476.png" alt="image-20230613182733476" style="zoom:50%;" />

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613182527697.png" alt="image-20230613182527697" style="zoom:50%;" />

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613182815594.png" alt="image-20230613182815594" style="zoom:50%;" />

<img src="imgs/day03-反编译工具和hook框架参考笔记.assets/image-20230613182834375.png" alt="image-20230613182834375" style="zoom:50%;" />

![image-20230816204457153](imgs/day03-课堂笔记.assets/image-20230816204457153.png)

## 1.5 小案例抓https包

```python
# 以今日南川app为例：
	-把apk直接拖入模拟器，安装成功---》要求更新---》更到最新即可
    -找到登录，输入用户名密码--》点击登录
    -查看charles的抓包
    
    
# 登录的包
	-地址：https://api.cqliving.com/login.html
    -请求方式：post
    -请求头：
    	appid	32  # 测试可以不带
        sessionid	3cedc892-a84a-47ec-895b-f3f30047302c
        token	
        t	1692188648594
        sign	d4a94154cbae5fa438d852f1beb68a60
        cqlivingappclienttype	1
        cqlivingappclientversion	2031
    -请求体：
    	appId	32
        hashSign	1382889b3f7dc16365df8614d4bdf928
        imgUrl	
        lat	29.568295
        lng	106.559123
        loginName	18953675222
        nickName	
        openId	
        place	重庆
        pwd	fcea920f7412b5da7be0cf42b8c93759
        sessionId	3cedc892-a84a-47ec-895b-f3f30047302c
        token	 # 可以不带
        type	 # 可以不带
   


# 使用python重写请求，发送
```



```python
import requests

data = {
    'appId': '32',
    'hashSign': '5cbcd0d5aa6e8c465c9eda4c178e467e',
    'imgUrl': '',
    'lat': '29.568295',
    'lng': '106.559123',
    'loginName': '18956875221',
    'nickName': '',
    'openId': '',
    'place': '重庆',
    'pwd': '734f7fb5e505a3dd35c29d3af4795c79',
    'sessionId': '1cda109e-a35b-46c0-9161-21f3dd67ad63',
    'token': '',
    'type': '',
}
# 发送请求，发现返回 ：感谢您的反馈，应用防火墙会尽快进行分析和确认
# 说明模拟的不像
# 请求地址，请求体都是了---》请求头：
headers = {
    'sessionid': '1cda109e-a35b-46c0-9161-21f3dd67ad63',
    'token': '',
    't': '1692190592030',
    'sign': 'a7da03d417519e1a059de13c4747eeea',
    'cqlivingappclienttype': '1',
    'cqlivingappclientversion': '2031',
    'accept-encoding': 'gzip',
    'user-agent': 'okhttp/4.10.0',  # 必须带的
    'content-length': '236',
    'content-type': 'application/x-www-form-urlencoded'
}
res = requests.post('https://api.cqliving.com/login.html', data=data, verify=False, headers=headers)
print(res.text)

```



## 1.6 charles 重新发送包和修改包

```python
# 重新发送：在发送的地址上，点右键---》repeat

# 修改包再发送：在发送的地址上，点右键---》compose
	-以后常用---》验证参数可以不携带，以后就不用破解它了
```





# 2 反编译工具

## 2.1 常见反编译工具

```python
# 常见的反编译工具：jadx（推荐）、jeb、GDA(不支持mac，免费，收费)
	-以后如果反编译某个app，发现反编译不完成，可以选择其他的测
    
# 反编译工具依赖java环境，需要安装jdk
```



## 2.2 jdk环境搭建

```python
# 安装jdk环境---》目前给jadx使用
# 后期我们会学java开发，也需要jdk环境

# 去官网下载jdk---》jdk21---》而咱们用jdk8
	-好多公司，做java开发，还在用jdk8
    -https://www.oracle.com/java/technologies/downloads/
    -注册账号，找位置还挺麻烦
    
# 直接用下好的

# 下载地址
链接: https://pan.baidu.com/s/10CuP_snpciwvYkWlVFATXA 
提取码: tt88
 

# mac安装
	-一路下一步，确定即可

# win安装
	-一路下一步，选好安装位置，确定即可
    
    
# 验证是否安装成功命令窗口中
	java -version  # 能看到输出，就是安装完成
    java version "1.8.0_371"
    Java(TM) SE Runtime Environment (build 1.8.0_371-b11)
    Java HotSpot(TM) 64-Bit Server VM (build 25.371-b11, mixed mode)
```



## 2.3 安装jadx

```python
# 1 官网下载
https://github.com/skylot/jadx/releases
# 最新版是： 1.4.7  可以用这个

# 2 老版本 1.2.0---》后面有个app，用最新版，反编译不全--》还会用1.2.0

# win上使用
	# ---第一个----
	- jdk装好了
    -只需要下载：jadx-gui-1.4.7-no-jre-win.exe
    -下载下来双击运行即可
    
    #---第二个---
    没有安装jdk
    下载：jadx-gui-1.4.7-with-jre-win.zip
    解压开，双击exe运行即可
    
    # ---第三个--不分win还是mac是一样的--
    安装jdk
    下载：jadx-1.4.7 .zip
    解压开：执行bin目录下
    	-jadx
        -jadx-gui-->mac 双击它运行
        
        jadx.bat
        jadx-gui.bat --》双击它运行
    
    
  # mac上
	安装jdk
    下载：jadx-1.4.7 .zip
    解压开：执行bin目录下
    	-jadx
        -jadx-gui-->mac 双击它运行
```





# 3 反编译某app定位代码

```python
# 反编译工具安装完成

# 反编译，定位app代码-》
	-车智赢app ：v3.13.0
    -更新到最新版 v3.22.x
    
# 咱们配置的可以抓http是的包了--》打开charles---》抓登录包

```



## 3.1 抓包

```python
# 登录地址：
https://dealercloudapi.che168.com/tradercloud/sealed/login/login.ashx
# 请求方式：
post
# 请求头：
没有特殊
# 请求体：
_appid	atc.android
_sign	D51FD8853BC1792E3AD07C1D59626C8C
appversion	3.24.1
channelid	csy
pwd	fcea920f7412b5da7be0cf42b8c93759
udid	WyjO2aBlQKKMruzg8k5BpG/Y/cXnsxROXjQiCSHx+nFZtFirQQTDu9tEC1F6 6STcG0eOoLln3xYn4OWsuQEz1w==
username	18953675221


# 目标：破解 pwd是如何加密的

```



## 3.2 反编译后定位代码位置

```python
# 1 把最新版的车智赢app，拖到 jadx中
# 2 等一会，就会把该apk反编译成java代码(咱们目前不懂java)
# 3 通过查找，定位登录接口如何写的
	-以后去搜：  pwd    "pwd"    "pwd      put("pwd
    -但是优先推荐用url搜索--——》url只有一个--》登录的url---》pwd就是在这个url中加密的
    https://dealercloudapi.che168.com/tradercloud/sealed/login/login.ashx
    -搜索：login/login.ashx
# 4 定位到它pwd字段是如何加密的
	-通过url地址，搜索到：
    -public static final String LOGIN_URL = "/tradercloud/sealed/login/login.ashx";
	-有的代码位置一定使用了这个常量：
    -在常量上  右键---》查找用例--（哪里用了LOGIN_URL）
    -搜到后双击
# 5 定位到登录接口的代码位置
public static void loginByPassword(String str, String str2, String str3, ResponseCallback<UserBean> responseCallback) {
        HttpUtil.Builder builder = new HttpUtil.Builder();
        builder.tag(str).method(HttpUtil.Method.POST).signType(1).url(LOGIN_URL).param("username", str2).param("pwd", SecurityUtil.encodeMD5(str3));
        doRequest(builder, responseCallback, new TypeToken<BaseResult<UserBean>>() { // from class: com.che168.autotradercloud.user.model.UserModel.5
        }.getType());
    }
# 6 看到了param("pwd", SecurityUtil.encodeMD5(str3))
# 7 密码明文通过SecurityUtil.encodeMD5(str3) 得到了密文--》发送请求

# 8 SecurityUtil.encodeMD5的代码是什么
	在上面点右键---》跳到声明
# 9 看到代码---》就是md5加密
    public static final String encodeMD5(String str) {
        char[] cArr = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};
        try {
            byte[] bytes = str.getBytes();
            MessageDigest messageDigest = MessageDigest.getInstance("MD5");
            messageDigest.update(bytes);
            byte[] digest = messageDigest.digest();
            char[] cArr2 = new char[digest.length * 2];
            int i = 0;
            for (byte b : digest) {
                int i2 = i + 1;
                cArr2[i] = cArr[(b >>> 4) & 15];
                i = i2 + 1;
                cArr2[i2] = cArr[b & bx.m];
            }
            return new String(cArr2).toLowerCase();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }


# 10 可以使用python复现--》发现确实是
import hashlib
md5=hashlib.md5()
md5.update(b'1234567') # fcea920f7412b5da7be0cf42b8c93759
print(md5.hexdigest()) # fcea920f7412b5da7be0cf42b8c93759



######11 注意：咱们目前看不懂java代码，很正常--》后期咱们会学java，安卓开发
```





# 4 hook框架frida

```python
# 搜出位置---》找到了代码---》你确定他就是吗？
# 我们现在不确定代码有没有走咱们找的地方

# 借助于另一个东西，帮咱们确认，它确实走了它

# hook框架---》通过hook(钩子)--》拦截 把我找的函数hook住，看看有没有执行
Hook 框架是一种技术，用于在运行时拦截和修改应用程序的行为。
通过 Hook，你可以劫持应用程序的方法调用、修改参数、篡改返回值等，以达到对应用程序的修改、增强或调试的目的

# 常见的有：
Xposed Framework：Xposed 是一个功能强大的开源 Hook 框架，可以在不修改应用程序源代码的情况下，对应用程序进行各种修改。它允许你编写模块来拦截和修改应用程序的方法调用，修改应用程序的行为和逻辑。

Frida（咱们讲）：Frida 是一个跨平台的动态 Hook 框架，支持安卓和其他操作系统。它提供了一个强大的 JavaScript API，可以在运行时对应用程序进行 Hook，包括方法拦截、参数修改、调用注入等。Frida 可以用于安全研究、逆向工程和应用程序调试等方面。
```



## 4.1 下载安装(电脑，手机)

```python
#搭建frida的hook环境---》电脑上hook手机---》电脑要配置，手机要配置

# 电脑端一定要安装python解释器---》3.9 我用的，建议你们也是3.9
# 手机端要跟电脑端【版本一致】
####版本一定要对应

```



### 4.1.1 电脑端配置

```python
# 下载两个模块---》最新版
pip install frida           # 16.1.3  16.6.6
pip install frida-tools     # 12.2.1  13.6.1
```





### 4.1.2 手机端配置

```python
# 去frida官网，下载对应版本的 frida-server  ----》16.1.3
	-https://github.com/frida/frida/releases
# 下的frida-server跟手机架构对应
	-adb shell getprop ro.product.cpu.abi
    -arm64-v8a
    
# 根据手机平台下载：
# 压缩包=---解压---》看到frida-server-16.1.3-android-arm64
# 推送到手机上---》不要把压缩包放到手机上
	adb push frida-server-16.1.3-android-arm64   /data/local/tmp
    
# 去手机那个目录下看看有没有

# 按照命令
	adb shell  # 进入手机命令行
    su  #切换为root用户
    cd /data/local/tmp  # 切换到目录下
    chmod 755 frida-server-16.1.3-android-arm64  # 加入执行权限
    ls -al  # 查看文件
    
```

![image-20230816221452901](imgs/day03-课堂笔记.assets/image-20230816221452901.png)



## 4.2 启动并hook-app程序

```python
# 刚刚反编译：找到这个  SecurityUtil.encodeMD5(str3)，觉得密码加密用的它
# 但是不确定--》现在要用frida，hook这个函数，看一下是不是真的走了
```

### 4.2.1 通过frida，打印出当前手机所有的进程和前台进程（固定代码）

```python
# 前置条件一：
	手机端启动frida-server
    进入到手机路径下  ./frida-server  # 你的名字一定要对

# 前置条件二：
	在电脑端要做端口转发---》命令行中执行---》电脑
    adb forward tcp:27042 tcp:27042
	adb forward tcp:27043 tcp:27043
# 然后才能hook
import frida

# 获取设备信息
rdev = frida.get_remote_device()

# 枚举所有的进程
processes = rdev.enumerate_processes()
for process in processes:
    print(process)

# 获取在前台运行的APP
front_app = rdev.get_frontmost_application()
print(front_app)
```



## 4.3 hook某智赢app-pwd加密算法

```python
# hook-->encodeMD5--在登录的时候，有没有走它--》只要走了它--》hook代码执行了---可以修改内容
# hook返回值是明文---》抓包看到也是明文

# 确定了，密码加密，就会走encodeMD5

import frida
import sys
# 连接手机设备
rdev = frida.get_remote_device()

# 包名：com.che168.autotradercloud
# 车智赢+
session = rdev.attach("车智赢+")  # app名字

# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：com.autohome.ahkit.utils下的
    var SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");

    //替换类中的方法
    SecurityUtil.encodeMD5.implementation = function(str){
        console.log("传入的参数(未加密之前的)：",str);
        var res = this.encodeMD5(str); //调用原来的函数
        console.log("返回值（加密后的字符串）：",res);
        return str;  // 没加密的
    }
});
"""


# -----下面固定---以后不会动
script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()
```

![image-20230816223908964](imgs/day03-课堂笔记.assets/image-20230816223908964.png)

## 4.4 使用python还原加密算法

```python
import hashlib
md5=hashlib.md5()
md5.update(b'1234567') # fcea920f7412b5da7be0cf42b8c93759
print(md5.hexdigest()) # fcea920f7412b5da7be0cf42b8c93759

# 还发现  _sign  加密也用这个md5

```



## 4.5 hook方式(两种，python，js)

```python
# hook 安卓程序函数的两种方式
	-spawn：
    需要在应用程序启动的早期阶段进行 Hook。
    需要访问和修改应用程序的内部状态，例如应用程序的全局变量、静态变量等。
    需要 Hook 应用程序的初始化过程，以实现对应用程序的自定义初始化逻辑。
    需要在应用程序的上下文中执行代码，并与其他模块或库进行交互。
    
    -attach：刚刚写的
    需要对已经运行的应用程序进行 Hook，即动态地连接到正在运行的进程。
    需要在应用程序运行时拦截和修改特定的方法调用。
    需要实时监视和修改应用程序的行为，例如参数修改、返回值篡改等。
    需要对应用程序进行调试和分析，以查找潜在的问题和漏洞。
```

### 4.5.1 attach方案(刚讲了)

```python
import frida
import sys
# 连接手机设备
rdev = frida.get_remote_device()

# 包名：com.che168.autotradercloud
# 车智赢+
session = rdev.attach("车智赢+")  # app名字

# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：com.autohome.ahkit.utils下的
    var SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");

    //替换类中的方法
    SecurityUtil.encodeMD5.implementation = function(str){
        console.log("传入的参数(未加密之前的)：",str);
        var res = this.encodeMD5(str); //调用原来的函数
        console.log("返回值（加密后的字符串）：",res);
        return str;  // 没加密的
    }
});
"""


# -----下面固定---以后不会动
script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()
```

### 4.5.2 spawn方案

```python
# 自动重启app，适用于在应用程序启动的早期阶段进行

import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.che168.autotradercloud"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    // 包.类
    var SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");
    SecurityUtil.encodeMD5.implementation = function(str){
        console.log("明文：",str);
        var res = this.encodeMD5(str);
        console.log("md5加密结果=",res);
        return "305eb636-eb15-4e24-a29d-9fd60fbc91bf";
    }
});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
rdev.resume(pid)
sys.stdin.read()
```

### 4.5.3 hook可以使用js代码写

```python
# 之前用python写的
# 现在可以用js代码写--》attach和spawn
```



```js

// hook代码如下
Java.perform(function () {
    //找到类 反编译的首行+类名：com.autohome.ahkit.utils下的
    var SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");

    //替换类中的方法
    SecurityUtil.encodeMD5.implementation = function(str){
        console.log("传入的参数(未加密之前的)：",str);
        var res = this.encodeMD5(str); //调用原来的函数
        console.log("返回值（加密后的字符串）：",res);
        return str;  // 没加密的
    }
});

// 执行是，选择用attach还是  spwan方案


// attach 方案执行命令：   frida -UF -l 6-hook-pwd-attach.js

// spwan 方案执行命令：  frida -U -f com.che168.autotradercloud -l 6-hook-pwd-attach.js
```


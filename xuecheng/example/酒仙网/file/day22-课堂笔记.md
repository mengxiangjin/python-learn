# 今日内容

# 1 今日目标

```python
# 酒仙网（不涉及到逆向）
	- 手机号密码登录
    - 手机号验证码登录
    - 预约茅台
    
    
# 酒仙网
	adb install  路径/酒仙网-v9.1.13.apk  # 安装到手机上
    
```

# 2 抓包分析

```python
# 1 抓用户名密码登录包
# 2 请求包：
	-请求地址：
    	https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm
    -请求方式
    	post
    -请求头：
    	User-Agent	okhttp/3.14.9
    -请求体：
        appKey	526b9977-be06-38e3-b2f0-da7b41964c09  # uuid--》尝试使用uuid发送请求
        appVersion	9.1.13  # app版本
        areaId	2707        # 地区数字
        channelCode	0       # 固定
        cpsId	tencent     # 腾讯推送
        deviceIdentify	526b9977-be06-38e3-b2f0-da7b41964c09 # 就是appkey，uuid
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        lati	31.088975
        longi	121.58378
        netEnv	wifi
        passWord	lqz12345  # 密码
        pushToken	ArzKycf-0Yqb118FEQiKVjytCvh6ET-jp0pEQzGKmthD  # 不太清楚--》删除再发请求，去掉可以---》固定值---》app有推送功能，推动的token，
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11     
        userName	18953675221  #手机号
        
        
 # 根本没有需要破解的东西，直接使用requests发送请求即可

```

![image-20231110201000963](imgs/day22-课堂笔记.assets/image-20231110201000963.png)

# 3 密码登录

```python
import requests

import uuid


def login_by_password(mobile, password, app_key, device_identify):
    res = requests.post(
        url='https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm',
        data={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "netEnv": "wifi",
            "passWord": password,
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "11",
            "userName": mobile
        },
        headers={
            'secure': 'false',
            'User-Agent': 'okhttp/3.14.9',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        verify=False
    )
    data_dict = res.json()
    print(data_dict)
    token = data_dict['result']['userInfo']['token']
    return token


if __name__ == '__main__':
    app_key = device_identify = uuid.uuid4()
    mobile = '17717823244'
    password = 'lqz1234567'
    login_by_password(mobile, password, app_key, device_identify)

```



# 4 验证码登录

```python
# 1 获取图片验证码接口
	-地址：
    	https://newappuser.jiuxian.com/messages/graphCode.htm
    -请求方式：
    	get
    -请求头：
    	没有特殊的
    -请求参数：
    	appKey	526b9977-be06-38e3-b2f0-da7b41964c09  # uuid
        appVersion	9.1.13
        areaId	2707
        channelCode	0
        cpsId	tencent
        deviceIdentify	526b9977-be06-38e3-b2f0-da7b41964c09
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        lati	31.088975
        longi	121.58378
        mobile	17717823244  # 手机号---》后面咱们验证码登录，跟这个手机号跟验证码匹配的
        netEnv	wifi
        pushToken	ArzKycf-0Yqb118FEQiKVjytCvh6ET-jp0pEQzGKmthD
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        type	4
# 2 验证码登录接口
	-请求地址:
       -https://newappuser.jiuxian.com/user/loginMobileFast.htm
    -请求方式：
    	-post
    -请求头：
    	-无特殊
    -请求体：
    	appKey	526b9977-be06-38e3-b2f0-da7b41964c09
        appVersion	9.1.13
        areaId	2707
        channelCode	0
        cpsId	tencent
        deviceIdentify	526b9977-be06-38e3-b2f0-da7b41964c09
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        lati	31.088975
        longi	121.58378
        mobile	17717823244  # 手机号
        netEnv	wifi
        pushToken	ArzKycf-0Yqb118FEQiKVjytCvh6ET-jp0pEQzGKmthD
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        verifyCode	392092  # 验证码
  

# 3 图片验证码获取

# 4 破解图片验证码的库---》直接破解即可
```

![image-20231110202348110](imgs/day22-课堂笔记.assets/image-20231110202348110.png)



## 4.1 图片验证码破解

```python
# 1 ddddorc 库
# 2 pytesseract库
# 3 muggle_ocr库（麻瓜）
# 4 第三方打码平台
	-云打码，超级鹰
    
# 5 如果打码平台破不了
	-只能人工
    -我们的目标是获取数据---如果登录特别难破--》手动登录---》只需要拿着cookie，token发送请求即可
```

### 4.1.1 ddddocr



### 4.1.2 pytesseract模块

```python
# pytesseract是基于Python的OCR工具， 底层使用的是Google的Tesseract-OCR 引擎，支持识别图片中的文字，支持jpeg, png, gif, bmp, tiff等图片格式

# 需要额外安装软件
#1 win 下载tesseract：
https://github.com/UB-Mannheim/tesseract/wiki
    
#2 一路下一步安装--注意选择语言包支持（注意，要下载语言环境支持）
#3 安装完成后，把安装路径加入到环境变量
	-我的安装路径是：D:\Program Files\Tesseract-OCR
# 4 下载python模块：pytesseract和pillow
pip install pytesseract
pip install Pillow

# 5 代码实现
import pytesseract
from PIL import Image
# 列出支持的语言
print(pytesseract.get_languages(config=''))
print(pytesseract.image_to_string(Image.open('v1.png'), lang='chi_sim+eng'))


### 识别成功率不高
```

![image-20230905182149432](imgs/day22-课堂笔记.assets/image-20230905182149432.png)



### 4.1.3 麻瓜ocr

```python
# 1 直接安装，装不了
pip install muggle-ocr

# 2 使用源码安装（）
	-下载源码，解压
    - 源码路径下一定会有 setup.py
    - python setup.py install # 把这个模块，安装在解释器中
    	-如果这么执行，安装在真实环境中
        -切换到虚拟环境中，在虚拟环境中执行上面的代码
		(venv) D:\爬虫逆向9期\day22\软件\muggle-ocr-1.0.3\muggle-ocr-1.0.3>python setup.py install

    -安装麻瓜，需要有别的模块支持，可以提前先把这俩模块装好(耗时)
    pip install opencv-python
	pip install tensorflow-intel
    
    
# 3 代码演示
import muggle_ocr
from muggle_ocr import ModelType
# 二进制 模式打开文件
with open(r"v2.png", "rb") as f:
    # 方法用于从文件读取指定的字节数
    b = f.read()
# model_type 包含了 ModelType.OCR/ModelType.Captcha 两种
# ModelType.OCR 用于识别普通印刷文本 是ModelType.Captcha 可识别光学印刷文本
sdk = muggle_ocr.SDK(model_type=ModelType.Captcha)
text = sdk.predict(image_bytes=b)
print(text)
```

### 4.1.4 最终

```python
# 建议：直接使用打码平台----》免费的识别率都不高
	-超级鹰
```

## 4.2 代码实现验证码登录

```python
import requests
import uuid
import base64
import ddddocr


def fetch_image_code(mobile, app_key, device_identify):
    res = requests.get(
        url="https://newappuser.jiuxian.com/messages/graphCode.htm",
        params={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "type": "4"
        },
        headers={
            "secure": "false",
            "Accept-Encoding": "gzip",
            'user-agent': "okhttp/3.14.9",
            'Host': "newappuser.jiuxian.com",
            'Connection': "keep-alive"
        },
        verify=False
    )

    image_str = res.json()['result']["imgCode"]

    img = base64.b64decode(image_str)

    ocr = ddddocr.DdddOcr(show_ad=False)
    code = ocr.classification(img)
    return code


def check_image_code(mobile, code, app_key, device_identify):
    res = requests.get(
        url='https://newappuser.jiuxian.com/messages/mobileCode.htm',
        params={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "code": code,
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "type": "1"
        },
        verify=False
    )
    data_dict = res.json()

    # {'result': '', 'errCode': '', 'success': '1', 'errMsg': ''}
    # {'result': '', 'errCode': '1200013', 'success': '0', 'errMsg': '验证码输入错误'}
    # print(data_dict)
    return data_dict.get('success') == "1"


def login_by_sms(mobile, sms_code, app_key, device_identify):
    res = requests.post(
        url="https://newappuser.jiuxian.com/user/loginMobileFast.htm",
        data={
            "appKey": app_key,
             "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "mobile": mobile,
            "netEnv": "wifi",
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "verifyCode": sms_code
        },
        verify=False
    )
    # {"result":"","errCode":"1200003","success":"0","errMsg":"验证码错误或已过期，请重新输入"}
    # {"result":{...},"errCode":"1200093","success":"1","errMsg":"初始化密码"}
    # {"result":{...},"errCode":"","success":"1","errMsg":""}
    data_dict = res.json()
    return data_dict.get("success") == "1", data_dict.get('result')


def run():
    mobile = "17717823244"
    app_key = device_identify = str(uuid.uuid4())
    while True:
        # 获取图片验证码
        img_code = fetch_image_code(mobile, app_key, device_identify)
        # 发送手机验证码---》如果图片验证码错了，这个接口发不成功
        status = check_image_code(mobile, img_code, app_key, device_identify)
        if status:
            break
    # 手机就能收到验证码了---》手动输入
    # 接码平台
    sms_code = input("请输入验证码：")

    status, data_dict = login_by_sms(mobile, sms_code, app_key, device_identify)
    if not status:
        print("登录失败")
        return
    print("登录成功")
    print(data_dict)


if __name__ == '__main__':
    run()


'''
{'userInfo': {'apiVersion': 1.0, 'areaId': 500, 'channelCode': '0', 'isClubUser': False, 'isNewUser': False, 'loginUnionFirst': 0, 'loginWay': 2, 'mobile': '18953675221', 'needBindMobile': False, 'rank': 1, 'rankName': '酒虫', 'sex': 0, 'token': '6494ac1cd90b462fbd3c953a69a70861210440860', 'uid': 210440860, 'uname': 'jxw485893769', 'userImg': 'https://misc.jiuxian.com/img/usercenter/sbbgg.jpg'}}

'''
```



# 5 登录+预约茅台

```python
# 1 必须登录成功后才能预约
# 2 抓预约包
	-地址：
    	https://newappuser.jiuxian.com/reservation/preReservation.htm
    -请求方式:
        get
   	-请求参数：
        actId	1907
        appKey	526b9977-be06-38e3-b2f0-da7b41964c09 # uuid
        appVersion	9.1.13
        areaId	2707
        channel	1
        channelCode	0
        cpsId	tencent
        deviceIdentify	526b9977-be06-38e3-b2f0-da7b41964c09
        deviceType	ANDROID
        deviceTypeExtra	0
        equipmentType	Pixel 2 XL
        lati	31.088975
        longi	121.58378
        netEnv	wifi
        productId	626626
        pushToken	ArzKycf-0Yqb118FEQiKVjytCvh6ET-jp0pEQzGKmthD
        screenReslolution	1440x2712
        supportWebp	1
        sysVersion	11
        token	4635e62cb1ef48749bf72079547adc2b210440860 # 这个token就是登录后的token
```

![image-20231110210408975](imgs/day22-课堂笔记.assets/image-20231110210408975.png)



## 6.2 登录+预约实现

```python
import requests

import requests
import uuid


def login_by_pwd(mobile, password, app_key, device_identify):
    res = requests.post(
        url="https://newappuser.jiuxian.com/user/loginUserNamePassWd.htm",
        data={
            "appKey": app_key,
            "appVersion": "9.1.13",
            "areaId": "2707",
            "channelCode": "0",
            "cpsId": "tencent",
            "deviceIdentify": device_identify,
            "deviceType": "ANDROID",
            "deviceTypeExtra": "0",
            "equipmentType": "Pixel 2 XL",
            "netEnv": "wifi",
            "passWord": password,
            "screenReslolution": "1440x2712",
            "supportWebp": "1",
            "sysVersion": "10",
            "userName": mobile
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "secure": "false",
        },
        verify=False
    )
    data_dict = res.json()

    token = data_dict['result']['userInfo']['token']
    return token


def pre_reservation(token, app_key, device_identify):
    res = requests.get(
        url="https://newappuser.jiuxian.com/reservation/preReservation.htm",
        params={
            'actId': '1810',
            'appKey': app_key,
            'appVersion': '9.1.13',
            'areaId': '2707',
            'channel': '1',
            'channelCode': '0',
            'cpsId': 'tencent',
            'deviceIdentify': device_identify,
            'deviceType': 'ANDROID',
            'deviceTypeExtra': '	0',
            'equipmentType': 'Pixel 2 XL',
            'lati': '31.088975',
            'longi': '121.58378',
            'netEnv': 'wifi',
            'productId': '626626',
            # 'pushToken': 'AsLMhsufh3YEmpzPv3S5nHhv0pxuModssTVXvf1TSIsp',
            'screenReslolution': '1440x2712',
            'supportWebp': '1',
            'sysVersion': '11',
            'token': token
        },
        verify=False

    )

    data_dict = res.json()
    print(data_dict)


def run():
    app_key = device_identify = str(uuid.uuid4())
    mobile = "18953675221"
    password = "Lqz12345"
    token = login_by_pwd(mobile, password, app_key, device_identify)
    print(token)

    pre_reservation(token, app_key, device_identify)


if __name__ == '__main__':
    run()


 '''
 {'result': {'verificationState': False}, 'errCode': '1200601', 'success': '0', 'errMsg': '您已预约成功，不需重复预约'}
 
 '''

```





# 6 frida反调试绕过

```python
# 1 之前做识货---》有frida反调试---》打印so文件---》删除so文件方式---》一种方案
# 2 有些app，在运行时，会检测手机中，有没有frida的进程，frida特征(产生一些文件)-->检测到就闪退
Frida的Hook
    - 正常去运行APP，无额外的其他特征
    - 正常去运行APP + 运行frida进行Hook【在手机上会生成一个文件】
    有些app内部监测是否有这个文件，如果有这个文件，那么就让app强制停止
    
    
# 3 绕过第二种检测，网上有个开源第三方---》就是把frida名字和生成的文件，改了名字

# 4 地址：https://github.com/hzzheyang/strongR-frida-android/releases

# 5 咱么下载的strongR-frida-android（hluda）--就是frida
	-以后咱们在手机端运行 frida-server，就不运行原来的了，现在就运行hluda即可
    -python代码跟之前完全一样
    
    -hluda就是对frida-server的一个包装，屏蔽了frida
    
    
# 6 查看手机设备信息
adb shell getprop ro.product.cpu.abi
arm64-v8a

# 7 重要：下载版本要跟python模块版本对应
# 8 下载后解压--》推送到手机上
	adb push  电脑端的hulada   /data/local/tmp/hulada
    
# 9 加入执行权限
	ls -al # 查看当前文件夹下文件的相信信息
    chmod 755 hulada  # 加入执行权限，它才能执行
    
    
# 10 启动（以后不需要启动frida-server了）
./hulada

# 11 后续，电脑端，端口转发，写代码hook即可
# import frida
#
# # 获取设备信息
# rdev = frida.get_remote_device()
#
# # 枚举所有的进程
# processes = rdev.enumerate_processes()
# for process in processes:
#     print(process)
#
# # 获取在前台运行的APP
# front_app = rdev.get_frontmost_application()
# print(front_app)
```

![image-20231110213101898](imgs/day22-课堂笔记.assets/image-20231110213101898.png)



![image-20231110213350443](imgs/day22-课堂笔记.assets/image-20231110213350443.png)

![image-20231110214300615](imgs/day22-课堂笔记.assets/image-20231110214300615.png)

# 7 脱壳

## 7.1 加壳原理

```python
#  安卓开发  apk包
java语法+安卓sdk(context,TextView)+JNI----->打包成了apk---》实际上apk中：
	-一堆dex---》java代码编译后的产物
    -lib文件夹--》so文件---》JNI开发，c语言的产物
    -声音文件，图片文件，xml文件---》资源文件
这种方式打包后---》只需要把apk拖到jadx中，就可以反编译了，因为没有加壳
    
一些小公司：没有很强的加密实力，混淆能力弱---》为了加强apk的安全性，选择加壳


越大厂越不加壳，越小厂越爱加，加壳会使执行速度变慢，apk越大会越慢


# 加壳后，使用jadx打开，搜不到东西了

# 小厂不具备自己加壳的能力---》把apk开发完---》使用第三方加壳软件--》加个壳
	-邦邦加固
    -360
    -腾讯
    
    
# 加壳原理
	java开发的代码---》编译成dex---》使用 加壳软件---》把dex，加载到so中----》使用jadx打开，反编译不了so---》会发现反编译代码补全，没有（反编译不出来）
    
# 加壳后，apk能正常执行吗？
	apk启动---》先把apk所有资源加载到内存中----在内存中执行原来加壳的反向代码---》从so中把所有dexload出来，放到内存中---》app在运行的时候，由于dex已经解到了内存中---》app正常运行
    
    
# 明白了原理---》脱壳，方案好多
#### 手动脱壳：
    通过动态调试so，跟踪计算Dex源文件的内存偏移地址，从内存中Dump出Dex文件
    难度大，寄存器，汇编，反调试，反读写
# 工具脱壳：
    HOOK技术/内存特征寻找
    简单易操作
    基于xposed 脱壳工具（hook工具）：
        Fdex2：Hook ClassLoader loadClass方法 通用脱壳
        dumpDex：https://github.com/WrBug/dumpDex
    基于frida的脱壳工具（hook工具）：
        frida-dexdump：https://github.com/hluwa/FRIDA-DEXDump
# 其它    
自己定制脱壳机（后面会学）
armPro收费脱壳（很贵--》把apk给他--》花钱--》它给你脱完--》把dex给你）
	
    
    
# 今天先学 frida-dexdump---》原理是---》把apk加载到内存---》只要加载到内存执行---》原来的加壳软件会执行脱壳（把dex文件释放到内存中）---》这个软件可以去内存中找出所有的dex，下载到电脑上---》于是就实现了脱壳


```

## 7.2 使用步骤

```python
# 1【手机端】 必须有frida-server在手机端运行  （hulada还是frida-server，一样的）
# 2 【电脑端】端口转发
# 3 【电脑端】电脑端需要一个模块
	pip install frida-dexdump
    
# 4 电脑端执行脱壳命令
frida-dexdump -d -U -f com.jiuxianapk.ui

# 5 从手机内存中下载了很多dex---》java编译后的dex
# 6 使用jadx打开这堆dex即可
	-这里可能会有问题---》jadx直接报错了，无法正常反编译
    -下载的很多dex，有可能有空的，有的可能有错---》使用jadx打开，它就报错
    -笨办法：一个个往里拖动，拖到那个报错，就把那个删掉



```




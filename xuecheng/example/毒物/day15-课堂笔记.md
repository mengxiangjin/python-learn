# 今日内容

# 1 今日目标

```python
# 得物app
	-采集首页推荐信息
# 版本选择
	-4.74.5版本
```

![image-20231013200415647](imgs/day15-课堂笔记.assets/image-20231013200415647.png)



# 2 绕过强制更新

```python
# 1 先断网
# 2 打开app
# 3 连接网络

```



![image-20231013200531328](imgs/day15-课堂笔记.assets/image-20231013200531328.png)

# 3 抓包(反代理)

```python
#  1 该app进制了手机端代理，需要使用SocksDroid代理
	-切记：一定要把之前配置的手机代理删除
#  2 打开charles，抓包
	
    
    
 # 3 分析接口
	-地址：https://app.dewu.com/sns-rec/v1/recommend/all/feed
    -请求方式：get
    -请求头：都可以删除，只剩	X-Auth-Toke
        User-Agent	duapp/4.74.5(android;11)
        X-Auth-Toke # 不能删，需要携带

    
    -请参数：
        lastId	 # 空：第一页 或 1：继续加载
        limit	20 # 每次显示多少条
        newSign	178d802feef18d6a75caad8c048e10cf # 像加密的，测试可以删除，但是必须破，否则后续的完成不了
        -----以下的都可以不携带-----
        abType	social_brand_strategy_v454
        abValue	1
        deliveryProjectId	0
        abVideoCover	2
        abRectagFengge	0
        abRecReason	0
    -请求体：无
    
    
    
 # 4 分析完，我们破解目标
	-newSign
    -X-Auth-Token
```

![image-20231013201001366](imgs/day15-课堂笔记.assets/image-20231013201001366.png)

# 4 破解newSigin(难)

## 4.1 反编译app

```python
# 1 把 得物app ，拖到 jadx中，搜索   "newSign
	-发现 addQueryParameter比较像
    -QueryParameter名字就是请求地址中问号后面的东西
    -大胆猜测，就是它----》后面要做hook验证
    
# 2 分析host.addQueryParameter("newSign", RequestUtils.c(hashMap2, currentTimeMillis));
# 3 调用了RequestUtils.c，传了两个参数进去
# 4 写个hook脚本，测试是否走了这个c
	-通过写hook脚本，确认走了这个c
```

![image-20231013201954186](imgs/day15-课堂笔记.assets/image-20231013201954186.png)

## 4.2 hook-RequestUtils.c

```python
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")   # 老版本叫： 得物(毒)    新版本：  得物

scr = """
Java.perform(function () {
    var RequestUtils = Java.use("com.shizhuang.duapp.common.utils.RequestUtils");
    RequestUtils.c.implementation = function(map,j){
        console.log("----------------------------------------");
        console.log('1.参数字典为：',map); // 此处直接打印map，发现打印的是对象，我们需要转换一下
        console.log('2.参数字典类型为：',JSON.stringify(map));  // 查看一下类型 ：java.util.HashMap
        // 以下是固定格式
        var Map = Java.use('java.util.HashMap');
        var obj = Java.cast(map, Map);
        console.log('3.参数字典转成字符串类型为：',obj.toString());
        var res = this.c(map,j);
        console.log("4.newSign结果：", res);
        return res;
    }
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()



'''
1.参数字典为： [object Object]
2.参数字典类型为： "<instance: java.util.Map, $className: java.util.HashMap>"
3.参数字典转成字符串类型为： {abValue=1, deliveryProjectId=0, abRectagFengge=0, abType=social_brand_strategy_v454, limit=20, lastId=, abRecReason=0, abVideoCover=2}
4.newSign结果： e8b28920d828c467800ff6076267c4ed
'''
```

## 4.3 分析RequestUtils.c--java源码--干了5个事

```java
public static synchronized String c(Map<String, String> map, long j2) throws UnsupportedEncodingException {
    synchronized (RequestUtils.class) {
        PatchProxyResult proxy = PatchProxy.proxy(new Object[]{map, new Long(j2)}, null, changeQuickRedirect, true, 6612, new Class[]{Map.class, Long.TYPE}, String.class);
        if (proxy.isSupported) {
            return (String) proxy.result;
        } else if (map == null) {
            return "";
        } else {
            //1 往map中放了很多 key-value
            map.put("uuid", DuHttpConfig.d.getUUID());
            map.put("platform", "android");
            map.put("v", DuHttpConfig.d.getAppVersion());
            map.put("loginToken", DuHttpConfig.d.getLoginToken());
            map.put("timestamp", String.valueOf(j2));
            //2 把上面的map放到arrayList中，做排序
            ArrayList arrayList = new ArrayList(map.entrySet());
            Collections.sort(arrayList, new Comparator<Map.Entry<String, String>>() {
                public static ChangeQuickRedirect changeQuickRedirect;
                @Override
                public int compare(Map.Entry<String, String> entry, Map.Entry<String, String> entry2) {
                    PatchProxyResult proxy2 = PatchProxy.proxy(new Object[]{entry, entry2}, this, changeQuickRedirect, false, 6618, new Class[]{Map.Entry.class, Map.Entry.class}, Integer.TYPE);
                    return proxy2.isSupported ? ((Integer) proxy2.result).intValue() : entry.getKey().toString().compareTo(entry2.getKey());
                }
            });
            // 3 把上面的arraylist中的内容，拼接到sb中，转成字符串
            StringBuilder sb = new StringBuilder();
            for (int i2 = 0; i2 < arrayList.size(); i2++) {
                Map.Entry entry = (Map.Entry) arrayList.get(i2);
                sb.append(((String) entry.getKey()) + ((String) entry.getValue()));
            }
            String sb2 = sb.toString();
            DuHttpConfig.LogConfig logConfig = DuHttpConfig.f15800h;
            String str = f16243a;
            // 4 调用了AESEncrypt.encode，把sb2传入，做了加密
            // 5 把加密后的结果，调用a(加密结果)--》返回结果返回了
            return a(AESEncrypt.encode(DuHttpConfig.f15796c, sb2));
        }
    }
}



/*
// 1 参数拼接
// 把uuid，platform，v，loginToken，timestamp放入map中
map.put("uuid", DuHttpConfig.d.getUUID());
map.put("platform", "android");
map.put("v", DuHttpConfig.d.getAppVersion());
map.put("loginToken", DuHttpConfig.d.getLoginToken());
map.put("timestamp", String.valueOf(j2));

//2 把map转成ArrayList，并进行排序
ArrayList arrayList = new ArrayList(map.entrySet());
Collections.sort(arrayList, new Comparator<Map.Entry<String, String>>()

// 3 构建字符串
StringBuilder sb = new StringBuilder();
sb.append()

// 4 执行AESEncrypt.encode 加密 
AESEncrypt.encode(DuHttpConfig.f15796c, sb2)

// 5 把返回结果当参数传入a中
a(AESEncrypt.encode(DuHttpConfig.f15796c, sb2));

*/


```

## 4.4 看a方法，干了什么事情

```java
public static String a(String str) {
    try {
        MessageDigest messageDigest = MessageDigest.getInstance("MD5");
        messageDigest.update(str.getBytes());
        byte[] digest = messageDigest.digest();
        StringBuilder sb = new StringBuilder();
        for (byte b2 : digest) {
            String hexString = Integer.toHexString(b2 & 255);
            while (hexString.length() < 2) {
                hexString = "0" + hexString;
            }
            sb.append(hexString);
        }
        return sb.toString();
    } catch (NoSuchAlgorithmException e2) {
        e2.printStackTrace();
        return "";
    }
}
// 进行md5加密--》转成16进制返回，就是python中的
import hashlib
md5=hashlib.md5()
md5.update(str) // str是加密后的字符串
print(md5.hexdigest())

```

## 4.5 AESEncrypt.encode

```java
public class AESEncrypt {
    static {
        System.loadLibrary("JNIEncrypt");   // libJNIEncrypt.so
    }
	// 调用 java中的encode---》调用了c中jni开发的getByteValues，得到结果，java处理---》处理完后又调用了---》调用了c中jni开发的encodeByte
   public static String encode(Object obj, String str) {
        String byteValues = getByteValues();
        StringBuilder sb = new StringBuilder(byteValues.length());
        for (int i2 = 0; i2 < byteValues.length(); i2++) {
            if (byteValues.charAt(i2) == '0') {
                sb.append('1');
            } else {
                sb.append('0');
            }
        }
       
        return encodeByte(str.getBytes(), sb.toString());
    }

	public static native String encodeByte(byte[] bArr, String str);
    public static native String getByteValues();
}

/*
1 接下来：看getByteValues() 返回结果是什么
2 hook--》getByteValues看返回结果是什么
	-返回了一堆0101010101
3 后续操作是对返回的一堆010101取反
*/
```

## 4.6 hook--查看getByteValues返回结果

```python
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
    var AESEncrypt = Java.use("com.duapp.aesjni.AESEncrypt");
    AESEncrypt.getByteValues.implementation = function(){
        var res = this.getByteValues();
        console.log('getByteValues返回值是：',res);
        return res;
    }
});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()

'''
getByteValues返回值是： 101001011101110101101101111100111000110100010101010111010001000101100101010010010101110111010011101001011101110101100101001100110000110100011101010111011011001101001101011101010100001101000011


'''
```

## 4.7 hook--AESEncrypt.encode查看参数和返回值

```python
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
    var AESEncrypt = Java.use("com.duapp.aesjni.AESEncrypt"); // encode是重载的方法，has more than one overload
    AESEncrypt.encode.overload('java.lang.Object', 'java.lang.String').implementation = function(obj,str){
        console.log('传入参数：',str);
        var res = this.encode(obj,str);
        console.log('返回值是：',res);
        return res;
    }
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()


'''
传入参数： loginTokenplatformandroidtimestamp1697201773755type1uuidaa39fda5dfb88d79v4.74.5
返回值是： knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs2z+72ySMAfAi1gCqQ7GVt4PrqncoUeLg4GM7WhIQc3UiduzaB/+e6vW/0+waWYbMQ=


需要知道：这堆参数：loginTokenplatformandroidtimestamp1697201773755type1uuidaa39fda5dfb88d79v4.74.5
是通过什么加密方式得到了（base64编码的）：
knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs2z+72ySMAfAi1gCqQ7GVt4PrqncoUeLg4GM7WhIQc3UiduzaB/+e6vW/0+waWYbMQ=

上面的base64编码的字符串---》md5---》得到了newSign

'''
```

## 4.8 查看encodeByte(str.getBytes(), sb.toString())是如何实现

```python
# 0 调用：encodeByte，传入了
str:loginTokenplatformandroidtimestamp1697201773755type1uuidaa39fda5dfb88d79v4.74.5
sb:010100101010101取反了，固定的
返回了加密
# 1 encodeByte是jni开发的，用c语言开发的---》需要去看它的c源码--》libJNIEncrypt.so

# 2 使用ida打开这个so文件--》libJNIEncrypt.so--》查看exports--》查看so文件中有哪些函数
	-看32位的so文件

# 3 发现它是动态注册---》找JNI_OnLoad
jint JNI_OnLoad(JavaVM *vm, void *reserved)
{
  # jclass clazz = (*env)->FindClass(env, "com/justin/s9day11/Dynamic");
  v4 = (*(__int64 (__fastcall **)(__int64, const char *))(*(_QWORD *)v6[0] + 48LL))(
         v6[0],
         "com/duapp/aesjni/AESEncrypt");
  #int res = (*env)->RegisterNatives(env, clazz, gMethods,2); 
    (*env)->RegisterNatives(v3, v4, off_15010, 8LL); #  动态注册的对应关系在off_15010函数中
  return v2;
}

# 4 双击 off_15010 查看它的汇编，找到java中encodeByte对应c中encode，有两个参数(bytes,字符串)，返回一个参数字符串


# 5 查看encode的代码---》双击--》按f5--》引入头文件--》扣出核心代码
  v11[v9] = 0;
  v18 = (const char *)AES_128_ECB_PKCS5Padding_Encrypt(v11, v8); # 得到了v18，要返回的字节数组
  return a1->functions->NewStringUTF(a1, v18); # v18 要返回的字节数组


# 6 AES_128_ECB_PKCS5Padding_Encrypt
__int64 __fastcall AES_128_ECB_PKCS5Padding_Encrypt()
{
  return AES_128_ECB_PKCS5Padding_Encrypt();
}

# 7 AES_128_ECB_PKCS5Padding_Encrypt--》核心代码
 v24 = v10;
  v25 = (char *)malloc(v10);
  v26 = v25;
  if ( v10 >= 16 )
  {
    v27 = (unsigned int)(v10 / 16);
    v28 = v8;
    v29 = v25;
    do
    {
      AES128_ECB_encrypt(v28, a2, v29);  # 循环执行AES128_ECB_encrypt，猜测是aes加密
      v29 += 16;
      --v27;
      v28 += 16;
    }
    while ( v27 );
  }
  v30 = b64_encode(v26, v24); # 看到了把某个字节数组用base64编码，返回了
  return v30;

# 8 我们看了代码后猜测是：aes加密---》结果使用base64编码
	1 aes明文是什么：
    2 秘钥是什么：
    3 自己使用python实现---》跟hook得到的结果比较，如果一样，说明我们猜的是对的
```



![image-20231013210215755](imgs/day15-课堂笔记.assets/image-20231013210215755.png)



![image-20231013210831639](imgs/day15-课堂笔记.assets/image-20231013210831639.png)

## 4.9 hook--so文件中方法--AES_128_ECB_PKCS5Padding_Encrypt

```python

# AES_128_ECB_PKCS5Padding_Encrypt
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
    var addr_func = Module.findExportByName("libJNIEncrypt.so", "AES_128_ECB_PKCS5Padding_Encrypt");
    Interceptor.attach(addr_func, {
        onEnter: function(args){
            console.log("--------------------------执行函数--------------------------");
            console.log("参数1：", args[0].readUtf8String());
            console.log("参数2：", args[1].readUtf8String());
        },
        onLeave: function(retValue){
            console.log("返回值:", retValue.readUtf8String());
        }

    })

});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()

'''
参数1： loginTokenplatformandroidtimestamp1697205035151uuidaa39fda5dfb88d79v4.74.5 # 明文
参数2： d245a0ba8d678a61  # aes加密的key是不变的
返回值: knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs21LrJ4Sf9GuQtUccnsVJEi1vorD9tdMeNnuNWK5OEpBP7lpjYe+SgKMSgHMdPJ/DU=
# 验证了，拿着明文，拿着秘钥，通过aes加密--》使用 base64编码---》得到返回值
knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs21LrJ4Sf9GuQtUccnsVJEi1vorD9tdMeNnuNWK5OEpBP7lpjYe+SgKMSgHMdPJ/DU=
'''


# 明文
loginToken # 空的
platform android # 固定的
timestamp 1697205035151# 时间戳
uuid aa39fda5dfb88d79 # 不知道怎么来的  16进制的手机设备id
v 4.74.5 # 固定的版本号
```

## 4.9 破解uuid

```python
# 1 map.put("uuid", DuHttpConfig.d.getUUID());


# 2  DuHttpConfig.d.getUUID()--->PatchProxyResult-->看不懂
public String getUUID() {
    PatchProxyResult proxy = PatchProxy.proxy(new Object[0], this, changeQuickRedirect, false, 5097, new Class[0], String.class);
    return proxy.isSupported ? (String) proxy.result : "";
}

# 3 想办法
	-1 固定uuid试试  aa39fda5dfb88d79-->是可以的
    -2 项目uuid应该是一样的---》别的位置找到uuid的生成，拿过来用试试
# 4 后来 破 X-Auth-Token 发现也有uuid---》看那个uuid能看懂---》使用那个试试
	-hashMap.put("uuid", HPDeviceInfo.b(BaseApplication.c()).a((Activity) null));
# 5 HPDeviceInfo.b(参数).a(参数)--》查看a
public String a(Activity activity) {
    String str = this.f15203b;  # 从内存中取出某个值---》重要项目不重启，这值是固定的
    if (str != null) {
        return str;
    }
    if (activity != null) {
        final TelephonyManager telephonyManager = (TelephonyManager) activity.getApplication().getSystemService("phone");
        new RxPermissions(activity).c("android.permission.READ_PHONE_STATE").subscribe(new Consumer() { 
            @Override // io.reactivex.functions.Consumer
            public final void accept(Object obj) {
                # 获取手机设备id号
                HPDeviceInfo.this.a(telephonyManager, (Boolean) obj);
            }
        });
    } else {
        this.f15203b = a();
    }
    return this.f15203b;
}

### python 生成手机设备id号
def gen_imei():
    # 这个不够标准
    return "".join(random.choices('0123456789abcdef', k=15))
```

## 4.10 整合代码-得到newSign

```python
import time
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus
import base64
import json
import random
import copy


def create_android_id():
    data_list = []
    for i in range(1, 9):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return "".join(data_list).lower()


def md5(data_bytes):
    hash_object = hashlib.md5()
    hash_object.update(data_bytes)
    return hash_object.hexdigest()


def aes_encrypt(data_string):
    key = "d245a0ba8d678a61"
    aes = AES.new(
        key=key.encode('utf-8'),
        mode=AES.MODE_ECB,
    )
    raw = pad(data_string.encode('utf-8'), 16)
    return aes.encrypt(raw)


uid = create_android_id()
ctime = str(int(time.time() * 1000))

reply_param_dict = {
    "lastId": "1",
    "limit": "20",
}

new_dict = copy.deepcopy(reply_param_dict)
new_dict.update(
    {"loginToken": "", "platform": "android", "timestamp": str(int(time.time() * 1000)), "uuid": uid, "v": "4.74.5"}
)
ordered_string = "".join(["{}{}".format(key, new_dict[key]) for key in sorted(new_dict.keys())])

aes_string = aes_encrypt(ordered_string)
aes_string = base64.encodebytes(aes_string)
aes_string = aes_string.replace(b"\n", b"")
sign_string = md5(aes_string)
print(sign_string)



### 总结
1 通过字符串loginToken platform timestamp uuid v
2 进行aes加密，秘钥是d245a0ba8d678a61
3 把结果用base64编码
4 把base64编码的结果使用md5加密
```





# 5 破解 X-Auth-Token

```python
# 1 反编译--搜索 X-Auth-Token
# 2 找到：hashMap.put("X-Auth-Token", ServiceManager.a().getJwtToken());
	-看到了其他请求都，添加到map中了
    
# 3 ServiceManager.a().getJwtToken()

# 4 String getJwtToken();  进行不下去了

# 5 x-auth-token到底是什么---》token串---》典型的三段式--》用来做前后端登录认证的
	-即便不登录，也有token串，三段都是使用base64编码---》base64解码
Bearer 

eyJhbGciOiJSUzI1NiJ9.  # 头


eyJpYXQiOjE2OTcxOTg3MDYsImV4cCI6MTcyODczNDcwNiwiaXNzIjoiYWEzOWZkYTVkZmI4OGQ3OSIsInN1YiI6ImFhMzlmZGE1ZGZiODhkNzkiLCJ1dWlkIjoiYWEzOWZkYTVkZmI4OGQ3OSIsInVzZXJJZCI6MTkyMjE2ODYzOCwidXNlck5hbWUiOiLlvpfniallci1DMUkzUDdMNyIsImlzR3Vlc3QiOnRydWV9.  # 荷载


Z-RMvetpgBdkh4TbOuEZQOBHsEKU3cYo1_18WzWij3VK_6waCY2fqMDrilMT2bQT3PFF5bCyg1gASO_Qw4-zzGvBKKrpyA6VKCPZe3QnhFd5dJ8WyD9-06AwBvpapuGgbfFel-lUCw0dK2Fq6mEh3zyVy9zgz-z2VMwwkqeh9aVxswqOK40gsD20L_ySVPOUg9QnjtrnK5P78HgR3gHmlQS2CNIUGDm1kPyniQlkdLI7yO1y0pD-r75amFcozvxpGLwWJd3B79y0XU37GSVDVNxuc0q9kjU0OSbtZ0GE4xiXCdE6_tIBdVDsayOdtRcLjdvGma_HjAK4TV7WvokzJw  # 签名


# 6 token串都是后端生成，返回给前端的
	一定是app一启动，向后端发送一个请求，获得到了这个token串
    
    
# 7 抓包，查看，那个请求获得token（清空app缓存，再抓）

	请求地址：https://app.dewu.com/api/v1/app/user_core/users/getVisitorUserId
    请求方式：post
    请求头：
        duv	4.74.5
        duloginToken	
        dudeviceTrait	Pixel+2+XL
        dudeviceBrand	google
        timestamp	1697206819966
        shumeiid	20231013222019b717ec769d0f04ac4f5207c9f95fe8e600dfeb39335ca0c2
        oaid	
        User-Agent	duapp/4.74.5(android;11)
    请求参数：无
    请求体：
    {
        "loginToken": "",
        "newSign": "8b471539ad8ef3dbffa7b2ce4cd9b4d8",
        "platform": "android",
        "timestamp": "1697206819966",
        "uuid": "aa39fda5dfb88d79",
        "v": "4.74.5"
    }
```

![image-20231013220646623](imgs/day15-课堂笔记.assets/image-20231013220646623.png)



![image-20231013221800291](imgs/day15-课堂笔记.assets/image-20231013221800291.png)



## 5.1 使用python获取x-auth-token

```python
import time
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus
import base64
import json
import random


def create_android_id():
    data_list = []
    for i in range(1, 9):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return "".join(data_list).lower()


def md5(data_bytes):
    hash_object = hashlib.md5()
    hash_object.update(data_bytes)
    return hash_object.hexdigest()


def aes_encrypt(data_string):
    key = "d245a0ba8d678a61"
    aes = AES.new(
        key=key.encode('utf-8'),
        mode=AES.MODE_ECB,
    )
    raw = pad(data_string.encode('utf-8'), 16)
    return aes.encrypt(raw)


uid = create_android_id()
ctime = str(int(time.time() * 1000))

param_dict = {"loginToken": "", "platform": "android", "timestamp": ctime, "uuid": uid, "v": "4.74.5"}

ordered_string = "".join(["{}{}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])
aes_string = aes_encrypt(ordered_string)
aes_string = base64.encodebytes(aes_string)
aes_string = aes_string.replace(b"\n", b"")
sign = md5(aes_string)
param_dict['newSign'] = sign

res = requests.post(
    url="https://app.dewu.com/api/v1/app/user_core/users/getVisitorUserId",
    headers={
        "duuuid": uid,
        "duimei": "",
        "duplatform": "android",
        "appId": "duapp",
        "timestamp": ctime,
        'duv': '4.74.5',
        'duloginToken': '',
        'dudeviceTrait': 'Pixel+2+XL',
        'shumeiid': '202308011759568af1c8fc75c211e7f876664d9493202d0055aeeb3dd6e38c',
        'User-Agent': 'duapp/4.74.5(android;11)'

    },
    json=param_dict,
    verify=False
)
print(res.headers)
x_auth_token = res.headers['X-Auth-Token']
print(x_auth_token)

# Bearer eyJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2OTcyMDY4NzQsImV4cCI6MTcyODc0Mjg3NCwiaXNzIjoiZDBmYWVjMzU5ZDdjOTAxMiIsInN1YiI6ImQwZmFlYzM1OWQ3YzkwMTIiLCJ1dWlkIjoiZDBmYWVjMzU5ZDdjOTAxMiIsInVzZXJJZCI6MjAxMjA0MDUzNiwiaXNHdWVzdCI6dHJ1ZX0.FHV-XOcmrNlS3dr4MxXEQpih9gwwIrYDHQMisL2y25yX66YGXHyb6SsJLnuf2QLUDJ-Vwg1XOuRc9je7g6V34tx_MOBn9v-lhR0ba9qySaL16r7kX4-eBRS2ewUXNuPJtI_F7dTCB83IB6vdjT6biP7dhuY0c4E1d-4hdhGw76RsNiBpA0hog5AvI8fe93LbeUiXVBxbq0bgEza4LWg0lBjKZuIpF7K48E-cUXD1dbiASDvYKKsncyK9sF6GvAj3-6W9A0ro1X3em68bG3BBDdzZXl_WGhbB3TQiMvIXqOatZLAiBJQekor8EiQW5OseIoyMzL7fbknkoN2E03MWuA

```



# 6 代码整合

```python
import time
import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus
import base64
import json
import random


def create_android_id():
    data_list = []
    for i in range(1, 9):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return "".join(data_list).lower()


def md5(data_bytes):
    hash_object = hashlib.md5()
    hash_object.update(data_bytes)
    return hash_object.hexdigest()


def aes_encrypt(data_string):
    key = "d245a0ba8d678a61"
    aes = AES.new(
        key=key.encode('utf-8'),
        mode=AES.MODE_ECB,
    )
    raw = pad(data_string.encode('utf-8'), 16)
    return aes.encrypt(raw)


uid = create_android_id()
ctime = str(int(time.time() * 1000))

# param_dict = {"loginToken": "", "platform": "android", "timestamp": ctime, "uuid": uid, "v": "4.84.0"}
param_dict = {"loginToken": "", "platform": "android", "timestamp": ctime, "uuid": uid, "v": "4.74.5"}

ordered_string = "".join(["{}{}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])
aes_string = aes_encrypt(ordered_string)
aes_string = base64.encodebytes(aes_string)
aes_string = aes_string.replace(b"\n", b"")
sign = md5(aes_string)
param_dict['newSign'] = sign

res = requests.post(
    url="https://app.dewu.com/api/v1/app/user_core/users/getVisitorUserId",
    headers={
        "duuuid": uid,
        "duimei": "",
        "duplatform": "android",
        "appId": "duapp",
        "timestamp": ctime,
        'duv': '4.74.5',
        'duloginToken': '',
        'dudeviceTrait': 'Pixel+2+XL',
        'shumeiid': '202308011759568af1c8fc75c211e7f876664d9493202d0055aeeb3dd6e38c',
        'User-Agent': 'duapp/4.74.5(android;11)'

    },
    json=param_dict,
    verify=False
)
x_auth_token = res.headers['X-Auth-Token']

reply_param_dict = {
    "lastId": "1",
    "limit": "20",
    # "newSign": ""
}
import copy

new_dict = copy.deepcopy(reply_param_dict)
new_dict.update(
    # {"loginToken": "", "platform": "android", "timestamp": str(int(time.time() * 1000)), "uuid": uid, "v": "4.84.0"})
    {"loginToken": "", "platform": "android", "timestamp": str(int(time.time() * 1000)), "uuid": uid, "v": "4.74.5"})
ordered_string = "".join(["{}{}".format(key, new_dict[key]) for key in sorted(new_dict.keys())])

aes_string = aes_encrypt(ordered_string)
aes_string = base64.encodebytes(aes_string)
aes_string = aes_string.replace(b"\n", b"")
sign_string = md5(aes_string)
reply_param_dict['newSign'] = sign_string

res = requests.get(
    url="https://app.dewu.com/sns-rec/v1/recommend/all/feed/",
    params=reply_param_dict,
    headers={
        "X-Auth-Token": x_auth_token,
        'User-Agent': 'duapp/4.74.5(android;11)'
    },
    verify=False
)
print(res.text)
```






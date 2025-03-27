# 今日内容

# 1 目标

```python
# B 站---》刷视频播放量--》三天时间
# B站app：6.24.0
# adb install 路径  装到手机上

```

# 2 抓包分析

```python
# 1 打开charles，设置代理，抓取即可
# 2 打开一个视频，抓包

# 3 分析出可以增加播放量的地址：
	-地址：https://api.bilibili.com/x/report/click/android2
    -请求方式：POST
    -请求体：（一堆二进制）
    	ê²Þm	Gf~5g5fÿÂÀÆ¹Õª
        im{A»IA%*:ÅÎmWé	Ì^¤Þ®Ie¬ä×¶cJxÉ!i)ì§÷ýUXùUwJMãîh]-Q¬¡ab"
        dØE·Ò¶ZA6F¢m`¦÷
        îé}Sâ6F¨KÀ+¶3;KyÂñ´Æ #¼äwè³¬^Î.¦VW	*À"Ùý¶~øO¯ññþÈE_=W_lR¤X§¨bèS!ØàKÀ÷ÆîÅÉ!¿Îº4ÎÒ¢f¼¿ÉRKÃ¿¼¹_Iæ¸¥]ÿõàê4mÁòö©5Ïuºø1@
    -请求头：
        buvid	XXCE06EC3F65CE60EE272907EC70BD5A491E7
        device-id	IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow
        fp_local	1d6a9c1ac4f284329263021dc511149f20230817211900c3a671e0d454262812
        fp_remote	1d6a9c1ac4f284329263021dc511149f202308030024054e69106c26213aee5f
        session_id	b0f008ec
```

![image-20231018200623129](imgs/day16-课堂笔记.assets/image-20231018200623129.png)



![image-20231018200757383](imgs/day16-课堂笔记.assets/image-20231018200757383.png)

# 3 请求体加密破解

## 3.0 反编译查找

### 补充：老版本jadx调大内存

```python
# jadx-gui 反编译app的时候内存不足
1.使用记事本或者notpad++打开jadx-gui.bat
2.找到 set DEFAULT_JVM_OPTS="-Xms128M" "-Xmx4g"
3.将其修改为 set DEFAULT_JVM_OPTS="-Xms128M" "-Xmx16g" 后保存就ok了 (你要4g 提升到16g把-Xmx4g改成-Xmx16g)
```





```python
# 1 jadx 打开 apk
# 2 搜索：report/click/android2
# 3 在方法上点右键，查找用例
# 4 找到：代码很难读---》app加入了混淆---》把之前很长的名字---》变成'魔鬼变量'---》jdax支持反混淆
	# 虽然可以反混淆，但是hook的时候，使用的还是反混淆之前的名字---》app在手机中运行的名字，就是 魔鬼变量的名字 
public final void a() {
    c0 create = c0.create(w.d(com.hpplay.sdk.source.protocol.h.E), d.this.H7(this.b.a(), this.b.b(), this.b.h(), i, j2, this.b.n(), this.b.m(), this.b.k(), this.b.c(), this.b.e(), this.b.l(), this.b.f()));

    l<String> execute = ((tv.danmaku.biliplayerimpl.report.heartbeat.a) com.bilibili.okretro.c.a(tv.danmaku.biliplayerimpl.report.heartbeat.a.class)).reportClick(create).execute();
    int b = execute.b();
    String h = execute.h();
}

# 5 咱们之前写过的代码--》比较
	ResponseBody responseBody = retrofit.create(接口类a.class).reportClick(参数).execute().body();
    
# 6 发送post请求，带在请求体中的参数 是 create
	c0 create = c0.create() # c0.create 执行，传入参数，返回的
    # 传入的参数：
    	第一个参数：w.d(com.hpplay.sdk.source.protocol.h.E)---》application/octet-stream--》请求编码格式--》不重要
		第二个参数：d.this.H7(传了一堆参数)
        
# 7 核心就是破解 d.this.H7 方法返回什么---》请求体就是什么

# 8 d.this.H7的源码如下
```

![image-20231018201929956](imgs/day16-课堂笔记.assets/image-20231018201929956.png)



### 3.0.1  d.this.H7的源码

```java
public final byte[] H7(long j2, long j4, int i, long j5, long j6, int i2, int i3, long j7, String str, int i4, String str2, String str3) throws Exception {
    long j8;
    int i5;
    Application f2 = BiliContext.f();
    com.bilibili.lib.accounts.b client = com.bilibili.lib.accounts.b.f(f2);
    AccountInfo h = BiliAccountInfo.f.a().h();
    if (h != null) {
        j8 = h.getMid();
        i5 = h.getLevel();
    } else {
        j8 = 0;
        i5 = 0;
    }
    // 1 把一堆 key  和 value 放到了 TreeMap中
    TreeMap treeMap = new TreeMap();
    treeMap.put("aid", String.valueOf(j2));
    treeMap.put("cid", String.valueOf(j4));
    treeMap.put("part", String.valueOf(i));
    treeMap.put(EditCustomizeSticker.TAG_MID, String.valueOf(j8));
    treeMap.put("lv", String.valueOf(i5));
    treeMap.put("ftime", String.valueOf(j6));
    treeMap.put("stime", String.valueOf(j5));
    treeMap.put("did", com.bilibili.lib.biliid.utils.f.a.c(f2));
    treeMap.put("type", String.valueOf(i2));
    treeMap.put("sub_type", String.valueOf(i3));
    treeMap.put("sid", String.valueOf(j7));
    treeMap.put("epid", str);
    treeMap.put("auto_play", String.valueOf(i4));
    x.h(client, "client");
    if (client.r()) {
        treeMap.put("access_key", client.g());
    }
    treeMap.put("build", String.valueOf(com.bilibili.api.a.f()));
    treeMap.put("mobi_app", com.bilibili.api.a.l());
    treeMap.put("spmid", str2);
    treeMap.put("from_spmid", str3);
    // 2 构建sb对象，把treeMap的内容，拼成字符串了
    // aid=asdfasdf&cid=asadfasd&part=sadfasd&
    StringBuilder sb = new StringBuilder();
    for (Map.Entry entry : treeMap.entrySet()) {
        String str4 = (String) entry.getValue();
        sb.append((String) entry.getKey());
        sb.append('=');
        if (str4 == null) {
            str4 = "";
        }
        sb.append(str4);
        sb.append('&');
    }
    // 3 sb=aid=asdfasdf&cid=asadfasd&part=sadfasd
    sb.deleteCharAt(sb.length() - 1);
    // 4 转成字符串了 aid=asdfasdf&cid=asadfasd&part=sadfasd
    String sb2 = sb.toString();
    // 5 调用： t3.a.i.a.a.a.b.e.b对 aid=asdfasdf&cid=asadfasd&part=sadfasd进行加密，得到字符串
    String b2 = t3.a.i.a.a.a.b.e.b(sb2);
	// 6 sb=aid=asdfasdf&cid=asadfasd&part=sadfasd&sign=加密串
    sb.append("&sign=");
    sb.append(b2);
    String sb3 = sb.toString();
	// 7 对整个字符串：aid=asdfasdf&cid=asadfasd&part=sadfasd&sign=加密串 调用了a加密得到结果
    return t3.a.i.a.a.a.b.e.a(sb3);
}

/*
1 把一堆 key  和 value 放到了 TreeMap中
2 构建sb对象，把treeMap的内容，拼成字符串了
     aid=asdfasdf&cid=asadfasd&part=sadfasd&
3 把字符串最后 & 删除
sb=aid=asdfasdf&cid=asadfasd&part=sadfasd
4 调用： t3.a.i.a.a.a.b.e.b对 aid=asdfasdf&cid=asadfasd&part=sadfasd进行加密，得到字符串
5 把加密后的字符串拼接到 aid=asdfasdf&cid=asadfasd&part=sadfasd 后面
sb=aid=asdfasdf&cid=asadfasd&part=sadfasd&sign=加密串
6 调用t3.a.i.a.a.a.b.e.a(sb3)对 上述字符串加密
7 得到的就是 请求体的内
*/
```



## 3.1 hook查看找的位置是否正确

```python
# 上述分析了一堆代码，但是我们不确定，发送请求时，是否是真正的走了：H7
# 通过hook查看一下
```



```python
# java 的自己数组

v = [-10, -74, -76, 116, 57, 117, -77, -11, -87, 9, 42, -128, -66, -84, 112, 83, -74, 96, 103, -23, 70, -59, -61, 29,
     -90, -46, -83, -109, 24, -12, 52, 69, -18, 108, 101, 48, -40, -72, 82, 53, -62, -41, -98, -99, -12, 113, 103, -57,
     71, 41, -6, -78, -85, -103, 28, 118, 100, 59, 99, 75, 62, -88, -17, -38, -85, 38, 95, -97, 52, 29, 62, -82, 46, 44,
     -82, 95, 67, -127, 36, 84, 67, 12, 86, 6, -56, -41, -20, 6, -17, -94, 27, 96, -49, 81, -4, -66, -1, -117, -64, -62,
     -24, 7, -45, -53, 56, 106, -34, -14, 112, -42, 72, -77, 123, -73, 25, 107, 42, -82, 37, 108, 17, -15, -84, 39, 19,
     1, 51, -24, 54, 25, -97, 18, 90, 87, -115, 44, 116, -90, 6, 35, -50, -101, 102, 117, 57, -1, -20, -2, 59, -114, 29,
     42, 64, -99, 1, -100, 114, -87, -7, 90, 15, 42, -53, -7, 85, -53, -48, -104, -73, 69, 84, 36, 58, 99, 118, 74, -32,
     -54, -98, 56, 109, 71, 81, -96, 21, -11, 67, -123, 60, 76, -13, -34, 100, 87, -44, 122, 93, 47, 16, -22, -35, -120,
     31, -25, -54, -124, 107, 31, 51, -95, -26, -117, -89, -105, 70, 94, -101, 127, 33, 89, -66, 77, -111, -89, -29, 41,
     -62, -94, 115, 81, -98, -42, 114, -74, 31, 71, 97, 79, 63, -15, 12, -29, 10, -124, 71, -69, -125, -20, -76, 78,
     -20, -46, 50, 43, 41, 67, -112, -114, -74, -100, 5, 106, -112, -26, -15, 70, -121, 19, 109, 65, 103, -69, -93, 0,
     123, -54, 32, 105, 94, 122, -91, 38, 4, 98, -63, 15, -111, 4, 53, 83, -32, -54, -58, 12, 57, -33, -9, 32, 94, 4,
     57, -77, -108, 47, -118, -38, -112, 25, -23, -9, 35, -106, 93, 54, 102, -16, -72, -65, -72, 47, -8, 89, -48, 5,
     -29, -79, 4, -122, -78, 44, 75, 17, -36, 1, -111, -72]

# 把java的转成python
l=[]
for i in v:
    if i < 0:
        i = i + 256
    l.append(i)
print(l) # python 的字节数组，转成16进制

res=[ hex(item)[2:] for item in l]
print(res)
print(''.join(res))
# f6b6b4743975b3f5a992a80beac7053b66067e946c5c31da6d2ad9318f43445ee6c6530d8b85235c2d79e9df47167c74729fab2ab991c76643b634b3ea8efdaab265f9f341d3eae2e2cae5f4381245443c566c8d7ec6efa21b60cf51fcbeff8bc0c2e87d3cb386adef270d648b37bb7196b2aae256c11f1ac2713133e836199f125a578d2c74a6623ce9b667539ffecfe3b8e1d2a409d19c72a9f95af2acbf955cbd098b74554243a63764ae0ca9e386d4751a015f543853c4cf3de6457d47a5d2f10eadd881fe7ca846b1f33a1e68ba797465e9b7f2159be4d91a7e329c2a273519ed672b61f47614f3ff1ce3a8447bb83ecb44eecd2322b2943908eb69c56a90e6f14687136d4167bba307bca20695e7aa526462c1f9143553e0cac6c39dff7205e439b3942f8ada9019e9f723965d3666f0b8bfb82ff859d05e3b1486b22c4b11dc191b8

## hook到的数据跟抓包抓到的一样，说明 找对位置了

```

![image-20231018205122867](imgs/day16-课堂笔记.assets/image-20231018205122867.png)

## 3.2 sign签名破解

```python
# 1 String b2 = t3.a.i.a.a.a.b.e.b(sb2);

# 2 b(sb2)源码如下
public final String b(String params) {
    Charset charset = com.bilibili.commons.c.b;
    # 1  把传入的params字符串，得到bytes格式，params=aid=asdfsd&cid=121342&part=3dseffs
    byte[] bytes = params.getBytes(charset);
    # 2 d 是类中一个常量 9cafa6466a028bfb
    String str = d;
    # 3 com.bilibili.commons.c.b也是个常量
    Charset charset2 = com.bilibili.commons.c.b;
    if (str != null) {
        #4 把charset2转成字节数组，把上面的常量，得到bytes格式
        byte[] bytes2 = str.getBytes(charset2);
        #5 调用com.bilibili.commons.m.a.g完成加密
        # bytes：传入的待加密的字符串             明文
        # bytes2：9cafa6466a028bfb的bytes格式   秘钥
        String g = com.bilibili.commons.m.a.g(bytes, bytes2);
        Locale locale = Locale.US;
        if (g != null) {
            String lowerCase = g.toLowerCase(locale);
            #  6 转成小写返回
            return lowerCase;
        }
        throw new TypeCastException("null cannot be cast to non-null type java.lang.String");
    }
    throw new TypeCastException("null cannot be cast to non-null type java.lang.String");
}


# 3  继续分析com.bilibili.commons.m.a.g(bytes, bytes2)
	# 典型的SHA256加密:对传入的两个参数加密，一个是加密体，一个是盐，盐一般不变
# 4 看g的源代码
	# 两个参数，一个待加密的明文，一个是秘钥
    public static String g(byte[] bArr, byte[] bArr2) {
        try {
            MessageDigest messageDigest = MessageDigest.getInstance(AaidIdConstant.SIGNATURE_SHA256);
            messageDigest.reset();
            messageDigest.update(bArr);
            if (bArr2 != null) {
                messageDigest.update(bArr2);
            }
            # 得到加密的结果后，又执行了g.H，最终返回
            return g.H(messageDigest.digest());
        } catch (NoSuchAlgorithmException e) {
            throw new AssertionError(e);
        }
    }
# 5 g.H---》把自己数组转成16进制
 public static String H(byte[] bArr) {
        StringBuilder sb = new StringBuilder();
        for (byte b2 : bArr) {
            int i = b2 & 255;
            if (i < 16) {
                sb.append('0');
            }
            sb.append(Integer.toHexString(i));
        }
        return sb.toString();
    }


# 6 确认 sha256 加密，明文是什么，秘钥是什么？
	hook查看
```



![image-20231018205329567](imgs/day16-课堂笔记.assets/image-20231018205329567.png)

### 3.2.1 hook查看sha256的明文和盐

```python
import frida
import sys

rdev = frida.get_remote_device()
# Application(identifier="tv.danmaku.bili", name="哔哩哔哩", pid=20650, parameters={})
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function () {
    var a = Java.use("com.bilibili.commons.m.a");
    var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    a.g.implementation = function(bytes, bytes2){
        console.log("请求来了");
        console.log("bytes=",ByteString.of(bytes).utf8());
        console.log("bytes2=",ByteString.of(bytes2).utf8());

        var res = this.g(bytes, bytes2);
        console.log("sign=",res);

        return res;
    };

});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()

'''
# 明文：
bytes= aid=319287973&auto_play=0&build=6240300&cid=1289959578&did=IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow&epid=&from_spmid=main.ugc-video-detail.0.0&ftime=1692278308&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1697634744&sub_type=0&type=3
# 盐：
bytes2= 9cafa6466a028bfb
# 加密后的串，16进制
sign= 908c3d4bd0702d811a125bd7ed686bab9580266e65767f8adbb1ea34e6e570b0

'''



### 总结：sign逻辑
	1 一串字符串aid=319287973&auto_play=0&build=6240300&cid=1289959578&did=IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow&epid=&from_spmid=main.ugc-video-detail.0.0&ftime=1692278308&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1697634744&sub_type=0&type=3
    2 通过盐：9cafa6466a028bfb  + sha256 加密 得到加密串
    3 转成16进制
```

### 3.2.2 python重写sha256加密

```python
import hashlib

data = 'aid=319287973&auto_play=0&build=6240300&cid=1289959578&did=IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow&epid=&from_spmid=main.ugc-video-detail.0.0&ftime=1692278308&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1697634744&sub_type=0&type=3'
salt = '9cafa6466a028bfb'
obj = hashlib.sha256()

obj.update(data.encode('utf-8')) # 先对 明文 update，再加盐
obj.update(salt.encode('utf-8'))
print(obj.hexdigest())
# Python 得到的结果：908c3d4bd0702d811a125bd7ed686bab9580266e65767f8adbb1ea34e6e570b0
# hook得到的结果：   908c3d4bd0702d811a125bd7ed686bab9580266e65767f8adbb1ea34e6e570b0

```



## 3.3 请求体加密

```python
#1  t3.a.i.a.a.a.b.e.a(sb3)
	sb3是字符串，内容是： aid=319287973&auto_play=0&build=6240300&cid=1289959578&did=IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow&epid=&from_spmid=main.ugc-video-detail.0.0&ftime=1692278308&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1697634744&sub_type=0&type=3&sign=908c3d4bd0702d811a125bd7ed686bab9580266e65767f8adbb1ea34e6e570b0
    
    
# 2 t3.a.i.a.a.a.b.e.a源码
    public final byte[] a(String body) {
        try {
            # 1 b是常量：fd6b639dbcff0c2a1b03b389ec763c4b
            String str = b;
            # 2 utf-8 编码
            Charset charset = com.bilibili.commons.c.b;
            if (str != null) {
                # 3 常量使用utf-8得到 bytes格式
                byte[] bytes = str.getBytes(charset);
                # 4 aes加密的秘钥：fd6b639dbcff0c2a1b03b389ec763c4b
                SecretKeySpec secretKeySpec = new SecretKeySpec(bytes, "AES");
                # 5 常量：77b07a672d57d64c
                String str2 = f22911c;
                Charset charset2 = com.bilibili.commons.c.b;
                if (str2 != null) {
                    byte[] bytes2 = str2.getBytes(charset2);
                    # 6 aes加密的iv：77b07a672d57d64c
                    IvParameterSpec ivParameterSpec = new IvParameterSpec(bytes2);
                    Charset charset3 = com.bilibili.commons.c.b;
                    byte[] bytes3 = body.getBytes(charset3);
                    # 7 把body，通过aes加密，秘钥是：fd6b639dbcff0c2a1b03b389ec763c4b，iv是：77b07a672d57d64c，得到加密后的结果---》真正发送请求携带的数据
                    byte[] i = com.bilibili.droid.g0.a.i(secretKeySpec, ivParameterSpec, bytes3);
                    # 8 最后返回字节数组，放在请求体中：抓包看到的是乱码
                    return i;
                }
                throw new TypeCastException("null cannot be cast to non-null type java.lang.String");
            }
            throw new TypeCastException("null cannot be cast to non-null type java.lang.String");
        } catch (Exception e2) {
            BLog.e(a, e2);
            Charset charset4 = com.bilibili.commons.c.b;
            x.h(charset4, "Charsets.UTF_8");
            byte[] bytes4 = body.getBytes(charset4);
            x.h(bytes4, "(this as java.lang.String).getBytes(charset)");
            return bytes4;
        }
    }


# 3 aes的秘钥和iv，都是猜的，需要hook确认真正的确认--》hook  SecretKeySpec和IvParameterSpec的构造方法，得到秘钥和iv

```

### 3.3.1 hook--SecretKeySpec和IvParameterSpec的构造方法得到秘钥和iv

```python
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function () {
    var ByteString = Java.use("com.android.okhttp.okio.ByteString");

    var SecretKeySpec = Java.use("javax.crypto.spec.SecretKeySpec");
    SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function(key,name){
        console.log("请求来了");
        console.log("key=",ByteString.of(key).utf8()); //bytes格式转成字符串
        console.log("name=",name);

        var res = this.$init(key,name);
        return res;
    };

    var IvParameterSpec = Java.use("javax.crypto.spec.IvParameterSpec");
    IvParameterSpec.$init.overload('[B').implementation = function(iv){
        console.log("iv=",ByteString.of(iv).utf8()); // bytes格式转成字符串
        var res = this.$init(iv);
        return res;
    };

});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()


'''
最终：aes的秘钥是
key= fd6b639dbcff0c2a1b03b389ec763c4b
name= AES
aes的iv是
iv= 77b07a672d57d64c
'''
```

### 3.3.2 python实现aes加密

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY = "fd6b639dbcff0c2a1b03b389ec763c4b"
IV = "77b07a672d57d64c"

def aes_encrypt(data_string):
    aes = AES.new(
        key=KEY.encode('utf-8'),
        mode=AES.MODE_CBC,
        iv=IV.encode('utf-8')
    )
    raw = pad(data_string.encode('utf-8'), 16)
    return aes.encrypt(raw)


data = "aid=319287973&auto_play=0&build=6240300&cid=1289959578&did=IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow&epid=&from_spmid=main.ugc-video-detail.0.0&ftime=1692278308&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1697634744&sub_type=0&type=3&sign=908c3d4bd0702d811a125bd7ed686bab9580266e65767f8adbb1ea34e6e570b0"

# 字节类型
bytes_data = aes_encrypt(data)

result = [item for item in bytes_data]
print(result)
```



# 4 上述流程总结

```python
# 1 根据请求地址：x/report/click/android2  ---》反编译查找
# 2 retrofit发送请求---》用例
	ResponseBody responseBody = retrofit.create(接口类a.class).reportClick(参数).execute().body()
# 3 破解参数，create
# 4 参数是通过：d.this.H7 传了一堆参数进去，得到的结果

# 5 H7的逻辑是：
/*
1 把一堆 key  和 value 放到了 TreeMap中
2 构建sb对象，把treeMap的内容，拼成字符串了
     aid=asdfasdf&cid=asadfasd&part=sadfasd&
3 把字符串最后 & 删除
sb=aid=asdfasdf&cid=asadfasd&part=sadfasd
4 调用： t3.a.i.a.a.a.b.e.b对 aid=asdfasdf&cid=asadfasd&part=sadfasd进行加密，得到字符串
5 把加密后的字符串拼接到 aid=asdfasdf&cid=asadfasd&part=sadfasd 后面
sb=aid=asdfasdf&cid=asadfasd&part=sadfasd&sign=加密串
6 调用t3.a.i.a.a.a.b.e.a(sb3)对 上述字符串加密
7 得到的就是 请求体的内
*/

# 6 破解sign加密
	-sha256+盐 
    
# 7 得到最终的字符串，又加密了---》aes加密：秘钥，iv，明文

```

# 5 请求中 aid，cid，did破解

```python
# 1 待加密的字符串是

aid=319287973&   # 咱么不知道怎么来的
cid=1289959578&  # 不知道怎么来的
-------------------
did=IBksFHYQJ0QiF3FAckQmFVUFbBRxHS93Ow& # 不知道怎么来的

-------打开页面时间，视频播放时间-------
ftime=1692278308&
stime=1697634744&
---------------下面的都是固定的
auto_play=0& # 是否自动播放
build=6240300& # 版本
epid=&
from_spmid=main.ugc-video-detail.0.0&
lv=0&
mid=0&
mobi_app=android&
part=1&
sid=0&
spmid=main.ugc-video-detail.0.0&
sub_type=0&
type=3

# 2 目标：aid，cid
# 3 目标：did
```

## 5.1 aid和cid的破解

```python
# 1 找到aid和cid的位置
treeMap.put("aid", String.valueOf(j2));
treeMap.put("cid", String.valueOf(j4));

# 2 j2和j4怎么来的
 调用：H7(long j2, long j4)传入的

# 3 找到H7的用例
	d.this.H7(this.b.a(), this.b.b())
# 4 再往下不好找了---》aid和cid 是视频的id号，每个视频有自己的id号，我们要刷视频播放量，这个id号需要带的

# 5 网页版，刷b站播放量，打开一个视频地址，返回了 aid和cid
# 6 aid和cid在手机端不好破，而它跟某个视频是唯一的，后期咱们要刷视频播放量，要获得这个视频的aid和cid
	-可使用网页端地址获取---》使用移动端的接口刷播放量
```

### 5.1.1 web端获取aid和cid

```python
import requests
import json
import re

res = requests.get("https://www.bilibili.com/video/BV1uH4y1R7Ec")
data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', res.text)
data_dict = json.loads(data_list[0])

aid = data_dict['aid']
cid = data_dict['videoData']['cid']

print(aid)
print(cid)
```



## 5.2 did的破解 

```python
# 1 位置：treeMap.put("did", com.bilibili.lib.biliid.utils.f.a.c(f2));

# 2  com.bilibili.lib.biliid.utils.f.a.c(f2) 源码
public static String c(Context context) {
    # 1 判断变量是不是空：f13201c--》内存的变量中拿数据
    if (TextUtils.isEmpty(f13201c)) {
        # 2 如果是空，通过c2.f.b0.c.a.e.k().f获得值--》从xml中拿数据  SharedPreferences
        String f = c2.f.b0.c.a.e.k().f(context);
        f13201c = f;
        # 3 如果xml中拿出来还为空
        if (!TextUtils.isEmpty(f)) {
            return f13201c;
        }
        # 4 用算法生成
        # 赋值给这个变量，以后直接拿这个变量
        f13201c = g(context);
        # 5 放到xml中
        c2.f.b0.c.a.e.k().x(f13201c, context);
        return f13201c;
    }
    return f13201c;
}

# 3 算法如何生成的did：f13201c = g(context)
static String g(Context context) {
    # 使用f函数生成的did
    String f = f(context); 
    if (f.length() < 4) {
        f = Settings.Secure.getString(context.getContentResolver(), "android_id") + "@" + g.g(Build.MODEL);
    }
    # 最后调用了b(字符串)---》得到了did
    return b(f);
}

# 4 f()-->  字符串1|字符串2|字符串3|字符串4  
			mac地址|蓝牙地址|设备总线|sn号  # 都可以伪造出来
public static String f(Context context) {
    StringBuffer stringBuffer = new StringBuffer();
    String j2 = j(context);
    if (j2 != null) {
        String lowerCase = j2.replaceAll("[^0-9A-Fa-f]", "").toLowerCase();
        if (k(lowerCase)) {
            stringBuffer.append(lowerCase);
        }
    }
    stringBuffer.append('|');
    String a2 = z.a("persist.service.bdroid.bdaddr");
    if (a2.length() > 0) {
        String lowerCase2 = a2.replaceAll("[^0-9A-Fa-f]", "").toLowerCase();
        if (k(lowerCase2)) {
            stringBuffer.append(lowerCase2);
        }
    }
    stringBuffer.append('|');
    String h = h();
    if (h != null) {
        stringBuffer.append(h.toLowerCase());
    }
    stringBuffer.append('|');
    String i = i();
    if (i != null) {
        stringBuffer.append(i.toLowerCase());
    }
    return stringBuffer.toString();
}
#### 这个字符串，直接可以伪造
# 5 b() --》 ^:按位亦或    &：按位与：   GPT 转一下
public static String b(String str) {
    byte[] bytes = str.getBytes();
    bytes[0] = (byte) (bytes[0] ^ ((byte) (bytes.length & 255)));
    for (int i = 1; i < bytes.length; i++) {
        bytes[i] = (byte) ((bytes[i - 1] ^ bytes[i]) & 255);
    }
    try {
        return new String(Base64.encode(bytes, 11));
    } catch (Exception unused) {
        return str;
    }
}

# 6 上述代码python重写


```

### 5.2.1 python实现按位操作

```python
import random
import string
import base64

def base64_encrypt(data_string):
    data_bytes = bytearray(data_string.encode('utf-8'))
    data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
    for i in range(1, len(data_bytes)):
        data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
    res = base64.encodebytes(bytes(data_bytes))
    return res.strip().strip(b"==").decode('utf-8')
```

### 5.2.2 伪造mac地址|蓝牙地址|设备总线|sn号

```python
import random
import string


def create_random_mac(sep=":"):
    """ 随机生成mac地址 """
    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
	return mac

def gen_sn():
    return "".join(random.sample("123456789" + string.ascii_lowercase, 10))


mac_string = create_random_mac(sep="")
sn = gen_sn()

prev_did = "{}|||{}".format(mac_string, sn)
print(prev_did)
```

### 5.2.3 hook---f拿到did-->同一个设备不会变，不同设备会变

```python
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("tv.danmaku.bili")

scr = """
Java.perform(function () {
    var didCls = Java.use("com.bilibili.lib.biliid.utils.f.a");
    
    didCls.f.implementation = function(arg5){
        var res = this.f(arg5);
        console.log("生成的did = ",res);
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

# hook发现为：|||
# 或
```



# 6 代码整合

```python
import random
import string
import base64
import time
import re
import json
import requests
import hashlib

import urllib3

urllib3.disable_warnings()
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

####did获取开始#########、
# did生成
def base64_encrypt(data_string):
    data_bytes = bytearray(data_string.encode('utf-8'))
    data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
    for i in range(1, len(data_bytes)):
        data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
    res = base64.encodebytes(bytes(data_bytes))
    return res.strip().strip(b"==").decode('utf-8')

# 随机生成mac
def create_random_mac(sep=":"):
    """ 随机生成mac地址 """
    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
    return mac

# 随机生成sn
def gen_sn():
    return "".join(random.sample("123456789" + string.ascii_lowercase, 10))

mac_string = create_random_mac(sep="")

did = base64_encrypt(f"{mac_string}|||")
####did获取结束#########

### 获取aid和cid 开始 ###
res = requests.get("https://www.bilibili.com/video/BV1uH4y1R7Ec",verify=False)
text = re.findall(r"__INITIAL_STATE__=(.+);\(function", res.text)[0]
data_dict = json.loads(text)
# print(data_dict)
aid = data_dict['aid']
cid = data_dict['videoData']["cid"]
### 获取aid和cid 结束 ###


#### 构造明文参数
data_dict = {
    "aid": aid,
    "auto_play": "0",
    "build": "6240300",
    "cid": cid,
    "did": did,
    "epid": "",
    "from_spmid": "main.ugc-video-detail.0.0",
    "ftime": str(int(time.time() - random.randint(100, 5000))),
    "lv": "0",
    "mid": "0",
    "mobi_app": "android",
    "part": "1",
    "sid": "0",
    "spmid": "main.ugc-video-detail.0.0",
    "stime": str(int(time.time())),
    "sub_type": "0",
    "type": "3"
}

#####  2.sign签名---sha256加密-->sign
v1 = "&".join([f"{key}={data_dict[key]}" for key in sorted(data_dict)])
salt = "9cafa6466a028bfb"
obj = hashlib.sha256()
obj.update(v1.encode('utf-8'))
obj.update(salt.encode('utf-8'))

sign_string = obj.hexdigest()
print(sign_string)

data_string = f"{v1}&sign={sign_string}"

# #### 3.AES加密

KEY = "fd6b639dbcff0c2a1b03b389ec763c4b"
IV = "77b07a672d57d64c"

aes = AES.new(
    key=KEY.encode('utf-8'),
    mode=AES.MODE_CBC,
    iv=IV.encode('utf-8')
)
bytes_data = pad(data_string.encode('utf-8'), 16)

result = [item for item in bytes_data]
print(result)

```






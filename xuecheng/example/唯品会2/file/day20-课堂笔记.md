# 今日内容

# 1 今日目标

```python
# 1 唯品会搜索功能实现
    1 https://mp.appvipshop.com/apns/device_reg  # 搞定了
        -devices_token:uuid
        -skey:固定的
        -authorization：sha1加密，有盐，加了两次密

    2 https://vcsp-api.vip.com/token/getTokenByFP
    3 https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token
    4 https://mapi.appvipshop.com/vips-mobile/rest/shopping/search/product/list/v1
```



# 2 getTokenByFP接口

```python
# 请求地址：
https://vcsp-api.vip.com/token/getTokenByFP
# 请求方式：
get
# 请求参数：
vcspKey=4d9e524ad536c03ff203787cf0dfcd29
# 请求头：
vcspauthorization	vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387

# 需要破解的：
	-vcspKey
    -vcspauthorization实际上是vcspSign
```

## 2.1 vcspKey破解

### 2.1.1 直接确定

```python
# 固定值：咱们上节课在破解 skey的时候，写了个hook脚本---》脚本中打印出过：vcspKey---》hook了好几次，发现vcspKey换了设备也是固定的

# 以后都是固定的：4d9e524ad536c03ff203787cf0dfcd29
```



```python
设备1：
		-----------------
		参数==> app_name
		返回的值==> shop_android
		-----------------
		参数==> vcsp_key
		返回的值==> 4d9e524ad536c03ff203787cf0dfcd29
		-----------------
		参数==> api_key
		返回的值==> 23e7f28019e8407b98b84cd05b5aef2c

		-----------------
		参数==> skey
		返回的值==> 6692c461c3810ab150c9a980d0c275ec
		-----------------
		参数==> skey
		返回的值==> 6692c461c3810ab150c9a980d0c275ec

设备2：
        -----------------
        参数==> app_name
        返回的值==> shop_android
        -----------------
        参数==> vcsp_key
        返回的值==> 4d9e524ad536c03ff203787cf0dfcd29
        -----------------
        参数==> api_key
        返回的值==> 23e7f28019e8407b98b84cd05b5aef2c
        -----------------
        参数==> skey
        返回的值==> 6692c461c3810ab150c9a980d0c275ec
        -----------------
        参数==> skey
        返回的值==> 6692c461c3810ab150c9a980d0c275ec
```



### 2.1.2 搜索

```python
# 1 搜 vcspKey 
# 2 结果又两个，但是是一样的
# 3 vCSPNetworkParam.pairs.put("vcspKey", VCSPCommonsConfig.getAppKey());
# 4 VCSPCommonsConfig.getAppKey()
  public static String getAppKey() {
        return appKey;
    }
# 5 找appKey在哪赋值---》往下拉
  public static void setAppKey(String str) {
        appKey = str;
    }
# 6 谁调用了setAppKey---》查找用例--就一个
VCSPCommonsConfig.setAppKey(KeyInfoFetcher.getInfo(VCSPCommonsConfig.getContext(), "vcsp_key"));

# 7 KeyInfoFetcher.getInfo---》java的反射
    public static String getInfo(Context context, String str) {
        try {
            if (clazz == null || object == null || method == null) {
                int i10 = KeyInfo.f69594a;
                clazz = KeyInfo.class;
                object = KeyInfo.class.newInstance();
                method = clazz.getMethod("getInfo", Context.class, String.class);
            }
            return (String) method.invoke(object, context, str);
        } catch (Exception e10) {
            VCSPMyLog.error(KeyInfoFetcher.class, e10);
            return "";
        }
    }

# 8 KeyInfo类的getInfo方法
	 public static String getInfo(Context context, String str) {
        try {
            try {
                return getNavInfo(context, str);
            } catch (Throwable th2) {
                return "KI gi: " + th2.getMessage();
            }
        } catch (Throwable unused) {
            SoLoader.load(context, LibName);
            return getNavInfo(context, str);
        }
    }
# 9 getNavInfo(context, str) --》jni的方法---》上次课，咱们读了它了，并且hook了--》发现返回值是固定的
# 10 值是固定的
4d9e524ad536c03ff203787cf0dfcd29
```

![image-20231103201239430](imgs/day20-课堂笔记.assets/image-20231103201239430.png)

## 2.2 vcspSign破解

### 2.2.1 固定值

```python
# 多次抓包---》发现参数值这个值是固定的
# 固定值：05a68135d2bfd322e3a22f95bbc25a24c777f387
```

### 2.2.2 搜索

```python
# 1 搜索：vcspSign|
# 2 找到一个
# 3 str = VCSPSecurityBasicService.apiSignVcspToken()
# 4 VCSPSecurityBasicService.apiSignVcspToken()
 public static String apiSignVcspToken(TreeMap<String, String> treeMap, String str) throws Exception {
        return VCSPSecurityConfig.getMapParamsSign(VCSPCommonsConfig.getContext(), treeMap, str, true);
    }
# 5 VCSPSecurityConfig.getMapParamsSign()

    public static String getMapParamsSign(Context context, TreeMap<String, String> treeMap, String str, boolean z10) {
        String str2 = null;
        if (treeMap != null) {
            boolean z11 = false;
            Set<Map.Entry<String, String>> entrySet = treeMap.entrySet();
            if (entrySet != null) {
                Iterator<Map.Entry<String, String>> it = entrySet.iterator();
                while (true) {
                    if (it == null || !it.hasNext()) {
                        break;
                    }
                    Map.Entry<String, String> next = it.next();
                    if (next != null && next.getKey() != null && ApiConfig.USER_TOKEN.equals(next.getKey()) && !TextUtils.isEmpty(next.getValue())) {
                        z11 = true;
                        break;
                    }
                }
            }
            if (z11) {
                if (TextUtils.isEmpty(str)) {
                    str = VCSPCommonsConfig.getTokenSecret();
                }
                str2 = str;
            }
            return getSignHash(context, treeMap, str2, z10);
        }
# 6 getSignHash(context, treeMap, str2, z10);
   public static String getSignHash(Context context, Map<String, String> map, String str, boolean z10) {
        try {
            return gs(context.getApplicationContext(), map, str, z10);
        } catch (Throwable th2) {
            VCSPMyLog.error(clazz, th2);
            return "error! params invalid";
        }
    }
# 7 gs(context.getApplicationContext(), map, str, z10);反射
            private static String gs(Context context, Map<String, String> map, String str, boolean z10) {
        try {
            if (clazz == null || object == null) {
                synchronized (lock) {
                    initInstance();
                }
            }
            if (gsMethod == null) {
                gsMethod = clazz.getMethod("gs", Context.class, Map.class, String.class, Boolean.TYPE);
            }
            return (String) gsMethod.invoke(object, context, map, str, Boolean.valueOf(z10));
        } catch (Exception e10) {
            e10.printStackTrace();
            return "Exception gs: " + e10.getMessage();
        } catch (Throwable th2) {
            th2.printStackTrace();
            return "Throwable gs: " + th2.getMessage();
        }
    }
# 8 KeyInfo中找gs
  public static String gs(Context context, Map<String, String> map, String str, boolean z10) {
        try {
            try {
                return gsNav(context, map, str, z10);
            } catch (Throwable th2) {
                return "KI gs: " + th2.getMessage();
            }
        } catch (Throwable unused) {
            SoLoader.load(context, LibName);
            return gsNav(context, map, str, z10);
        }
    }
# 9 gsNav 是jni的方法---》加密方式--》so中做的--》上次课读过---》sha1加密，有盐，加了两次密--》盐一样--》待加密的参数---》authorization动态变化---》得到这个vcspSign的明文是固定的，所以密文也是固定的
```

![image-20231103201855680](imgs/day20-课堂笔记.assets/image-20231103201855680.png)

#### 2.2.2.1 hook脚本

```js
function do_hook() {

        var addr = Module.findExportByName("libkeyinfo.so", "getByteHash");
        console.log(addr); //0xb696387d


        Interceptor.attach(addr, {
            onEnter: function (args) {
                this.x1 = args[2];
            },
            onLeave: function (retval) {
                console.log("--------------------")
                console.log(Memory.readCString(this.x1));
                console.log(Memory.readCString(retval));
            }

        })

}

function load_so_and_hook() {
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            // console.log("[dlopen:]", path);
            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf("libkeyinfo.so") !== -1) {
                console.log("[dlopen:]", this.path);
                do_hook();

            }
        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();

            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf("libkeyinfo.so") !== -1) {
                console.log("\nandroid_dlopen_ext加载：", this.path);
                do_hook();

            }
        }
    });
}

load_so_and_hook();

// frida -U -f com.achievo.vipshop -l delay_hook.js

// 根据抓包抓到的数据，去搜索

/* 请求参数整体加密---》请求参数是固定的---》所以结果是固定的

da19a1b93059ff3609fc1ed2e04b0141 vcspKey=4d9e524ad536c03ff203787cf0dfcd29
5a7c831821536f5a9d5244b99af681226dc8a277
--------------------
da19a1b93059ff3609fc1ed2e04b0141 5a7c831821536f5a9d5244b99af681226dc8a277
05a68135d2bfd322e3a22f95bbc25a24c777f387
*/
```

#### 2.2.2.2 python代码得到 vcspSign

```python
import hashlib

data_string ="da19a1b93059ff3609fc1ed2e04b0141vcspKey=4d9e524ad536c03ff203787cf0dfcd29"

# sha1加密
hash_object = hashlib.sha1()
hash_object.update(data_string.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7) # 5a7c831821536f5a9d5244b99af681226dc8a277

x = "da19a1b93059ff3609fc1ed2e04b0141"+arg7
# sha1加密
hash_object = hashlib.sha1()
hash_object.update(x.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7) #05a68135d2bfd322e3a22f95bbc25a24c777f387
```



## 2.3 getTokenByFP接口-python实现

```python
import requests

res = requests.get(
    url="https://vcsp-api.vip.com/token/getTokenByFP?vcspKey=4d9e524ad536c03ff203787cf0dfcd29",
    headers={
        "vcspauthorization": "vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387"
    }
)

print(res.text)
```



# 3 generate_token接口

## 3.1 抓包分析

```python
# 请求地址：
https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token
# 请求方式：
post

# 请求头：（上次课破过了-原理是把请求体的内容做了两次sha1加密+盐）
authorization	OAuth api_sign=04a3e9bfa601113ccf8d8b62bbd6f76fa36f6a15
# 请求体：
api_key	23e7f28019e8407b98b84cd05b5aef2c  # 固定值
did	 # 空的
edata # 很多东西
eversion	0 # 固定的
skey	6692c461c3810ab150c9a980d0c275ec # 之前破过  skey:固定的
timestamp	1699013439 # 时间戳


# 破解目标
	edata  # 像 base64编码，先base64解码---=》看看能不能解成明文---》如果能解成明文--》不需要破解了
    	   # 咱们这个解码后还是密文---》需要破
```

## 3.2 搜索分析+hook

```python
# 1 反编译，搜索  "edata"
# 2 一个常量：public static final String EDATA = "edata";
# 3 查找用例---》找到比较多--》殊途同归--》看第二个
treeMap2.put(ApiConfig.EDATA, GobalConfig.encodeStr(context, sb2.toString(), null, null, 0));
# 4 GobalConfig.encodeStr
public static String encodeStr(Context context, String str, String str2, String str3, int i10) {
        try {
            d.f(GobalConfig.class, "SecurityConfig encodeStr");
            return VCSPSecurityConfig.encodeStr(getApplicationContext(context), str, i10);
        } catch (Throwable th2) {
            d.d(GobalConfig.class, th2);
            return null;
        }
    }

# 5 VCSPSecurityConfig.encodeStr(getApplicationContext(context), str, i10);
   public static String encodeStr(Context context, String str, int i10) {
        try {
            VCSPMyLog.info(VCSPSecurityConfig.class, "VCSPSecurityConfig encodeStr");
            return es(context.getApplicationContext(), str, null, null, i10);
        } catch (Throwable th2) {
            VCSPMyLog.error(VCSPSecurityConfig.class, th2);
            return null;
        }
    }
# 6 es(context.getApplicationContext(), str, null, null, i10);
private static String es(Context context, String str, String str2, String str3, int i10) {
        try {
            if (clazz == null || object == null) {
                synchronized (lock) {
                    initInstance(); # KeyInfo类
                }
            }
            if (esMethod == null) {
                esMethod = clazz.getMethod("es", Context.class, String.class, String.class, String.class, Integer.TYPE);
            }
            return (String) esMethod.invoke(object, context, str, str2, str3, Integer.valueOf(i10));
        } catch (Exception e10) {
            e10.printStackTrace();
            return "Exception es: " + e10.getMessage();
        } catch (Throwable th2) {
            th2.printStackTrace();
            return "Throwable es: " + th2.getMessage();
        }
    }
# 7 KeyInfo类的es方法
    public static String es(Context context, String str, String str2, String str3, int i10) {
        try {
            try {
                return esNav(context, str, str2, str3, i10);
            } catch (Throwable th2) {
                return "KI es: " + th2.getMessage();
            }
        } catch (Throwable unused) {
            SoLoader.load(context, LibName);
            return esNav(context, str, str2, str3, i10);
        }
    }
# 8 return esNav(context, str, str2, str3, i10)  jni的方法

# 9 hook-esNav看参数和返回值
# 10 反编译so--》找代码看
```

![image-20231103203330544](imgs/day20-课堂笔记.assets/image-20231103203330544.png)

![image-20231103203607674](imgs/day20-课堂笔记.assets/image-20231103203607674.png)

### 3.2.1 hook-esNav看参数和返回值

```python

# 清除数据，重新运行
import frida
import sys

rdev = frida.get_remote_device()

session = rdev.attach("唯品会")

scr = """
Java.perform(function () {
    var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");
    
    KeyInfo.esNav.implementation = function (ctx, str, str2,str3, i10) {
        console.log("-----------------gsNav-----------------");
        console.log("参数==>", str);
        console.log("参数==>", str2);
        console.log("参数==>", str3);
        console.log("参数==>", i10);
        var res = this.esNav(ctx, str, str2,str3, i10);
        console.log("返回的值==>", res);
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

''' 跟抓包抓的一样，位置对了
参数==> app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pixel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2C%22as3%22%3A%22%22%2C%22as4%22%3A%22cff15d2b8c13bf22%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%22a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d%22%7D&mars_cid=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&phone_model=Pixel+2+XL&session_id=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d_shop_android_1699015508448&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzAxNjA3MjY3fHx8.1bdf9570959162ddac51899f6adee761
参数==> null
参数==> null
参数==> 0
返回的值==> NmY3MzE5ZTkzMjRlYzJlMM62kxsv0hIQOKLZ1FsI1tRY8KW1D6WWgXK44PUa/hqFUAdBFvEffpWkwg1yHf4tp56pYh1zMr/ix0Ba4qyBjU988lwq4zSTIQB06dwAg39xyrX4SxEeC7n3MP8b8/7xkb5+w+adMudewYIOiRYYFrWk9UvbTx5GgPlIt4Wus5HCRy31xq0Qlogr+KjQiCeIjBR6X4gtxjOcQ/Itt5kl0cZJLVWik2CqfbaHg73tj63jLzEPaX823A2zUtCEpNbhKj8kAD4exQKmpKSXed1OBoxla3nB7EixhFwLMv9rRvdFhTUVuFDCJ1KHcj4AZ+ZgAuC3cbIjX0y4zrhz2xSZebR7AYjuGwB5g5Bp/g0VVKU+GRIizCZPKfGqjTDRSzSOVQmEO+SP6uHIVt1WsNdpHYgfFrKYuzABA1f09WrAs1gVoudNcVT3F3ntK4VjqOSScmL3Mc3ryjKtcOc+BP4exDrl5YJ2DaTgm4Rlqm2TaH5LjwtGO6n138qSRqXtsRy2QWaQr8RF488ywEQryxGJrYKL2ajew7CaGEwk2WOV1UU9w0Y3GbjwQN2GL7qCwiSFlBhZ2AGvnP5wGkUbl6gp3cIsKyMAXx4/Jxh4QvaV3OLRsfK1Ek5jUETYmKfOeiq4EfPyAsUIMY6sy2v65TgYd7d98uQ5GJd3cfxN9nuesy66MmG7M44xz3diFa6OjAXpLnWcVwGWdFKblxQJd9p2Jpuir2us46DywxkV1hXJaGGg3CLMzAHlTYePPFaXEGHiDKLap1ynRvyitBSt1dvvXh//iHT/U2VyahYiF2nz9JztQwhuk9yNGtmfu+R9Dloaxh3WMbX4/0vqB6zOYDQeHRqS4C4q6AF5QQnRxjFS9mg3izuHEC7CJaUhJ27ZrohotbPiqlyTIyoixw0wNbCxuqGzhvMMhkbZnpussnk0aFoXw6U62OWZ3oFwQu1Wa3gMFvd+NpLXq+uXkjWiTb7sGW1PxYsktVKMSBhRTxyUKN30X0V1subGR1SetlqDtxszzUArTDLSGS1Q8kRZPioNDGz3pnVHdH6e1Lomkf7o/vcL1icXcN5QWPjFZuKbrgobbCxHcYyQEGwVgTkn6SN2jaNWdLNQuozdN2ZQFtqmMC0uDdF1tGZEqe9sUT9iAUUKA680XgtN6+XXZDxwgecWqCL+15gaUDO7u3kNUhSOkqtCfDlKcW/DP/uz72ID1jGSTQ==

# 猜测的：
# 传入了参数 app_name=很多很多
# 使用so做了加密--》转成base64，返回了

'''



## 分析的结果是：传入了很多，调用so，实现了加密，转成base64返回了

```

## 3.3 读so文件-分析逻辑

```python
# 1 ida 打开--libkeyinfo.so
# 2 搜索esNav发现是静态注册： java_包名_类名_方法名
# 3 代码入下
int __fastcall Java_com_vip_vcsp_KeyInfo_esNav(JNIEnv_ *a1, int a2, int a3, int a4, int a5, int a6, int a7)
{
  int v9; // r5
  int v11; // [sp+4h] [bp-Ch]

  v11 = a4;
  if ( j_Utils_ima(a1, a2, a3) )
    v9 = j_Functions_es(a1, a4, a5, a6, a7, v11);
  else
    v9 = 0;
  j_Utils_checkJniException(a1);
  return v9;
}

# 4 查看：v9 = j_Functions_es(a1, a4, a5, a6, a7, v11);
int __fastcall j_Functions_es(int a1, int a2, int a3, int a4, int a5, int a6)
{
  return Functions_es(a1, a2, a3, a4, a5);
}

# 5 Functions_es(a1, a2, a3, a4, a5);
##### 代码部分1#######
v22 = a1->functions->FindClass(a1, "javax/crypto/Cipher");
v23 = a1->functions->GetStaticMethodID(a1, v22, "getInstance", "(Ljava/lang/String;)Ljavax/crypto/Cipher;");
v24 = a1->functions->NewStringUTF(a1, "AES/CBC/PKCS5Padding");
v57 = a1->functions->CallStaticObjectMethod((JNIEnv *)a1, v22, v23, v24);

##### 代码部分2####
v25 = a1->functions->NewStringUTF(a1, "AES");
v26 = a1->functions->FindClass(a1, "javax/crypto/spec/SecretKeySpec");
v27 = a1->functions->GetMethodID(a1, v26, "<init>", "([BLjava/lang/String;)V");
v21 = a1->functions->NewObject((JNIEnv *)a1, v26, v27, v20, v25);
a1->functions->DeleteLocalRef((JNIEnv *)a1, v20);
    
    
#### 代码部分3 #####
v34 = a1->functions->FindClass(a1, "javax/crypto/spec/IvParameterSpec");
v35 = a1->functions->GetMethodID(a1, v34, "<init>", "([B)V");
        
a1->functions->CallVoidMethod((JNIEnv *)a1, v29, v42, 1, v21, v39);
v52 = (char *)j_base64_encode((char *)v39); # 把v39进行base64编码
v45 = a1->functions->NewStringUTF(a1, v52); # v52是c的字符串--》转成字符串返回
return v45; # 加密后的结果


# 6 通过读代码---》猜测：aes加密
	-aes的key 是什么
    -aes的iv 偏移量
    -加密的明文是什么
    
    
# 7 补充java的 aes加密的代码
public static String encryptData(String key, String iv, String content) throws Exception {	     # 待加密的字符串
        byte[] byteContent = content.getBytes(StandardCharsets.UTF_8);
    	# aes的秘钥
        SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(), "AES");
    	# aes的iv
        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv.getBytes());
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(1, secretKeySpec, ivParameterSpec);
    	# 通过key和iv对待加密字符串进行加密
        byte[] encryptedBytes = cipher.doFinal(byteContent);
        return Base64.encodeBase64String(encryptedBytes);
    }


# 8 对比 c代码  和 java代码
	#### c代码#######   jni中使用c调用java
    v22 = a1->functions->FindClass(a1, "javax/crypto/Cipher");
    v23 = a1->functions->GetStaticMethodID(a1, v22, "getInstance", "(Ljava/lang/String;)Ljavax/crypto/Cipher;");
    v24 = a1->functions->NewStringUTF(a1, "AES/CBC/PKCS5Padding");
    v57 = a1->functions->CallStaticObjectMethod((JNIEnv *)a1, v22, v23, v24);
    ###翻译成java代码###### 
    Cipher cipher=Cipher.getInstance("AES/CBC/PKCS5Padding")
    
    
    
    #### c代码#######  c调用java代码--》核心就是得到aeskey的对象
    v25 = a1->functions->NewStringUTF(a1, "AES");
    v26 = a1->functions->FindClass(a1, "javax/crypto/spec/SecretKeySpec");
    v27 = a1->functions->GetMethodID(a1, v26, "<init>", "([BLjava/lang/String;)V");
    v21 = a1->functions->NewObject((JNIEnv *)a1, v26, v27, v20, v25);
    ###翻译成java代码###### 
    SecretKeySpec spec =new SecretKeySpec(第一个参数：v20,第二个参数：v25 "AES")
    SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(), "AES");
    ### v20是 key
    
    
    
    #### c代码#######  c调用java代码--》核心就是得到aeskey的对象
	  v34 = a1->functions->FindClass(a1, "javax/crypto/spec/IvParameterSpec");
      v35 = a1->functions->GetMethodID(a1, v34, "<init>", "([B)V");
      v37 = a1->functions->NewObject((JNIEnv *)a1, v36, v35, v32);
    ###翻译成java代码######
    IvParameterSpec ivParameterSpec = new IvParameterSpec(iv.getBytes());
    ## v32 是 iv
   

    #### c代码#######  c调用java代码--》核心就是得到aeskey的对象
	v43 = a1->functions->GetMethodID(a1, v22, "doFinal", "([B)[B");
    v44 = a1->functions->CallObjectMethod((JNIEnv *)a1, v29, v43, v41);
    ###翻译成java代码######
    byte[] encryptedBytes = cipher.doFinal(byteContent);
    ## v41 是明文
    # v44 加密后的
    
# 9 c代码虽然很多，但实际是在
Cipher cipher=Cipher.getInstance("AES/CBC/PKCS5Padding")
SecretKeySpec spec =new SecretKeySpec(第一个参数：v20,第二个参数：v25 "AES")
IvParameterSpec ivParameterSpec = new IvParameterSpec(iv.getBytes());
cipher.init(1, spec, ivParameterSpec);
byte[] encryptedBytes = cipher.doFinal(byteContent); #传入明文字节数组，返回密文字节数组
## v20是 aes的 key
## v32 是 aes的iv
## v41 是 aes明文
# v44 是 aes加密后的结果
```

 ![image-20231103204510271](imgs/day20-课堂笔记.assets/image-20231103204510271.png)



##  3.4 加密方式使用aes加密--》破解aes的key值

```python
# 1 上面分析是v20，分析
v20 = a1->functions->NewByteArray(a1, 16); # 生成一个空的 16位的数组
a1->functions->SetByteArrayRegion((JNIEnv *)a1, v20, 0, 16, v19); # 把v19的前16位，放到上面定义的那个空数组中

#2 继续看v19
v18 = strlen(s); # s是个字符串，v18是数字，是字符串的长度
v19 = (const jbyte *)j_getMD516(v59, s, v18); # 得到md5值

# 3 做如下操作--》同时hook c和java--》如果打印出来的值是一样的，key值就定位好了
	-1 在c层 hook一下j_getMD516---》getMD516(a1, a2, a3);
	-2 在java层 hook：SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(), "AES");的构造方法
    
# 4 同时hook-java层的SecretKeySpec实例化方法 和 c层的getMD516 方法
	- hook这俩，可能项目中好多地方都在用，打印出来非常多，不好定位
    -java中的esNav 方法---》调用了 so文件中 某个加密---》某个加密中 执行了getMD516 得到了aes的key---》c语言调用java的SecretKeySpec的初始化方法
    -我们可以这么做：hook3个东西
    	-1 hook esNav 
        	它开始的时候，一开始打印一句话  ===>开始了
            结束的时候，打印   ====》结束了
        -2 hook getMD516
        -3 hook SecretKeySpec
        
   -效果如下：
	===>开始了
    	getMD516  我们打印了一些东西
        SecretKeySpec 打印了一些东西
    ===>结束了
    
    
# 5 总体要hook 3个位置
	java中的esNav
    c中的getMD516
    java中的SecretKeySpec

  
    
```



![image-20231103213902742](imgs/day20-课堂笔记.assets/image-20231103213902742.png)



### 3.4.1 hook-3个-esNav-getMD516-SecretKeySpec

```js
function java_hook() {
    Java.perform(function () {
        var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");

        KeyInfo.esNav.implementation = function (ctx, str, str2, str3, i10) {
            console.log("-----------------gsNav-----------------");
            console.log("开始================>", str);
            var res = this.esNav(ctx, str, str2, str3, i10); // 一定会执行 getMD516 和 java的 SecretKeySpec
            console.log("结束================>", res);
            return res;
        }

        var SecretKeySpec = Java.use("javax.crypto.spec.SecretKeySpec");
        var ByteString = Java.use("com.android.okhttp.okio.ByteString");
        SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function (key, name) {
            if (name === 'AES') {
                console.log("-----------------------SecretKeySpec---------------------------");
                //console.log("4.key bytes=", JSON.stringify(key));
                console.log("java key hex =", ByteString.of(key).hex());
                //console.log("4.key", ByteString.of(key).utf8());
            }
            var res = this.$init(key, name);
            return res;
        }
    });

}

function delay_hook(so_name, hook_func) {
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            // console.log("[dlopen:]", path);
            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf(so_name) !== -1) {
                console.log("[dlopen:]", this.path);
                hook_func();
            }
        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            this.path = path;
        },
        onLeave: function (retval) {
            if (this.path.indexOf(so_name) !== -1) {
                console.log("\nandroid_dlopen_ext加载：", this.path);
                hook_func();
            }
        }
    });
}

function so_hook() {
    var getMD516 = Module.findExportByName("libkeyinfo.so", "getMD516");
    console.log('getMD516 addr = ', getMD516);

    if (getMD516) {
        Interceptor.attach(getMD516, {
            onEnter: function (args) {
                console.log('getMD5参数：', hexdump(args[1], {length: args[2].toInt32()}), "\n");
                // console.log('2.getMD5 参数：', hexdump(args[1]), "\n");
            },
            onLeave: function (retval) {
                // console.log('3.getMD5 返回值：', hexdump(retval), "\n");
                console.log('getMD5=key 返回值：', hexdump(retval, {length: 16}), "\n");
            }
        });
    }
}

delay_hook("libkeyinfo.so", so_hook)
java_hook()

//frida -U -f  com.achievo.vipshop -l  4-hook-3个-esNav-getMD516-SecretKeySpec.js


/*

开始================> 
app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221
440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pixel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C
%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2C%22as3%22%3A%22%22%2C%22as4%22%3A%22cff15d2b8c13bf22%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%22a9d1a2b9-2a79-
36fd-a8ca-cbe24c03979d%22%7D&mars_cid=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&phone_model=Pixel+2+XL&session_id=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d_shop_android_1699019437862&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzAxNjExMTk3fHx8.9eaabfe23735d1e02d9b99f7f289e697
getMD5参数：            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
b9ccffc0  61 65 65 34 63 34 32 35 64 62 62 32 32 38 38 62  aee4c425dbb2288b
b9ccffd0  38 30 63 37 31 33 34 37 63 63 33 37 64 30 34 62  80c71347cc37d04b

getMD5=key 返回值：            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF      
b9ccff48  cd d1 7a b2 9b 84 b3 25 52 dd cf bb 4a bf 02 25  ..z....%R...J..%

-----------------------SecretKeySpec---------------------------
java key hex = cdd17ab29b84b32552ddcfbb4abf0225
结束================>

getMD5 的返回值是：aes的key值:     cd d1 7a b2 9b 84 b3 25 52 dd cf bb 4a bf 02 25
SecretKeySpec 入参是 aes的key值   cdd17ab29b84b32552ddcfbb4abf0225

 */


//  多hook几次发现，hook到的aes的key值都是一样的---》确定好了

aes的可以就是：cdd17ab29b84b32552ddcfbb4abf0225
```



## 3.5 破解aes的iv值

```python
# 1 上面分析了 aes的iv是 ----》 v32 是 aes的iv
v31 = j_Utils_getStringByteArray(a1);
v32 = (struct _jobject *)v31;

v34 = a1->functions->FindClass(a1, "javax/crypto/spec/IvParameterSpec");
v35 = a1->functions->GetMethodID(a1, v34, "<init>", "([B)V");
v37 = a1->functions->NewObject((JNIEnv *)a1, v36, v35, v32);
# v32 就是aes的iv的值，v32又是v31赋值的，v31通过执行j_Utils_getStringByteArray，传了a1得到的
# a1 是通过NewStringUTF(a1, v58)  v58得到的
v58[0] = 0LL;
v58[1] = 0LL;
v58[2] = 0LL;
v58[3] = 0LL;

# 2 v58 是一个长度为4的数组，数字目前全是空
	j_rand16Str(v58); 对这个空数组赋值
# 3 随机生成字符，填充进去


# 4 hook---》j_rand16Str--->看iv是什么

# 5 正常来讲，aes的key是固定的，iv也是固定的
	-移动端通过key和iv加密----》后端通过key和iv解密
    -咱们这个案例特殊:
       	key是固定的
        iv随机生成的
    -前端通过固定的key+随机生成的iv加密-----》后端通过固定给的key和前端携带后端的iv解密
    
    
# 6 hook---》esNav--》IvParameterSpec构造方法---》rand16Str--》按照上面逻辑，打印开始，打印结束
```

### 3.5.1 hook-esNav-IvParameterSpec构造方法-rand16Str

```python
// hook  KeyInfo的esNav---》内部执行了rand16Str---》又执行了java的IvParameterSpec
function java_hook() {
    Java.perform(function () {
        var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");
        KeyInfo.esNav.implementation = function (ctx, str, str2, str3, i10) {
            console.log("开始================>", str);
            var res = this.esNav(ctx, str, str2, str3, i10);  // 一定会执行 rand16Str  和 IvParameterSpec 的构造方法
            console.log("结束================>", res);
            return res;
        }

        var IvParameterSpec = Java.use("javax.crypto.spec.IvParameterSpec");
        var ByteString = Java.use("com.android.okhttp.okio.ByteString");
        IvParameterSpec.$init.overload('[B').implementation = function (iv) {
            console.log("-----------------------IvParameterSpec---------------------------");
            //console.log("iv str=", ByteString.of(iv).utf8());
            console.log("java iv hex=", ByteString.of(iv).hex());
            //console.log("iv byte", JSON.stringify(iv));
            var res = this.$init(iv);
            return res;
        }

    });

}

function delay_hook(so_name, hook_func) {
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf(so_name) !== -1) {
                console.log("[dlopen:]", this.path);
                hook_func();
            }
        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            this.path = path;
        },
        onLeave: function (retval) {
            if (this.path.indexOf(so_name) !== -1) {
                console.log("\nandroid_dlopen_ext加载：", this.path);
                hook_func();
            }
        }
    });
}

function so_hook() {
    var rand16Str = Module.findExportByName("libkeyinfo.so", "rand16Str");
    console.log('rand16Str addr = ', rand16Str);
    if (rand16Str) {
        Interceptor.attach(rand16Str, {
            onEnter: function (args) {
                this.x1 = args[0]
            },
            onLeave: function (retval) {
                // console.log('5.rand16Str 返回值：', hexdump(this.x1), "\n");
                console.log('so rand16Str=iv 返回值：', hexdump(this.x1, {length: 16}), "\n");
            }
        });
    }
}

delay_hook("libkeyinfo.so", so_hook)
java_hook()

//frida -U -f  com.achievo.vipshop -l  5-hook-esNav-IvParameterSpec构造方法-rand16Str.js


/*
开始================> app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221
440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pixel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C
%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2C%22as3%22%3A%22%22%2C%22as4%22%3A%22cff15d2b8c13bf22%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%22a9d1a2b9-2a79-
36fd-a8ca-cbe24c03979d%22%7D&mars_cid=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&phone_model=Pixel+2+XL&session_id=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d_shop_android_1699020913111&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzAxNjEyNjcyfHx8.5474000460661f0cbc4c44ccaaa8c23c


so rand16Str=iv 返回值：            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
b238af28  63 64 64 31 37 37 34 37 39 30 61 63 32 30 34 65  cdd1774790ac204e

-----------------------IvParameterSpec---------------------------
java iv hex= 63646431373734373930616332303465
结束================>

# 这个iv是：63646431373734373930616332303465
# 再一次： 39363232343039383639666466393966
# 每次iv都不一样---》iv是动态生成的--->由于后端要解密---》一定会携带到后端--》一定是拼在某个位置携带到后端，aes的key由于是固定的，不需要携带
# 把上面 待加密字符串  通过  aes的key和随机生成的iv---》加密---》把iv拼接在前面--》使用base64加密了

iv:是随机生成的
 */
```



## 3.6 待加密的字符串是

```python
# 1 待加密字符串
app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221
440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pixel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C
%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2C%22as3%22%3A%22%22%2C%22as4%22%3A%22cff15d2b8c13bf22%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%22a9d1a2b9-2a79-
36fd-a8ca-cbe24c03979d%22%7D&mars_cid=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&phone_model=Pixel+2+XL&session_id=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d_shop_android_1699020913111&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzAxNjEyNjcyfHx8.5474000460661f0cbc4c44ccaaa8c23c
# 2 做了url编码
# 3 转回来
    from urllib.parse import unquote_plus
    s=''
    res=unquote_plus(s)
    print(res)
    
# 4 通过 aes的key:cdd17ab29b84b32552ddcfbb4abf0225  和 iv随机生成的  得到加密串----》把iv拼接在前面---》通过base64编码得到  edata

# 5 看待加密的串中，有没有需要破解的数据
app_name=shop_android&   # 固定的
app_version=7.83.3&      # app版本 
client_type=android&     # 固定的
dinfo={
    "ah1":"",
    "ah2":"",
    "ah3":"",
    "ah4":"wifi",  # 手机网络
    "ah5":"1440_2712",
    "ah6":1900800,  # cpu最大功率
    "ah7":8,#cpu核数
    "ah8":3839954944, #内存大小
    "ah9":"Pixel 2 XL", # 手机型号
    "ah10":"",
    "ah11":"",
    "ah12":"",
    "ah13":"",
    "as1":"11",# 安卓版本
    "as2":"","as3":"",
    "as4":"cff15d2b8c13bf22", # 手机id号
    "as5":"","as6":"",
    "as7":"30", # 安卓版本
    "ac1":"a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d"}&
mars_cid=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d& # 破解过，uuid
phone_model=Pixel 2 XL& # 手机型号
session_id=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d_shop_android_1699020913111& # 上次课破解过 uuid+时间戳
sys_version=30& # sdk版本 
vcspKey=4d9e524ad536c03ff203787cf0dfcd29& 破解了，固定的
vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzAxNjEyNjcyfHx8.5474000460661f0cbc4c44ccaaa8c23c # getTokenByFP返回的
```

![image-20231103223046002](imgs/day20-课堂笔记.assets/image-20231103223046002.png)



## 3.7 代码整合--》generate_token发送请求

```python
import random
import time
import uuid
from base64 import b64encode
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
from urllib.parse import quote_plus
import requests
import hashlib

requests.packages.urllib3.disable_warnings()  # https 会有红色警告，去掉

# ====================== 注册设备 ======================
mars_cid = device_token = str(uuid.uuid4())
android_id = ''.join(["%x" % random.randint(1, 15) for i in range(16)])
build_model = "Pixel 2 XL"
ctime = str(int(time.time()))


def sha1(data_string):
    # sha1加密
    hash_object = hashlib.sha1()
    hash_object.update(data_string.encode('utf-8'))
    arg7 = hash_object.hexdigest()
    return arg7

device_token = str(uuid.uuid4())
param_dict = {
    'app_name': 'achievo_ad',
    'app_version': '7.83.3',
    'device_token': device_token,
    'status': 1,
    'warehouse': 'null',
    'manufacturer': 'Google',
    'device': build_model,
    'os_version': '30',
    'channel': 'oziq7dxw:::',
    'vipruid': '',
    'regPlat': '0',
    'regid': '',
    'rom': 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)',
    'skey': '6692c461c3810ab150c9a980d0c275ec',

}

ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])

salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{ordered_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.get(
    url="https://mp.appvipshop.com/apns/device_reg",
    params=param_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },verify=False
)
print("1.注册设备", res.text)


# ====================== getTokenByFP ======================
res = requests.get(
    url="https://vcsp-api.vip.com/token/getTokenByFP?vcspKey=4d9e524ad536c03ff203787cf0dfcd29",
    headers={
        "vcspauthorization": "vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387"
    },verify=False
)

print(res.text)
vsp_dict = res.json()['data']

# ====================== generate_token ======================

dinfo = '{"ah1":"","ah2":"","ah3":"","ah4":"wifi","ah5":"1080_2189","ah6":1804800,"ah7":8,"ah8":7742595072,"ah9":"%s","ah10":"","ah11":"","ah12":"","ah13":"","as1":"10","as2":"","as3":"","as4":"%s","as5":"","as6":"","as7":"29","ac1":"%s"}' % (
    build_model, android_id, device_token)

data_dict = {
    "app_name": "shop_android",
    "app_version": "7.83.3",
    "client_type": "android",
    "dinfo": quote_plus(dinfo),
    "mars_cid": mars_cid,
    "phone_model": build_model,
    "session_id": "{}_shop_android_{}".format(mars_cid, ctime),
    "sys_version": "29",
    "vcspKey": "4d9e524ad536c03ff203787cf0dfcd29",
    "vcspToken": vsp_dict['vcspToken']
}

data = "&".join(["{}={}".format(key, data_dict[key]) for key in sorted(data_dict.keys())])
iv = ''.join(["%x" % random.randint(1, 15) for i in range(16)])

obj = hashlib.md5()
obj.update(b'aee4c425dbb2288b80c71347cc37d04b')
key = obj.digest()

aes = AES.new(
    key=key,
    mode=AES.MODE_CBC,
    iv=iv.encode('utf-8')
)
raw = pad(data.encode('utf-8'), 16)
encrypt_bytes = aes.encrypt(raw)
total_bytes = iv.encode('utf-8') + encrypt_bytes
edata = b64encode(total_bytes).decode('utf-8')

body_dict = {
    'api_key': "23e7f28019e8407b98b84cd05b5aef2c",
    'did': "",
    'edata': edata,
    'eversion': "0",
    'skey': "6692c461c3810ab150c9a980d0c275ec",
    'timestamp': int(time.time())
}

body_string = "&".join(["{}={}".format(key, body_dict[key]) for key in sorted(body_dict.keys())])
# print(body_string)
salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{body_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.post(
    url="https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token",
    data=body_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },
    verify=False
)
print("3.token", res.text)
```





# 4 唯品会搜索功能-代码整合

```python
import random
import time
import uuid
from base64 import b64encode
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
from urllib.parse import quote_plus
import requests
import hashlib

requests.packages.urllib3.disable_warnings()  # https 会有红色警告，去掉

# ====================== 注册设备 ======================
api_key = "23e7f28019e8407b98b84cd05b5aef2c"
skey = '6692c461c3810ab150c9a980d0c275ec'

mars_cid = device_token = str(uuid.uuid4())
android_id = ''.join(["%x" % random.randint(1, 15) for i in range(16)])
build_model = "Pixel 2 XL"
ctime = str(int(time.time()))
session_id = "{}_shop_android_1669730552506".format(mars_cid, ctime)


def sha1(data_string):
    # sha1加密
    hash_object = hashlib.sha1()
    hash_object.update(data_string.encode('utf-8'))
    arg7 = hash_object.hexdigest()
    return arg7

device_token = str(uuid.uuid4())
param_dict = {
    'app_name': 'achievo_ad',
    'app_version': '7.83.3',
    'device_token': device_token,
    'status': 1,
    'warehouse': 'null',
    'manufacturer': 'Google',
    'device': build_model,
    'os_version': '30',
    'channel': 'oziq7dxw:::',
    'vipruid': '',
    'regPlat': '0',
    'regid': '',
    'rom': 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)',
    'skey': '6692c461c3810ab150c9a980d0c275ec',

}

ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])

salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{ordered_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.get(
    url="https://mp.appvipshop.com/apns/device_reg",
    params=param_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },verify=False
)
print("1.注册设备", res.text)


# ====================== getTokenByFP ======================
res = requests.get(
    url="https://vcsp-api.vip.com/token/getTokenByFP?vcspKey=4d9e524ad536c03ff203787cf0dfcd29",
    headers={
        "vcspauthorization": "vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387"
    },verify=False
)

print(res.text)
vsp_dict = res.json()['data']

# ====================== generate_token ======================

dinfo = '{"ah1":"","ah2":"","ah3":"","ah4":"wifi","ah5":"1080_2189","ah6":1804800,"ah7":8,"ah8":7742595072,"ah9":"%s","ah10":"","ah11":"","ah12":"","ah13":"","as1":"10","as2":"","as3":"","as4":"%s","as5":"","as6":"","as7":"29","ac1":"%s"}' % (
    build_model, android_id, device_token)

data_dict = {
    "app_name": "shop_android",
    "app_version": "7.83.3",
    "client_type": "android",
    "dinfo": quote_plus(dinfo),
    "mars_cid": mars_cid,
    "phone_model": build_model,
    "session_id": "{}_shop_android_{}".format(mars_cid, ctime),
    "sys_version": "29",
    "vcspKey": "4d9e524ad536c03ff203787cf0dfcd29",
    "vcspToken": vsp_dict['vcspToken']
}

data = "&".join(["{}={}".format(key, data_dict[key]) for key in sorted(data_dict.keys())])
iv = ''.join(["%x" % random.randint(1, 15) for i in range(16)])

obj = hashlib.md5()
obj.update(b'aee4c425dbb2288b80c71347cc37d04b')
key = obj.digest()

aes = AES.new(
    key=key,
    mode=AES.MODE_CBC,
    iv=iv.encode('utf-8')
)
raw = pad(data.encode('utf-8'), 16)
encrypt_bytes = aes.encrypt(raw)
total_bytes = iv.encode('utf-8') + encrypt_bytes
edata = b64encode(total_bytes).decode('utf-8')

body_dict = {
    'api_key': "23e7f28019e8407b98b84cd05b5aef2c",
    'did': "",
    'edata': edata,
    'eversion': "0",
    'skey': "6692c461c3810ab150c9a980d0c275ec",
    'timestamp': int(time.time())
}

body_string = "&".join(["{}={}".format(key, body_dict[key]) for key in sorted(body_dict.keys())])
# print(body_string)
salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{body_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.post(
    url="https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token",
    data=body_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },
    verify=False
)
print("3.token", res.text)
did = res.json()['data']['token']['did']

# ====================== 搜索 ======================

key_word = "裤子"

search_dict = {
    "api_key": api_key,
    "app_name": "shop_android",
    "app_version": "7.83.3",
    "bigSaleTagIds": "",
    "brandIds": "",
    "brandStoreSns": "",
    "categoryId": "",
    "channelId": "1",
    "channel_flag": "0_1",
    "client": "android",
    "client_type": "android",
    "darkmode": "0",
    "deeplink_cps": "",
    "device_model": "".format(build_model),
    "did": did,
    "elder": "0",
    "extParams": '{"priceVer":"2","mclabel":"1","cmpStyle":"1","statusVer":"2","ic2label":"1","video":"2","preheatTipsVer":"4","floatwin":"1","superHot":"1","exclusivePrice":"1","router":"1","coupons":"1","needVideoExplain":"1","rank":"2","needVideoGive":"1","bigBrand":"1","couponVer":"v2","videoExplainUrl":"1","live":"1","sellpoint":"1","reco":"1","vreimg":"1","search_tag":"2","tpl":"1","stdSizeVids":"","labelVer":"2"}',
    "fdc_area_id": "101103104123",
    "functions": "RTRecomm,flagshipInfo,feedback,otdAds,zoneCode,slotOp,survey,hasTabs,floaterParams",
    "harmony_app": "0",
    "harmony_os": "0",
    "headTabType": "all",
    "height": "2189",
    "isMultiTab": "0",
    "keyword": key_word,
    "lastPageProperty": '{"isBgToFront":"0","suggest_text":"%s","scene_entry_id":"-99","refer_page_id":"page_te_globle_classify_search_1669733882852","text":"%s","tag":"1","module_name":"com.achievo.vipshop.search","type":"all","typename":"全部","is_back_page":"0"}' %(key_word,key_word),
    "maker": "REDMI",
    "mars_cid": mars_cid,
    "mobile_channel": "oziq7dxw:::",
    "mobile_platform": "3",
    "net": "WIFI",
    "operator": "中国电信",
    "os": "Android",
    "osv": "10",
    "otddid": "",
    "other_cps": "",
    "page_id": "page_te_commodity_search_{}".format(int(time.time() * 1000) - 200),
    "phone_model": build_model,
    "priceMax": "",
    "priceMin": "",
    "props": "",
    "province_id": "101103",
    "referer": "com.achievo.vipshop.search.activity.TabSearchProductListActivity",
    "rom": "Dalvik/2.1.0 (Linux; U; Android 10; M2007J17C MIUI/V12.0.11.0.QJSCNXM)",
    "sd_tuijian": "0",
    "service_provider": "46011",
    "session_id": session_id,
    "skey": skey,
    "sort": "0",
    "source": "app",
    "source_app": "android",
    "standby_id": "oziq7dxw:::",
    "sys_version": "29",
    "timestamp": ctime,
    "union_mark": "blank&_&blank&_&oziq7dxw:::&_&blank&_&blank",
    "vipService": "",
    "warehouse": "VIP_BJ",
    "width": "1080"
}

search_string = "&".join(["{}={}".format(key, search_dict[key]) for key in sorted(search_dict.keys())])
# print(body_string)
salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{search_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.post(
    url="https://mapi.appvipshop.com/vips-mobile/rest/shopping/search/product/list/v1",
    data=search_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },
    verify=False
)
print(res.text)
```

# 5 总结

```python
# 1 定位搜索接口：
	https://mapi.appvipshop.com/vips-mobile/rest/shopping/search/product/list/v1
    需要破的：
    api_key：23e7f28019e8407b98b84cd05b5aef2c 
    mars_cid：a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d  
    session_id：a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d _shop_android_1698834176657 
    skey：6692c461c3810ab150c9a980d0c275ec 
    did
    
# 2 did---》通过generate_token返回的
	https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token
    edata：看上去像base64
    
    随机生成的iv+ 对一堆数据加密（vcspToken不知道），其他都知道---》做了base64加密
    
    
 # 3 vcspToken通过 getTokenByFP 返回的
	-vcspKey  固定的 
    -vcspSign  固定的
    
 # 4 注册设备
```




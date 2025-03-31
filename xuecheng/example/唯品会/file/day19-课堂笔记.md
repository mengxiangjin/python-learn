# 今日内容

# 1 今日目标

```python
# 唯品会---》根据商品关键字搜索---》两天时间
# 版本：v7.83.3 版本
# 知识点:
	1 so的延迟hook
    2 java反射
    
    
#1  app安装到手机上
	adb install  app的位置
    
# 2 打开app，在输入框搜索内容，破解该接口

```

![image-20231101200649554](imgs/day19-课堂笔记.assets/image-20231101200649554.png)



# 2 抓包分析

```python
# 1 charles--->手机端配置代理

# 2 搜索---》抓包
	-抓到包---》这个包需要携带很多数据(请求头，请求体)---》有一部分是之前别的请求返回的数据
    -找之前请求--》app装好后第一次打开，这几个请求才会有(清空缓存)
    
    
# 3 搜索商品的请求：
	地址：https://mapi.appvipshop.com/vips-mobile/rest/shopping/search/product/list/v1
    请求方式：post
    请求头：（一个）
    	authorization	OAuth api_sign=e571d25abbd4a1bb8cbd60beddab6c081b14a862
    请求体：
    api_key	23e7f28019e8407b98b84cd05b5aef2c  # 需要破
    app_name	shop_android # 固定
    app_version	7.83.3  # 固定的
    bigSaleTagIds	
    brandIds	
    brandStoreSns	
    categoryId	
    channelId	1
    channel_flag	0_1
    client	android
    client_type	android
    darkmode	0
    deeplink_cps	
    device_model	Google Pixel 2 XL # 手机型号
    elder	0
    extParams	{"priceVer":"2","mclabel":"1","cmpStyle":"1","statusVer":"2","ic2label":"1","video":"2","uiVer":"2","preheatTipsVer":"4","floatwin":"1","superHot":"1","exclusivePrice":"1","router":"1","coupons":"1","needVideoExplain":"1","rank":"2","needVideoGive":"1","bigBrand":"1","couponVer":"v2","videoExplainUrl":"1","live":"1","sellpoint":"1","reco":"1","vreimg":"1","search_tag":"2","tpl":"1","stdSizeVids":"","labelVer":"2"}
    fdc_area_id	103101101113
    functions	RTRecomm,flagshipInfo,feedback,otdAds,zoneCode,slotOp,survey,hasTabs,floaterParams
    harmony_app	0
    harmony_os	0
    headTabType	all
    height	2712
    isMultiTab	0
    keyword	长袖套衫  # 搜索条件
    lastPageProperty	{"isBgToFront":"0","suggest_text":"长袖套衫","scene_entry_id":"-99","refer_page_id":"page_te_globle_classify_search_1698840606324","text":"长袖套衫","tag":"1","module_name":"com.achievo.vipshop.search","type":"all","typename":"全部","is_back_page":"0"}
    maker	GOOGLE
    mars_cid	a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d  # 需要破
    mobile_channel	oziq7dxw:::
    mobile_platform	3
    net	WIFI
    operator	
    os	Android
    osv	11
    otddid	
    other_cps	
    page_id	page_te_commodity_search_1698840618728
    phone_model	pixel 2 xl
    priceMax	
    priceMin	
    props	
    province_id	103101  # 省份数字
    referer	com.achievo.vipshop.search.activity.TabSearchProductListActivity
    rom	Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)
    sd_tuijian	0
    service_provider	
    session_id	a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d_shop_android_1698834176657 # 需要破
    skey	6692c461c3810ab150c9a980d0c275ec # 需要破
    sort	0
    source	app
    source_app	android
    standby_id	oziq7dxw:::
    sys_version	30
    timestamp	1698840618 # 时间戳
    union_mark	blank&_&blank&_&oziq7dxw:::&_&blank&_&blank
    vipService	
    warehouse	VIP_SH   
    width	1440 
    	
        
   -----------需要破的-------------
    api_key：23e7f28019e8407b98b84cd05b5aef2c # 看上去像sha1，md5摘要
    mars_cid：a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d  # uuid
    session_id：a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d _shop_android_1698834176657 # mars_cid+时间戳
    skey：6692c461c3810ab150c9a980d0c275ec # 摘要算法
    
    
    
    
# 4 改包测试
	-去掉请求头中的（authorization）--》API signature must not be empty  必须要传
    -请求体中：随便去一个，都报错
    Invalid API signature 962b50c5714a4eb35590a265462877510e34aac2
    
    
    
# 5 猜测：
	-把请求体的所有内容---》通过某种加密方式得到摘要
    -把摘要放到了请求头中
    -只要请求体中去掉任意一个参数，都会校验失败
    
# 6 多次请求：
 	api_key：23e7f28019e8407b98b84cd05b5aef2c  # 多次请求是一样的
    mars_cid：a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d # 多次请求是一样的
    session_id：a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d _shop_android_1698834176657 # 多次请求是一样的
    skey：6692c461c3810ab150c9a980d0c275ec # 多次请求是一样的
    
    
# 7 最核心就是 authorization 的破解
# 8 第一次发送请求搜索的时候---》did
	did：0.0.f5bb01a00a0871e0c5d670abbacda7d9.c75f2a
    
# 9 反编译app---》搜索发现
	api_key mars_cid session_id skey 都搜到，代码生成的
    唯独：did搜不到 
    did可能如何产生的？
    	1 使用代码产生---》如果使用代码生成，一定能搜到
        2 某个请求返回的数据----》下次请求携带它
        
# 10 如果要破搜索---》必须先要破--》https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token


# 11 generate_token接口---返回了did
	-请求地址：https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token
    -请求方式：post
    -请求头：authorization	OAuth api_sign=ff7c3d6bcfd91c91e6afdcc387e78db082037b05
    -请求体：
        api_key	23e7f28019e8407b98b84cd05b5aef2c  # 看到过
        did	    # 空的
        edata	 # 非常多
        eversion	0 # 固定的
        skey	6692c461c3810ab150c9a980d0c275ec # 看到过
        timestamp	1698842071 # 时间戳
# 12 edata不知道怎么来的
	-搜：某个接口返回的（vcsptoken）用代码 最终生成的---》edata
    
    
# 13 edata是那个接口返回的呢？
	https://vcsp-api.vip.com/token/getTokenByFP?vcspKey=4d9e524ad536c03ff203787cf0dfcd29
# 14 注册设备接口
https://mp.appvipshop.com/apns/device_reg?app_name=achievo_ad&app_version=7.83.3&device_token=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&status=1&warehouse=null&manufacturer=Google&device=Pixel+2+XL&os_version=30&channel=oziq7dxw%3A%3A%3A&vipruid=&regPlat=0&regid=null&rom=Dalvik%2F2.1.0+%28Linux%3B+U%3B+Android+11%3B+Pixel+2+XL+Build%2FRP1A.201005.004.A1%29&skey=6692c461c3810ab150c9a980d0c275ec
    
    
# 15 最终：破解四个接口
    1 https://mp.appvipshop.com/apns/device_reg
    2 https://vcsp-api.vip.com/token/getTokenByFP
    3 https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token
    4 https://mapi.appvipshop.com/vips-mobile/rest/shopping/search/product/list/v1
```

![image-20231101200822624](imgs/day19-课堂笔记.assets/image-20231101200822624.png)



![image-20231101201131466](imgs/day19-课堂笔记.assets/image-20231101201131466.png)



![image-20231101202403916](imgs/day19-课堂笔记.assets/image-20231101202403916.png)

![image-20231101203601252](imgs/day19-课堂笔记.assets/image-20231101203601252.png)



![image-20231101204206986](imgs/day19-课堂笔记.assets/image-20231101204206986.png)

# 3 注册设备接口

```python
# 1 好多app---》app一启动，就会注册设备---》需要携带一些数据---》把这个设备注册上，以后携带固定的值才能请求
# 2 注册设备接口：https://mp.appvipshop.com/apns/device_reg

# 3 详细参数：
	-请求地址：https://mp.appvipshop.com/apns/device_reg
    -请求方式：get
    -请求参数：
    device_token	a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d # 设备号
    skey	6692c461c3810ab150c9a980d0c275ec # 多次发包---》都是固定的，无论那个接口，用的都是一样的
    -请求头：
    authorization	OAuth api_sign=bd16242e8738370e6ea310dad1ff92d49c181040
    
# 4 咱们得目标是：
	device_token
    authorization
```



## 3.1逆向 device_token

```python
# 1 反编译--搜索---》 device_token---》很多
# 2 搜索出11个，不确定那个，随便看几个---》最终发现，殊途同归---》都是uuid
# 3 看第一个
   sb2.append(s.b.f83866a);
    sb2.append("?ordersn=");
    sb2.append(str);
    sb2.append("&device_token=");
    sb2.append(c.Q().m());
# 4 c.Q().m()--》查找声明
   public String m() {
        if (TextUtils.isEmpty(this.f73030x)) {
            MyLog.debug(c.class, "mid isEmpty!!!!!!");
        }
        return this.f73030x;
    }
# 5 找 this.f73030x 在哪赋值的
    public c u0(String str) {
        this.f73030x = str; # 在这里赋值
        CommonsConfig.getInstance().setMid(str);
        ApiConfig.getInstance().setMid(str);
        LogConfig.self().setMid(str);
        return Q();
    }

# 6 谁调用了u0： hook打印调用栈   查找用例
# 7 查找用例：有很多，大致有两类---》随便看---》最终 都是一个位置
	-一类是：uui
    -一类是：Utils.i 生成的
    
# 8 随便看第一个：
hk.c.Q().u0(Utils.i(BaseApplication.getContextObject()));

# 9 Utils.i：先去xml中找，找不到--》生成 安卓uuid---》还没生成就随机生成uuid
    public static String i(Context context) {
        if (CommonsConfig.getInstance().isPreviewModel) {
            return hk.c.Q().m();
        }
        if (p(f39524g)) {
            String stringByKey = CommonPreferencesUtils.getStringByKey(context, CommonsConfig.VIP_MID_KEY);
            f39524g = stringByKey;
            if (p(stringByKey) || DeviceUuidFactory.ANDROIDID_000000000_MID.equals(f39524g)) {
                String uuid = DeviceUuidFactory.getDeviceUuid(context).toString();
                f39524g = uuid;
                if (p(uuid)) {
                    f39524g = UUID.randomUUID().toString(); # 随机生成uuid
                    CommonPreferencesUtils.addConfigInfo(context, CommonsConfig.MID_TYPE_KEY, "3");
                }
                CommonPreferencesUtils.addConfigInfo(context, CommonsConfig.VIP_MID_KEY, f39524g);
            }
        }
        return f39524g;
    }
# 9 使用随机生成的uuid测试---》发现可以

# 10 代码模拟：uuid
import uuid
device_token = str(uuid.uuid4())
```

![image-20231101205201606](imgs/day19-课堂笔记.assets/image-20231101205201606.png)

## 3.2 逆向skey

```python
# 1 搜索---》skey--》搜索到很多
	-发现有个常量是skey---》好多接口请求体中都携带skey
    -程序员会经常性把常用的变量，定义长常量，以后直接取着用
    
# 2 点第一个常量进去发现，很多常量（好多接口都会用）
 	public static final String API_KEY = "api_key";
    public static final String APP_NAME = "app_name";
    public static final String DID = "did";
    public static final String EDATA = "edata";
	public static final String SKEY = "skey";
# 3 程序员习惯，如果一个字符串经常用，会把它定义成常量
	-通过之前抓包--发现skey 多次发送请求，其实是不变的
    -生成一次后，以后都用这个常量的
# 4 查找用例：三种方式：每个都看---》看完后，又是殊途同归--》最终定位到一个位置
	1 调用f生成---》找到的位置
    2 GobalConfig.getSecureKey生成--》一样的
    3 直接使用SecureKey
# 5 看第一个：treeMap.put(ApiConfig.SKEY, f(context, new String[0]));
   public static String f(Context context, String... strArr) {
        if (TextUtils.isEmpty(f2017b)) {
            String info = KeyInfoFetcher.getInfo(context, ApiConfig.SKEY);
            f2017b = info;
            if (TextUtils.isEmpty(info) || f2017b.startsWith("KI ")) {
                KeyInfoFetcher.loadKeyInfoSoWarp((strArr == null || strArr.length <= 0) ? "" : strArr[0]);
                f2017b = KeyInfoFetcher.getInfo(context, ApiConfig.SKEY);
            }
        }
        return f2017b;
    }
# 6 通过：KeyInfoFetcher.getInfo(context, ApiConfig.SKEY) 得到
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
# 7 看如下代码---》java的反射机制
	# python的反射---》通过字符串去对象中找方法（执行）或属性---》java也是一样的
    clazz = KeyInfo.class; # 得到这个类  KeyInfo
    object = KeyInfo.class.newInstance(); # 实例化得到对象  之前new KeyInfo()
    method = clazz.getMethod("getInfo", Context.class, String.class); # 通过字符串找到方法
    method.invoke(object, context, str) # 调用方法，得到返回结果---》传入对象和函数的参数
    
# 8 上述代码的本质：调用KeyInfo类的getInfo方法 得到结果--》直接找到KeyInfo的getInfo
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
# 9 getNavInfo(context, str)--》jni中使用so生成的
private static native String getNavInfo(Context context, String str);


# 10 正常操作---》去so文件中逆向--》找到加密算法---》破解加密算法
	-常量---》赋值一次---》以后请求都是这个---其实我们可以不破--》直接使用固定的值
    
    -使用hook，hook到返回值--》确定--》无论你怎么换设备--》值都是一样的
```

### 3.2.1 hook-getNavInfo看返回值

#### 绕过反调试-打印所有so-删除

```python
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
# Application(identifier="com.achievo.vipshop", name="唯品会", pid=22907, parameters={})


### hook运行了那些so
import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.achievo.vipshop"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {

    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            console.log("[dlopen:]", path);
        },
        onLeave: function (retval) {

        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            console.log("[dlopen_ext:]", path);
        },
        onLeave: function (retval) {

        }
    });


});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
rdev.resume(pid)
sys.stdin.read()


# /data/app/~~PYR1rBhukSZcT4B2KQ_VDw==/com.achievo.vipshop-LBTKI1qDnOWh1s-aZDbLIA==/lib/arm/libmsaoaidsec.so
```



```python
# 现象：hook就闪退（反调试） 删除 `libmsaoaidsec.so`
# 这个请求是注册设备---》删缓存---》卸载重载app

import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.achievo.vipshop"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");

    KeyInfo.getNavInfo.implementation = function (ctx, str) {
        console.log("-----------------");
        console.log("参数==>", str);
        var res = this.getNavInfo(ctx, str);
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
rdev.resume(pid)
sys.stdin.read()


''' 即便换设备，也是这个值
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

'''
```





## 3.3 逆向 authorization

```python
# 1 搜索：
	# 搜：authorization	  多一些
    # 搜 api_sign 少一些
# 2 第一个点进去
	builder.addHeader("Authorization", "OAuth api_sign=" + str);
# 3 str是什么
	str = b.b()得到的
# 4 b.b()源码---返回了a
    public static String b(Context context, TreeMap<String, String> treeMap, String str, String str2) {
        if (treeMap != null && TextUtils.isEmpty(treeMap.get(ApiConfig.SKEY))) {
            treeMap.put(ApiConfig.SKEY, f(context, new String[0]));
        }
        return a(context, treeMap, str);
    }
# 5 查看a
    private static String a(Context context, TreeMap<String, String> treeMap, String str) {
        try {
            if (VCSPCommonsConfig.getContext() == null) {
                VCSPCommonsConfig.setContext(context);
            }
            String apiSign = VCSPSecurityBasicService.apiSign(context, treeMap, str);
            if (TextUtils.isEmpty(apiSign)) {
                String a10 = com.achievo.vipshop.commons.c.a();
                return "p: " + a10 + ", vcsp return empty sign :" + apiSign;
            }
            return apiSign;
        } catch (Exception e10) {
            e10.printStackTrace();
            String a11 = com.achievo.vipshop.commons.c.a();
            return "p: " + a11 + ", Exception:" + e10.getMessage();
        } catch (Throwable th2) {
            th2.printStackTrace();
            String a12 = com.achievo.vipshop.commons.c.a();
            return "p: " + a12 + ", Throwable:" + th2.getMessage();
        }
    }
# 6 返回了apiSign--》通过String apiSign = VCSPSecurityBasicService.apiSign(context, treeMap, str)生成
    public static String apiSign(Context context, TreeMap<String, String> treeMap, String str) throws Exception {
        if (context == null) {
            context = VCSPCommonsConfig.getContext();
        }
        return VCSPSecurityConfig.getMapParamsSign(context, treeMap, str, false);
    }

# 7 返回了VCSPSecurityConfig.getMapParamsSign--》返回了getSignHash
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
        return null;
    }
# 8 getSignHash--》返回了gs
    public static String getSignHash(Context context, Map<String, String> map, String str, boolean z10) {
        try {
            return gs(context.getApplicationContext(), map, str, z10);
        } catch (Throwable th2) {
            VCSPMyLog.error(clazz, th2);
            return "error! params invalid";
        }
    }
# 9 gs
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
# 10 gs总结成四句
clazz = KeyInfo.class
object = KeyInfo.class.newInstance();
gsMethod = clazz.getMethod("gs", Context.class, Map.class, String.class, Boolean.TYPE);
gsMethod.invoke(object, context, map, str, Boolean.valueOf(z10))
# 11 本质就是在执行KeyInfo的gs方法，传入一堆参数

# 12 找KeyInfo的gs方法
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


# 13 返回了：gsNav
# 14 gsNav 是jni的方法---》authorization---》传入一些参数--》返回了加密串
private static native String gsNav(Context context, Map<String, String> map, String str, boolean z10);
# 15 咱们之前分析的--》gsNav--》传入待加密数据（请求体内容）--》返回加密后的签名

# 16 hook-gsNav查看参数和返回值
# 17 so文件阅读
```



![image-20231101214536797](imgs/day19-课堂笔记.assets/image-20231101214536797.png)



### 3.3.1 hook-gsNav查看参数和返回值

```python
# 清除一下数据
import frida
import sys

rdev = frida.get_remote_device()

session = rdev.attach("唯品会")

scr = """
Java.perform(function () {
    var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");
    var TreeMap = Java.use('java.util.TreeMap');


    KeyInfo.gsNav.implementation = function (ctx, map,str,z10) {
        console.log("-----------------gsNav-----------------");
        console.log("参数==>", Java.cast(map,TreeMap).toString());
        console.log("参数==>", str);
        console.log("参数==>", z10);
        var res = this.gsNav(ctx, map,str,z10);
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

'''
1 根据抓包抓到的 authorization	OAuth api_sign=f4f002d40e112a06ecdc04e54d5bf9c92c0477aa 搜索
2 如下
###这些参数就是device_reg这个请求拼出来一些参数，基本都是固定的
参数==> {app_name=achievo_ad, app_version=7.83.3, channel=oziq7dxw:::, device=Pixel 2 XL, device_token=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d, manufacturer=Google, os_version=30, regPlat=0, regid=null, rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1), skey=6692c461c3810ab150c9a980d0c275ec, status=1, vipruid=, warehouse=VIP_SH}
参数==> null
参数==> false
返回的值==> f4f002d40e112a06ecdc04e54d5bf9c92c0477aa
# 待加密的数据，就是注册设备接口 get请求的参数
# 我们依然不知道使用了什么加密方式
'''
```

### 3.3.2 反编译so文件查看

```python
# 1 so文件是 libkeyinfo.so--->32位的
# 2 使用ida打开---》exports

# 3 静态注册  （gsNav）
	java_包名_类名_方法名
    
# 4 Java_com_vip_vcsp_KeyInfo_gsNav 静态注册的方法
int __fastcall Java_com_vip_vcsp_KeyInfo_gsNav(JNIEnv_ *a1, int a2, int a3, int a4, int a5, int a6)
{
  int v9; // r5

  if ( j_Utils_ima(a1, a2, a3) )
    v9 = j_Functions_gs(a1, a2, a4, a5, a6); # 返回了v9，v9通过j_Functions_gs得到
  else
    v9 = 0;
  j_Utils_checkJniException(a1);
  return v9;
}

# 5 j_Functions_gs
int __fastcall j_Functions_gs(int a1, int a2, int a3, int a4, int a5)
{
  return Functions_gs(a1, a2, a3, a4, a5);
}

# 6 Functions_gs
v55 = j_getByteHash(a1, a2, v30, v16, v80, 256);
v58 = strlen(v79),  # 真正长的字符串是 v79，统计v79的长度
(v59 = (const char *)j_getByteHash(a1, a2, v79, v58, v80, 256)) != 0) )
v53 = a1->functions->NewStringUTF(a1, v59); #v59是c语言中字符串
return v53;

#7  j_getByteHash
int __fastcall j_getByteHash(int a1, int a2, int a3, int a4, int a5, int a6)
{
  return getByteHash(a1, a2, a3, a4, a5);
}

#8  getByteHash---》猜，使用sha1摘要---》 纯粹的sha1加密？还是带了盐
char *__fastcall getByteHash(int a1, int a2, int a3, int a4, char *a5)
{
  char *v7; // r10
  int i; // r4
  int v9; // r2
  _QWORD v11[8]; // [sp+0h] [bp-E0h] BYREF
  _DWORD v12[26]; // [sp+44h] [bp-9Ch] BYREF

  if ( !a3 )
    return 0;
  v7 = a5;
  j_SHA1Reset(v12);
  j_SHA1Input(v12, a3, a4);
  if ( j_SHA1Result(v12) )
  {
    for ( i = 0; i != 5; ++i )
    {
      v9 = v12[i];
      v11[0] = 0LL;
      v11[1] = 0LL;
      v11[6] = 0LL;
      v11[7] = 0LL;
      v11[4] = 0LL;
      v11[5] = 0LL;
      v11[2] = 0LL;
      v11[3] = 0LL;
      sprintf((char *)v11, "%08x", v9);
      strcat(a5, (const char *)v11);
    }
  }
  return v7;
}


#8 hook--getByteHash--》看返回值---》看参数（a3和a4）
```

![image-20231101220549587](imgs/day19-课堂笔记.assets/image-20231101220549587.png)



### 3.3.3 hook--getByteHash-手动

```js
// 去内存中中 libkeyinfo.so  getByteHash
var addr = Module.findExportByName("libkeyinfo.so", "getByteHash");
console.log(addr); //0xb696387d



Interceptor.attach(addr,{
    onEnter:function (args){
        this.x1 = args[2];
    },
    onLeave:function(retval) {
        console.log("--------------------")
        console.log(Memory.readCString(this.x1));
        console.log(Memory.readCString(retval));
    }

})

// frida -U -f com.achievo.vipshop -l hook04.js    重启app+hook（出问题）
// frida -UF -l hook04.js                          手动启动+hook


// 纯手动hook，可能不能---》拼手速，有时候很巧，就可以，有时候就不行
// 延迟hook
```

![image-20231101222121854](imgs/day19-课堂笔记.assets/image-20231101222121854.png)

### 3.3.4 延迟hook

```js

function do_hook() {
	setTimeout(function(){
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
     },10);

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

// frida -U -f com.achievo.vipshop -l hook05.js





/*
# 明文
aee4c425dbb2288b80c71347cc37d04b   app_name=achievo_ad&app_version=7.83.3&channel=oziq7dxw:::&device=Pixel 2 XL&device_token=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&manufacturer=Goo
gle&os_version=30&regPlat=0&regid=null&rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)&skey=6692c461c3810ab150c9a980d0c275ec&status=1&vipruid=&warehouse=VIP_SH
# 加密后是
f5fb31c0c3081d18c3f15c193e6f0c3868ae8d14
--------------------
# 明文加密---》返回了   明文前一段都一样   后面一段是上面加密的结果
aee4c425dbb2288b80c71347cc37d04b   f5fb31c0c3081d18c3f15c193e6f0c3868ae8d14
# 这个返回值是抓包抓到的，就是加密后的返回值
f4f002d40e112a06ecdc04e54d5bf9c92c0477aa


##### 传入的明文：前一段都一样
#### 下一个传入的明文，后一段是上一个的加密结果
## 大胆猜测：整个authorization 生成方案
    - 盐：前面一段：aee4c425dbb2288b80c71347cc37d04b
    - 加密的数据：做了两次加密 sha1
 */



// 注册设备请求的请求参数：app_name=achievo_ad&app_version=7.83.3&device_token=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&status=1&warehouse=VIP_SH&manufacturer=Google&device=Pixel+2+XL&os_version=30&channel=oziq7dxw%3A%3A%3A&vipruid=&regPlat=0&regid=null&rom=Dalvik%2F2.1.0+%28Linux%3B+U%3B+Android+11%3B+Pixel+2+XL+Build%2FRP1A.201005.004.A1%29&skey=6692c461c3810ab150c9a980d0c275ec
app_name=achievo_ad&
app_version=7.83.3&
channel=oziq7dxw:::&
device=Pixel 2 XL&
device_token=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&
manufacturer=Google&
os_version=30&
regPlat=0&
regid=null&
rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)&
skey=6692c461c3810ab150c9a980d0c275ec&
status=1&
vipruid=&
warehouse=VIP_SH


// 把 注册设备请求的参数 通过sha1+盐加密==》得到的结果===》再通过sha1+盐加密
```





## 3.4 代码整合

```python
import hashlib

data_string ="aee4c425dbb2288b80c71347cc37d04bapp_name=achievo_ad&app_version=7.83.3&channel=oziq7dxw:::&device=Pixel 2 XL&device_token=a9d1a2b9-2a79-36fd-a8ca-cbe24c03979d&manufacturer=Google&os_version=30&regPlat=0&regid=null&rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)&skey=6692c461c3810ab150c9a980d0c275ec&status=1&vipruid=&warehouse=VIP_SH"

# sha1加密
hash_object = hashlib.sha1()
hash_object.update(data_string.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7) # hook到的：f5fb31c0c3081d18c3f15c193e6f0c3868ae8d14   代码的：f5fb31c0c3081d18c3f15c193e6f0c3868ae8d14

x = "aee4c425dbb2288b80c71347cc37d04b"+arg7
# sha1加密
hash_object = hashlib.sha1()
hash_object.update(x.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7) #hook出来的：f4f002d40e112a06ecdc04e54d5bf9c92c0477aa  自己计算的：f4f002d40e112a06ecdc04e54d5bf9c92c0477aa

```



## 3.5 注册设备代码整合

```python
import requests
import uuid

import hashlib


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
    'device': 'Pixel 2 XL',
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
    },
    verify=False
)
print(res.text)
```




#  今日内容

# 1 今日目标

```python
# 大姨妈app 登录接口
# 今日会学到的重点;
	1 root检测和模拟器绕过(银行类的app都会有)
    2 frida-rpc使用
    3 基于别人的so，自己写安卓应用调用
   

# 版本：v8.6.0
# 安装到手机上
	-adb install xx.apk
# 由于咱么手机root了，一打开app，就弹窗---》不允许咱么继续使用
```

# 2 Root检测原理和绕过

## 2.1 root检测原理

```python
# 1 app在运行时，app内部会写一些函数，函数检测手机有没有root的【特征】，就是检测手机有没有 su 命令

# 2 su 命令(可执行文件)放在的位置：（root方式有很多种：面具，superuser.apk）
	"/system/bin/su", # 不同root软件，生成的位置不同，面具一般在这个目录下
   	"/data/local/bin/su",
    "/data/local/su",
    "/data/local/xbin/su",
    "/sbin/su",
    "/system/app/Superuser.apk",
    "/system/bin/failsafe/su",
    "/su/bin/su",
    "/system/sd/xbin/su",
    "/system/xbin/busybox",
    "/system/xbin/daemonsu",
    "/system/xbin/su",
    "/system/sbin/su",
# 3 app做root检测，就是去某些路径下查找有没有su这个命令，如果有，就是被root了

# 4 手动查看手机有没有被root
	-adb shell  # 进入到手机
    -cd /system/bin # 进入到这个目录下
    -ls  # 查看当前目录下有哪些文件或文件夹
    -ls | grep su  # 查看当前目录下有哪些文件或文件夹  只过滤名字中包含 su 文件或文件夹
```

![image-20231108201315517](imgs/day21-课堂笔记.assets/image-20231108201315517.png)

## 2.2 如何绕过

```python
# 明确了它的检测原理，绕过
	1 反编译+hook---》检测函数---》让它检测函数不执行
    2 改文件名：改su1可执行文件名字
    	aosp刷机--》把原来的su可执行文件，改名字
        
        
# 4种方案绕过
```

## 2.3 通用脚本方案绕过

```python
# 网上有人开源一个绕过root检测的通用脚本
# 地址：https://github.com/AshenOneYe/FridaAntiRootDetection
# 这个东西的原理就是hook方案（可能是c层，可能是java层）---》不让app检测到su文件
# js  hook方案，python的hook方案



### 使用步骤:
# 1 复制它提供的 antiroot.js
# 2 启动frida，端口转发
# 3 运行这个js脚本
# 4 启动app，发现root检测就检测不到了
```

## 2.4 面具+shamiko方案

```python
### 使用步骤
1 把我提供的 Shamiko-v0.5.2-120-release.zip，  推送到手机
	adb push Shamiko-v0.5.2-120-release.zip /sdcard/Download/Shamiko-v0.5.2-120-release.zip
    
2 在手机端，打开 面具，点击模块---》选择本地安装
3 找到放到手机上的Shamiko-v0.5.2-120-release.zip 直接刷入，重启手机
4 打开面具---》就能看到这个模块了--》打开
5 打开面具--》主页中---》右上角(设置)---》配置排除列表--》选择大姨妈app
6 打开大姨妈，就检测不到root了
```

![image-20231108202616615](imgs/day21-课堂笔记.assets/image-20231108202616615.png)

![image-20231108202702383](imgs/day21-课堂笔记.assets/image-20231108202702383.png)



![image-20231108202730240](imgs/day21-课堂笔记.assets/image-20231108202730240.png)



![image-20231108202820302](imgs/day21-课堂笔记.assets/image-20231108202820302.png)

![image-20231108202925949](imgs/day21-课堂笔记.assets/image-20231108202925949.png)

![image-20231108202959910](imgs/day21-课堂笔记.assets/image-20231108202959910.png)



## 2.5 自己反编译--hook方案

![image-20231108203249440](imgs/day21-课堂笔记.assets/image-20231108203249440.png)

```python
# 1 反编译apk---》搜索关键字--》 威胁您
# 2 搜索到--》一个DialogFactory弹窗---》
	-咱们的目标不是不让这个弹窗不弹了
    -目标是看看这个窗为什么会弹---》hook的是 前面的判断条件
    
# 3 搜索到：
 private void isRootPhone() {
        if (!MiscUtil.isSimulator(this) && !MiscUtil.isRooted()) {
            initVariables();
            if (NetUtil.getSharedPreferences(SettingsConfig.KEY_USER_PERMISSION, false)) {
                ScreenAdLoader.pullSSPAd(true);
                return;
            }
            return;
        }
        DialogFactory dialogFactory = new DialogFactory((Context) this, "温馨提示", "运行大姨妈在Root设备或模拟器上,将威胁您的数据安全请您在正常设备上安装使用~", false, new DialogCallBack() { // from class: com.yoloho.dayima.activity.core.Launcher.2
            @Override // com.yoloho.controller.dialog.customdialog.DialogCallBack
            public void negativeOnClickListener() {
            }

            @Override // com.yoloho.controller.dialog.customdialog.DialogCallBack
            public void positiveOnClickListener() {
                Launcher.this.finish();
            }

            @Override // com.yoloho.controller.dialog.customdialog.DialogCallBack
            public void titleRightOnClickListener() {
            }
        });
        dialogFactory.setCancel(false);
        dialogFactory.setNamePositiveButton("退出");
        dialogFactory.show();
    }
# 4 MiscUtil.isSimulator(this)  检测是否是模拟器
public static boolean isSimulator(Context context) {
        return Build.FINGERPRINT.startsWith("generic") || Build.FINGERPRINT.toLowerCase().contains("vbox") || Build.FINGERPRINT.toLowerCase().contains("test-keys") || Build.MODEL.contains("google_sdk") || Build.MODEL.contains("Emulator") || Build.MODEL.contains("MuMu") || Build.MODEL.contains("virtual") || Build.SERIAL.equalsIgnoreCase("android") || Build.MANUFACTURER.contains("Genymotion") || (Build.BRAND.startsWith("generic") && Build.DEVICE.startsWith("generic")) || "google_sdk".equals(Build.PRODUCT) || ((TelephonyManager) context.getSystemService(AliyunLogCommon.TERMINAL_TYPE)).getNetworkOperatorName().toLowerCase().equals("android");
    }
## 手机上有个文件，文件中有对手机的描述：描述了手机型号，sdk版本。。。好多，有的描述中包含 MuMu  virtual ，就说明这个设备是虚拟设备
## 这个文件在：/system/build.prop 
	-linux上使用命令查看这个文件的内容：  cat /system/build.prop 
	-Build.FINGERPRINT
    


# 5 MiscUtil.isRooted()  检测是否root
    public static boolean isRooted() {
        String[] strArr = {"/system/xbin/", "/system/bin/", "/system/sbin/", "/sbin/", "/vendor/bin/", "/su/bin/"};
        for (int i2 = 0; i2 < 6; i2++) {
            try {
                String str = strArr[i2] + bh.y;
                if (new File(str).exists()) {
                    String exec = exec(new String[]{"ls", "-l", str});
                    String str2 = "isRooted=" + exec;
                    if (!TextUtils.isEmpty(exec)) {
                        if (exec.indexOf("root") != exec.lastIndexOf("root")) {
                            return true;
                        }
                    }
                    return false;
                }
            } catch (Exception e2) {
                e2.printStackTrace();
            }
        }
        return false;
    }
# 核心原理是就是去某几个路径下看有没有su这个文件

```

### hook脚本

```python
# hook-isSimulator和isRooted 都返回false
```



```js
// hook 不成功，卸载重装
//1 端口转发

import subprocess
# 使用sbuprocess模块，执行命令，如果转发不了，就执行命令

'''
adb forward tcp:27042 tcp:27042
adb forward tcp:27043 tcp:27043
'''
subprocess.run('adb forward tcp:27042 tcp:27042')
subprocess.run('adb forward tcp:27043 tcp:27043')

//2 js脚本
Java.perform(function () {
    var MiscUtil = Java.use("com.yoloho.libcore.util.MiscUtil");

    MiscUtil.isRooted.implementation = function () {
        return false;
    }

    MiscUtil.isSimulator.implementation = function (ctx) {
        return false;
    }
    var SystemManager = Java.use("com.mobile.auth.gatewayauth.manager.SystemManager");

    SystemManager.checkEnvSafe.implementation = function () {
        return null;
    }
});

// frida -U -f  com.yoloho.dayima -l  root.js
// frida -UF -l  root.js


// python 脚本
import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.yoloho.dayima"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var MiscUtil = Java.use("com.yoloho.libcore.util.MiscUtil");
    MiscUtil.isRooted.implementation = function () {
        console.log('绕过')
        return false;
    }

    MiscUtil.isSimulator.implementation = function (ctx) {
        console.log('绕过')
        return false;
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

## 2.6 aosp刷机方案

```python
# 后面会学习 aosp刷机----》绕过root检测---》定制脱壳机

# aosp是什么
Android是开源的，AOSP（Android Open Source Project）为Android开源项目的缩写,自己编译Android系统


免费开源---》拿到它的源代码---》修改它的代码---》编译---》装到手机上---》自己的操作系统
  鸿蒙
  小米 miui是--》改ui改的多，底层基本没改
```



# 3 抓包

![image-20231108205839943](imgs/day21-课堂笔记.assets/image-20231108205839943.png)

```python
# 请求地址：
https://uicapi.yoloho.com/user/login
# 请求方式
post
# 请求头：
没有特殊
# 请求体
username	18953675221
password	WA89qByLlDeaGjmVNzXm/w== #需要破
sign	eae2f8f6456337b68388dcf5d56c8253 # 需要破
androidid	a8da7415550cd43a #随机生成
mac	C6:07:96:ED:C1:32# mac地址，随机生成
imei	
density	3.5   
brand	google#  固定

# 请求参数：
device	bcae572b84d20c385d6d9d2d7d9e645da29da3c0 # 需要破
ver	630
screen_width	1440
screen_height	2712
model	Pixel 2 XL
sdkver	30
platform	android
releasever	11
channel	360
latt	0
lngt	0
networkType	0
token	
userStatus	0


###需要破的
	1 passoword
    2 sign
    3 device
```



# 4 逆向

## 4.1 device破解

```python
# 1 反编译，搜索 device ，搜到很多
	-分析：device是放在请求参数中，请求参数中还有其他参数，搜索其他少见参数，试一下，如果搜出来的位置也有device，说明位置是正确的
    
    
# 2 找到
	 public StringBuilder setPostData(boolean z) throws UnsupportedEncodingException {
        try {
            StringBuilder sb = new StringBuilder();
            PackageInfo packageInfo = null;
            try {
                packageInfo = getContext().getPackageManager().getPackageInfo(getContext().getPackageName(), 0);
            } catch (PackageManager.NameNotFoundException e2) {
                e2.printStackTrace();
            }
            sb.append("device=");
            sb.append(URLEncoder.encode(getDeviceCode(), "UTF-8"));
            sb.append("&ver=");
            if (packageInfo != null) {
                sb.append(URLEncoder.encode(Integer.toString(packageInfo.versionCode), "UTF-8"));
            }
            sb.append("&screen_width=");
            sb.append(MiscUtil.getScreenWidth() + "");
            sb.append("&screen_height=");
            sb.append(MiscUtil.getScreenHeight() + "");
            sb.append("&model=");
            sb.append(URLEncoder.encode(Build.MODEL, "UTF-8"));
            sb.append("&sdkver=");
            sb.append(URLEncoder.encode(Build.VERSION.SDK, "UTF-8"));
            sb.append("&platform=android");
            sb.append("&releasever=");
            sb.append(URLEncoder.encode(Build.VERSION.RELEASE));
            sb.append("&channel=");
            sb.append(MiscUtil.getAppMeta(ApplicationManager.getContext(), "UMENG_CHANNEL") + "");
            sb.append("&latt=");
            sb.append(getLat());
            sb.append("&lngt=");
            sb.append(getLng());
            sb.append("&networkType=");
            sb.append(NetUtil.getCurrentNetworkType());
            String currentPeriod2 = getCurrentPeriod();
            if (!currentPeriod2.equals("")) {
                sb.append("&");
                sb.append(currentPeriod2);
            }
            String currentPeriodDay2 = getCurrentPeriodDay();
            if (!currentPeriodDay2.equals("")) {
                sb.append("&");
                sb.append(currentPeriodDay2);
            }
            if (z) {
                sb.append("&token=");
                sb.append(URLEncoder.encode(getToken(), "UTF-8"));
            }
            sb.append("&userStatus=");
            sb.append(CoreSettings.get(SettingsConfig.KEY_INFO_MODE).equals("") ? "0" : CoreSettings.get(SettingsConfig.KEY_INFO_MODE));
            return sb;
        } catch (Exception e3) {
            StringBuilder sb2 = new StringBuilder();
            if (z) {
                sb2.append("&token=");
                sb2.append(URLEncoder.encode(getToken(), "UTF-8"));
            }
            e3.printStackTrace();
            return sb2;
        }
    }

# 3 核心代码
sb.append("device=");
sb.append(URLEncoder.encode(getDeviceCode(), "UTF-8")); # URLEncoder.encode 编码，只有有中文才有用，其他没啥用

# 4 核心就是 getDeviceCode()
    public String getDeviceCode() {
        String str;
        synchronized (lock_device) {
            if (deviceCode == null) {
                setDeviceCode();
            }
            str = deviceCode;
        }
        return str;
    }
# 5 查看 setDeviceCode
public void setDeviceCode() {
        String str;
        String str2;
        String str3;
        if (NetUtil.getSharedPreferences(SettingsConfig.KEY_USER_PERMISSION, false) && deviceCode == null) {
            deviceCode = "NotFound";
            String str4 = null;
            try {
                try {
                    str = ((TelephonyManager) getContext().getSystemService(AliyunLogCommon.TERMINAL_TYPE)).getDeviceId();
                } catch (Exception e2) {
                    e2.printStackTrace();
                    str = null;
                }
                try {
                    str2 = Build.BOARD + Build.BRAND + Build.CPU_ABI + Build.DEVICE + Build.DISPLAY + Build.HOST + Build.ID + Build.MANUFACTURER + Build.MODEL + Build.PRODUCT + Build.TAGS + Build.TYPE + Build.USER;
                } catch (Exception e3) {
                    e3.printStackTrace();
                    str2 = null;
                }
                try {
                    str3 = Settings.Secure.getString(getContext().getContentResolver(), "android_id");
                } catch (Exception e4) {
                    e4.printStackTrace();
                    str3 = null;
                }
                try {
                    str4 = DayimaUtil.getPhoneMac();
                } catch (Exception e5) {
                    e5.printStackTrace();
                }
                String str5 = "";
                if (!Build.MODEL.equals("vivo X1w") || !Build.VERSION.RELEASE.equals(FaceEnvironment.SDK_VERSION)) {
                    try {
                        BluetoothAdapter defaultAdapter = BluetoothAdapter.getDefaultAdapter();
                        if (defaultAdapter != null) {
                            str5 = defaultAdapter.getAddress();
                        }
                    } catch (Exception e6) {
                        e6.printStackTrace();
                    }
                }
                String str6 = str + str3 + str2 + str4 + str5;
                MessageDigest messageDigest = MessageDigest.getInstance("sha-1");
                messageDigest.update(str6.getBytes());
                byte[] digest = messageDigest.digest();
                StringBuffer stringBuffer = new StringBuffer();
                for (byte b : digest) {
                    String lowerCase = Integer.toHexString(b & 255).toLowerCase(Locale.getDefault());
                    if (lowerCase.length() < 2) {
                        lowerCase = "0" + lowerCase;
                    }
                    stringBuffer.append(lowerCase);
                }
                deviceCode = stringBuffer.toString();
            } catch (Exception e7) {
                e7.printStackTrace();
            }
        }
    }

# 7 核心--》几个字符串加到一起，使用sha1加密--》转成16进制--》转成小写--》赋值给了deviceCode
String str6 = str + str3 + str2 + str4 + str5;
MessageDigest messageDigest = MessageDigest.getInstance("sha-1");
messageDigest.update(str6.getBytes());
byte[] digest = messageDigest.digest();
String lowerCase = Integer.toHexString(b & 255).toLowerCase(Locale.getDefault());
if (lowerCase.length() < 2) {
    lowerCase = "0" + lowerCase;
}
stringBuffer.append(lowerCase);


# 8 hook一下 setDeviceCode--messageDigest.update--》看update传入的字符串是什么
	-只hook--messageDigest.update会有很多输出，不知道是哪个
    -通时hook  setDeviceCode和messageDigest.update
    	执行了setDeviceCode 再执行的updata才是咱们想要的
```

![image-20231108210600591](imgs/day21-课堂笔记.assets/image-20231108210600591.png)



### 4.1.1 hook脚本

```js
Java.perform(function () {
    var MiscUtil = Java.use("com.yoloho.libcore.util.MiscUtil");
	// 绕过root的
    MiscUtil.isRooted.implementation = function () {
        return false;
    }
    MiscUtil.isSimulator.implementation = function (ctx) {
        return false;
    }

    // 想查看messageDigest.update(str6.getBytes()) 如参，只需要hook update即可
    // 再hook时，会有很多地方调用update
    // hook setDeviceCode --一开始打印了一句话
    // setDeviceCode里面调用了update---》再结束打印了一句话
    // hook完定位时 只要在
    
    /*
    -------------------------setDeviceCode-------------------------
    console.log(ByteString.of(data).utf8(), '\n' );
    ---------------
    */

    var PeriodAPIV2 = Java.use("com.yoloho.controller.api.PeriodAPIV2");
    var flag = false;
    
    PeriodAPIV2.setDeviceCode.implementation = function () {
        console.log("-------------------------setDeviceCode-------------------------")
        flag = true;
        return this.setDeviceCode();
    }

    var MessageDigest = Java.use("java.security.MessageDigest");
    var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    MessageDigest.update.overload("[B").implementation = function (data) {
        if (flag) {
            console.log(ByteString.of(data).utf8(), '\n' );
            console.log("---------------")
        }
        return this.update(data);
    }
    

});
// frida -U -f  com.yoloho.dayima -l 2.hook.js

/*
 -------------------------setDeviceCode-------------------------
 
String str6 = str + str3 + str2 + str4 + str5;

null                          #str ：getDeviceId
a8da7415550cd43a              # str3  安卓id，可以随机生成 android_id
taimengooglearm64-v8ataimenRP1A.201005.004.A1abfarm-01392RP1A.201005.004.A1GooglePixel 2 XLtaimenrelease-keysuserandroid-build # str2  ：指纹信息 Build.BOARD + Build.BRAND + Build.CPU_ABI + Build.DEVICE + Build.DISPLAY + Build.HOST + Build.ID + Build.MANUFACTURER + Build.MODEL + Build.PRODUCT + Build.TAGS + Build.TYPE + Build.USER;


C6:07:96:ED:C1:32  # str4  wifi信息 mac地址
02:00:00:00:00:00  # str5  蓝牙信息  BluetoothAdapter.getDefaultAdapter

---------------

*/
// device 针对于一个手机是不变的 
```

### 4.1.2 python实现

```python
import hashlib

data_string ="nulla8da7415550cd43ataimengooglearm64-v8ataimenRP1A.201005.004.A1abfarm-01392RP1A.201005.004.A1GooglePixel 2 XLtaimenrelease-keysuserandroid-buildC6:07:96:ED:C1:3202:00:00:00:00:00"

# sha1加密
hash_object = hashlib.sha1()
hash_object.update(data_string.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7)
```



## 4.2 密码破解

```python
# 1 搜索 "password
# 2 搜索到：
# str：手机号    str2：明文密码
public void loginByAccount(final String str, final String str2) {
        getLoginLoading().show();
        Observable.create(new Observable.OnSubscribe<JSONObject>() { // from class: com.yoloho.kangseed.presenter.entrance.LoginByAccountPresenter.3
            @Override 
            public void call(Subscriber<? super JSONObject> subscriber) {
                JSONObject jSONObject;
                ArrayList arrayList = new ArrayList();
                arrayList.add(new BasicNameValuePair("username", str));# 手机号放入
                # 通过str2明文密码  str手机号 生成了一个加密后的密码
                String privateStrHandle = DayimaPrivateUtil.privateStrHandle(str2, str);
                arrayList.add(new BasicNameValuePair("password", privateStrHandle));
                StringBuilder sb = new StringBuilder();
                sb.append(PeriodAPIV2.getInstance().getDeviceCode());
                sb.append("user/login");
                sb.append(str);
                sb.append(privateStrHandle);
                # sign：先留在这，后面破sign再来看
                arrayList.add(new BasicNameValuePair("sign", Crypt.encrypt_data(0L, sb.toString(), sb.length())));
                try {
                    jSONObject = PeriodAPIV2.getInstance().api("user", "login", arrayList);
                } catch (ServiceException e2) {
                    e2.printStackTrace();
                    jSONObject = null;
                }
                subscriber.onNext(jSONObject);
            }
        })
    
# 3 String privateStrHandle = DayimaPrivateUtil.privateStrHandle(str2, str);
    -传入了手机号和明文密码
    -str2传入了成了str
    -str传入了成了str2
    public static String privateStrHandle(String str, String str2) {
        # 传了第一个参数：明文密码
        # 第二个参数：手机号通过md5加密得到摘要后 截取了16位
        # 第三个参数：yoloho_dayima!%_ 固定字符串
        String encrypt = AESUtil.encrypt(str, MD5Util.getMD5(str2).substring(0, 16).toLowerCase(), "yoloho_dayima!%_");
        return TextUtils.isEmpty(encrypt) ? str : encrypt;
    }

# 4 AESUtil.encrypt
    
public class AESUtil {
    public static String encrypt(String str, String str2, String str3) {
        try {
            return Base64.encodeBytes(genAESCipher(str2, str3, 1).doFinal(str.getBytes("utf-8")));
        } catch (Exception unused) {
            return "";
        }
    }

    public static Cipher genAESCipher(String str, String str2, int i2) {
        # aes的key---》str---》调用genAESCipher(str2）传入，传入了str2--调用encrypt的第二个参数--》真正的key 是 手机号使用md5加密后取了16位
        SecretKeySpec secretKeySpec = new SecretKeySpec(str.getBytes(), "AES");
        IvParameterSpec ivParameterSpec = new IvParameterSpec(str2.getBytes());
        try {
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(i2, secretKeySpec, ivParameterSpec);
            return cipher;
        } catch (InvalidAlgorithmParameterException e2) {
            throw new RuntimeException(e2);
        } catch (InvalidKeyException e3) {
            throw new RuntimeException(e3);
        } catch (NoSuchAlgorithmException e4) {
            throw new RuntimeException(e4);
        } catch (NoSuchPaddingException e5) {
            throw new RuntimeException(e5);
        }
    }
}
    
    
# 整体逻辑
    明文密码  手机号做md5加密得到0-16位  固定字符串   传入了 AES 加密得到结果
    
    - aes的key 是什么：手机号使用md5加密后取了16位
    - aes的iv是什么：固定字符串：yoloho_dayima!%_
    - aes的明文是什么：明文密码
```

![image-20231108214757026](imgs/day21-课堂笔记.assets/image-20231108214757026.png)

### 4.2.1 hook---》encrypt--看参数

```js
Java.perform(function () {

    // 绕过root检测############
    var MiscUtil = Java.use("com.yoloho.libcore.util.MiscUtil");
    MiscUtil.isRooted.implementation = function () {
        return false;
    }
    MiscUtil.isSimulator.implementation = function (ctx) {
        return false;
    }
    // 绕过root检测############

    // hook去掉吐司 手机不安全 提示
    var SystemManager = Java.use("com.mobile.auth.gatewayauth.manager.SystemManager");
    SystemManager.checkEnvSafe.implementation = function () {
        return null;
    }
    //hook去掉吐司 手机不安全 提示


    var AESUtil = Java.use("com.yoloho.libcore.util.AESUtil");

    AESUtil.encrypt.implementation = function (str, str2, str3) {
        //传了第一个参数：明文密码
        //第二个参数：手机号通过md5加密得到摘要后 截取了16位
        //第三个参数：yoloho_dayima!%_ 固定字符串
        console.log(str, str2, str3)
        return this.encrypt(str, str2, str3);
    }


});

// frida -U -f  com.yoloho.dayima -l 6-hook---encrypt--看参数.js
// lqz12345 9eb091a1fb36369d yoloho_dayima!%_
//          9eb091a1fb36369d
```



### 4.2.2 python实现密码加密

```python
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

KEY = "9eb091a1fb36369d"
IV = "yoloho_dayima!%_"

password = "lqz12345"

aes = AES.new(
    key=KEY.encode('utf-8'),
    mode=AES.MODE_CBC,
    iv=IV.encode('utf-8')
)
raw = pad(password.encode('utf-8'), 16)
res = base64.b64encode(aes.encrypt(raw))
print(res) # WA89qByLlDeaGjmVNzXm/w== 跟抓包一样
```





## 4.3 sign破解

```python
# 1 sign 上面找到了
 arrayList.add(new BasicNameValuePair("sign", Crypt.encrypt_data(0L, sb.toString(), sb.length())));
    
# 2 传了3个参数	
	-0
    -sb.toString 字符串  getDeviceCode+"user/login"+手机号+密文密码
    - 字符串长度  
    
    
# 3 Crypt.encrypt_data
public class Crypt {
    static {
        System.loadLibrary("Crypt");
    }
	# 三个参数：
    public static native String encrypt_data(long j2, String str, long j3);
}

# 4 正常---》逆向so---》libCrypt.so---64位
	-静态注册---》反编译读c代码---》复现过程---》硬破
    -Java_com_yoloho_libcore_util_Crypt_encrypt_data
    
# 5 今天使用 frida-rpc方案
	-不需要读懂加密逻辑
    -只要传入该传的参数--》直接把加密结果返回---》拿到加密结果直接用即可
    
    
    
# 6 破解so---》静态注册
jstring __fastcall Java_com_yoloho_libcore_util_Crypt_encrypt_1data(JNIEnv_ *a1, __int64 a2, __int64 a3, __int64 a4)
{
  jsize v7; // w22
  const char *v8; // x0
  char v10[36]; #空数组
  __int64 v11; // [xsp+28h] [xbp-38h]

  v11 = *(_QWORD *)(_ReadStatusReg(ARM64_SYSREG(3, 3, 13, 0, 2)) + 40);
  v7 = a1->functions->GetStringUTFLength((JNIEnv *)a1, (jstring)a4);
  v8 = a1->functions->GetStringUTFChars(a1, a4, 0LL);
  sub_1DA0(a3, v8, v7, v10); # 对v10进行操作
  return a1->functions->NewStringUTF(a1, v10); # 返回了v10字符串
}


# 7 sub_1DA0(a3, v8, v7, v10)
 sprintf(a4, "%02x", (unsigned __int8)v27[0]);
  sprintf(a4 + 2, "%02x", (unsigned __int8)v27[1]);
  sprintf(a4 + 4, "%02x", (unsigned __int8)v27[2]);
  sprintf(a4 + 6, "%02x", (unsigned __int8)v27[3]);
  sprintf(a4 + 8, "%02x", (unsigned __int8)v27[4]);
  sprintf(a4 + 10, "%02x", (unsigned __int8)v27[5]);
  sprintf(a4 + 12, "%02x", (unsigned __int8)v27[6]);
  sprintf(a4 + 14, "%02x", (unsigned __int8)v27[7]);
  sprintf(a4 + 16, "%02x", (unsigned __int8)v27[8]);
  sprintf(a4 + 18, "%02x", (unsigned __int8)v27[9]);
  sprintf(a4 + 20, "%02x", (unsigned __int8)v27[10]);
  sprintf(a4 + 22, "%02x", (unsigned __int8)v27[11]);
  sprintf(a4 + 24, "%02x", (unsigned __int8)v27[12]);
  sprintf(a4 + 26, "%02x", (unsigned __int8)v27[13]);
  sprintf(a4 + 28, "%02x", (unsigned __int8)v27[14]);
  return sprintf(a4 + 30, "%02x", (unsigned __int8)v27[15]);


# 8 看上去比较复杂，不硬破了
```



# 5 frida-rpc介绍和使用

## 5.1 以后如果遇到so文件加密--破解方案有哪几种

```python
# 1 硬破--》之前都是这么做
# 2 frida-rpc方案，直接调用so的方法，拿到加密串
# 3 自己写个安卓项目，把被人的so放到我们项目中，直接调用方法，传入参数，得到加密串
# 4 unidbg，java代码模拟出手机app运行环境---》调用so中的方法--》后面学
```

## 5.2 frida-rpc是什么

```python
frida 提供了一种跨平台的 rpc (远程过程调用)机制,通过 frida rpc 可以在主机和目标设备之间进行通信,并在目标设备上执行代码
Frida-RPC 是一个基于 Frida 框架的扩展，用于在不同进程之间进行远程过程调用（RPC）。Frida 是一个功能强大的动态插桩工具，它允许开发人员在运行时监控、修改和控制应用程序的行为。通过使用 Frida-RPC，您可以在不同的进程之间建立通信通道，使得您能够从一个进程中调用另一个进程的函数或方法，就好像它们都在同一个进程中一样


# 缺点:
	-依赖于frida，还得运行app，脱离他们无法执行
    
    
    
    
# rpc: 远程过程调用---》调用远端机器上一个 函数，就跟调用本地的函数是一样的
	后端开发，微服务，服务和服务间调用，通常使用rpc方案
    	- springcloud
        - grpc
        - dubbo
# Frida-RPC 基于frida的远程过程调用

```

![image-20231108222737223](imgs/day21-课堂笔记.assets/image-20231108222737223.png)



![image-20231108223024832](imgs/day21-课堂笔记.assets/image-20231108223024832.png)

## 5.3 电脑写脚本通过frida-rpc调用手机上的方法

```python
# 流程
1 手机端启动 frida-server
2 运行app（app不运行，内存中没有这个方法，就调用不到）
3 电脑端端口
4 写脚本运行

```



```python
import frida

rdev = frida.get_remote_device()
session = rdev.attach("大姨妈")

scr = """
rpc.exports = {   
    yy:function(j2,str,j3){
         var res;
         Java.perform(function () { 
            // 包.类
            var Crypt = Java.use("com.yoloho.libcore.util.Crypt");
            // 类中的方法
            res = Crypt.encrypt_data(j2,str,j3);
         });

         return res;
    }
}
"""
script = session.create_script(scr)
script.load()

# 使用python调用
sign = script.exports_sync.yy(0,
                              'bcae572b84d20c385d6d9d2d7d9e645da29da3c0user/login18953675221WA89qByLlDeaGjmVNzXm/w==',
                              85)
print(sign)  # eae2f8f6456337b68388dcf5d56c8253


# 电脑必须连着手机--》手机上必须运行app
```

## 5.4 存在的问题

```python
# 电脑必须连着手机--》手机上必须运行app


# 之前写的脚本----》直接发给用户运行，我们直接运行即可--》python requests

# 现在如果使用了rpc--》代码没法发给用户用

# 解决这个问题：web框架

```



![image-20231108224130460](imgs/day21-课堂笔记.assets/image-20231108224130460.png)



##  代码整合

```python
# requests 发送post请求
	-device
    -password
    -sign
```



# 6 基于别人的so，自己写安卓调用

```python
# 1 新建安卓项目
# 2 把大姨妈的 so文件，放到咱们安卓项目中
	在libs目录下，放入大姨妈的 那些so文件  32位和64位都拿过来
# 3 build.gradle 添加
sourceSets {
        main {
            jniLibs.srcDirs = ['libs']
        }
    }

# 4 编写native类---》必须跟大姨妈包名一样
package com.yoloho.libcore.util;

public class Crypt {
    static {
        System.loadLibrary("Crypt");
    }

    public static native String encrypt_data(long j2, String str, long j3);
}

# 5 app调用
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView tv = findViewById(R.id.text);
        String sign = Crypt.encrypt_data(0, "bcae572b84d20c385d6d9d2d7d9e645da29da3c0user/login18953675221WA89qByLlDeaGjmVNzXm/w==", 85);
        tv.setText(sign);
    }
}
```



![image-20231108224802065](imgs/day21-课堂笔记.assets/image-20231108224802065.png)

![image-20231108225148682](imgs/day21-课堂笔记.assets/image-20231108225148682.png)![image-20231108225925580](imgs/day21-课堂笔记.assets/image-20231108225925580.png)
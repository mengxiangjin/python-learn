# 今日内容

# 1 unidbg是什么

```python
unidbg是一个Java开源项目，可以帮助我们去模拟一个安卓或IOS设备，用于去执行so文件中的算法，从而不需要再去逆向他内部的算法
它是一个基于 unicorn 的逆向工具，可以直接调用Android和iOS中的 so 文件

Allows you to emulate an Android native library, and an experimental iOS emulation
允许您模拟 Android native library 和 实验性的 iOS 模拟



# 之前安卓开发流程
	-我们通过java代码+c代码--》对某个参数进行加密---》得到apk
    
    -普通app：只是使用java对参数进行加密---》直接发送请求--》咱们之前学过的车智赢案例的密码加密--》使用java的md5加密得到---》我们直接逆向java，定位代码完成加密即可
    
    -高级app：使用java代码，调用了c写的so代码，具体的加密是在so中，对参数进行加密--》发送请求--->之前学过的B站，得物。。。
    
    
# 破解so文件加密的几种方式
	1 硬核破解---》直接反编译搜--》读代码逻辑--》使用python实现---》之前咱们学过：得物【难度很大】
    2 frida-rpc---》不需要硬核破解--》直接远程过程调用so文件中的某个方法--》传入参数---》返回了加密后的数据--》大姨妈案例---【破解简单--交付麻烦】
    3 自己编写安卓应用---》调用别人的so---》完成加密---【简单--交付麻烦】
    4 unidbg：集合了1和2,3的优点---》不需要手机，也不需要硬核破解---》直接用代码模拟手机--》只需要调用so文件中的某个方法，传入参数--》把结果跑出来---》以后交付用户---》python+java的jar包
    
    
    
# unidbg
	-可以模拟出手机的执行环境---》把apk和要使用so文件放到环境中---》它就能模拟运行这个apk---》我们只需要直接调用 so中某个加密方法--》传入应该传的参数---》最终返回加密后的结果
    -由于unidbg使用java写的---》有些代码需要用java写---》打包成一个jar包---》使用python调用java的jar包---》传入参数--》返回加密后的结果
    
```



# 2 下载和使用

```python
# 下载它（github开源）：https://github.com/zhkl0228/unidbg
# 下载地址：https://github.com/zhkl0228/unidbg/releases  下载最新 v0.9.7版本

# 下载完解压---》java开源的---》使用idea打开---》前提是必须配置好java的开发环境【jdk+idea】
	路径不能有中文
# 确认，unidbg能不能正常使用---》直接运行它的示例代码--》如果能顺利运行，就ok了
找到 unidbg-android/src/test/java/com/anjuke.mobile.sign/SignUtil 右键运行，如果能正常打印出结果，说明unidbg环境搭建完成	
```

![image-20231117201958200](imgs/day24-课堂笔记.assets/image-20231117201958200.png)



![image-20231117202102653](imgs/day24-课堂笔记.assets/image-20231117202102653.png)



![image-20231117202222812](imgs/day24-课堂笔记.assets/image-20231117202222812.png)

# 3 unidbg补环境

```python
# unidbg 模拟了手机设备---》so文件的加密----》有两种方式
	-加密算法，都在so层，全是用c实现的    大姨妈---》不需要补环境
    -加密算法，在so层--》调用了java层---》又在so做了逻辑---》唯品会--》需要补环境
    
# 所谓的补环境--》就是补上c调用java时候的一些类
	本身unidbg就是java写的---》c调用的时候，缺了java的这部分---》要使用java代码把c语言调用它时，缺的类，方法，补完整
```

![image-20231117171531531](imgs/day24-课堂笔记.assets/image-20231117171531531.png)





![image-20231117172308746](imgs/day24-课堂笔记.assets/image-20231117172308746.png)





# 4 车智赢案例

```python
# 第13天讲的

# 破解sign的时候--》sign是通过des加密得到--》加密的明文我们已经找到了---》但是des加密的秘钥，我们找到了--》jni中的--》get3desKey-->返回了秘钥

# 咱们当前没有去破解so---》通过hook得到了这个秘钥--》拿着直接用的

# 咱们今天，也不去破解so，而是使用unidbg 运行直接得到
```

## 4.1 hook获取的des加密秘钥的代码

```python
import frida
import sys

rdev = frida.get_remote_device()

session = rdev.attach("车智赢_jar包+")

scr = """
Java.perform(function () {
     // 包.类
    var AHAPIHelper = Java.use("com.autohome.ahkit.AHAPIHelper");

    // Hook，替换
    AHAPIHelper.getDesKey.implementation = function(ctx){
        // 执行原来的方法
        var res =this.getDesKey(ctx);
        console.log("DesKey值：",res);
        return res;
    }
});
"""

script = session.create_script(scr)

script.load()
sys.stdin.read()

# appapiche168comappapiche168comap
```

![image-20231117204427430](imgs/day24-课堂笔记.assets/image-20231117204427430.png)

![image-20231117204603614](imgs/day24-课堂笔记.assets/image-20231117204603614.png)



## 4.2 unidbg使用步骤

### 4.2.1 在unidbg项目中创建一个类

```python
# 在unidbg-android/src/test/java/com/nb/demo/CheZhiYing.class

# 为这个类，编写构造方法，sign静态方法，main 运行主函数

package com.nb.demo;

public class CheZhiYing {
    // 构造方法
    public CheZhiYing(){

    }

    // sign 成员方法，用来破解加密
    public  void sign(){

    }

    // 代码右键运行，创建一个main
    public static void main(String[] args) {
        CheZhiYing che =new CheZhiYing();
        che.sign();
    }
}

```

![image-20231117204808351](imgs/day24-课堂笔记.assets/image-20231117204808351.png)

### 4.2.2 设备初始化

```python
# 现在要模拟手机环境---》初始化出手机设备---》unidbg提供的---》写在构造函数中

# 初始化完成--》右键运行，如果不报错，表示初始化成功
```

![image-20231117205742510](imgs/day24-课堂笔记.assets/image-20231117205742510.png)





```java
package com.nb.demo;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.jni.ProxyClassFactory;
import java.io.File;

public class CheZhiYing extends AbstractJni{
    public static AndroidEmulator emulator;  // 静态属性，以后对象和类都可以直接使用
    public static Memory memory;
    public static VM vm;
    public static Module module;
    // 构造方法,以后这个代码，基本是固定的，只需要改app位置即可，其他不用动
    public CheZhiYing() {
        // 1.创建设备（32位或64位模拟器）， 具体看so文件在哪个目录。 在armeabi-v7a就选择32位
        // 传进设备时，如果是32位，后面so文件就要用32位，同理需要用64位的
        // 这个名字可以随便写,一般写成app的包名    以后可能会动
        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.che168.autotradercloud").build();
        // 2.获取内存对象（可以操作内存）
        memory = emulator.getMemory();
        // 3.设置安卓sdk版本（只支持19、23）
        memory.setLibraryResolver(new AndroidResolver(23));

        // 4.创建虚拟机（运行安卓代码需要虚拟机，就想运行py代码需要python解释器一样）    以后会动
        vm = emulator.createDalvikVM(new File("apks/che/che3.32.1.apk"));
        vm.setJni(this); // 后期补环境会用，把要补的环境，写在当前这个类中，执行这个代码即可，但是必须继承AbstractJni
        //vm.setVerbose(true); //是否展示调用过程的细节

        // 5.加载so文件
        DalvikModule dm = vm.loadLibrary(new File("apks/che/libnative-lib.so"), false);   // 以后会动
        dm.callJNI_OnLoad(emulator); // jni开发动态注册，会执行JNI_OnLoad，如果是动态注册，需要执行一下这个，如果静态注册，这个不需要执行，车智赢案例是静态注册

        // 6.dm代表so文件，dm.getModule()得到module对象，基于module对象可以访问so中的成员。
        module = dm.getModule(); // 把so文件加载到内存后，后期可以获取基地址，偏移量等，该变量代指so文件

    }

    // sign 成员方法，用来破解加密
    public void sign() {

    }

    // 代码右键运行，创建一个main
    public static void main(String[] args) {
        CheZhiYing che = new CheZhiYing();
        che.sign();
    }
}

```

### 4.2.3 执行签名

**JNI签名**



![image-20231117175841324](imgs/day24-课堂笔记.assets/image-20231117175841324.png)



```java
package com.nb.demo;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.jni.ProxyClassFactory;

import java.io.File;

public class CheZhiYing extends AbstractJni {
    public static AndroidEmulator emulator;  // 静态属性，以后对象和类都可以直接使用
    public static Memory memory;
    public static VM vm;
    public static Module module;

    // 构造方法,以后这个代码，基本是固定的，只需要改app位置即可，其他不用动
    public CheZhiYing() {
        // 1.创建设备（32位或64位模拟器）， 具体看so文件在哪个目录。 在armeabi-v7a就选择32位
        // 传进设备时，如果是32位，后面so文件就要用32位，同理需要用64位的
        // 这个名字可以随便写,一般写成app的包名    以后可能会动
        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.che168.autotradercloud").build();
        // 2.获取内存对象（可以操作内存）
        memory = emulator.getMemory();
        // 3.设置安卓sdk版本（只支持19、23）
        memory.setLibraryResolver(new AndroidResolver(23));

        // 4.创建虚拟机（运行安卓代码需要虚拟机，就想运行py代码需要python解释器一样）    以后会动
        vm = emulator.createDalvikVM(new File("apks/che/che3.32.1.apk"));
        vm.setJni(this); // 后期补环境会用，把要补的环境，写在当前这个类中，执行这个代码即可，但是必须继承AbstractJni
        //vm.setVerbose(true); //是否展示调用过程的细节

        // 5.加载so文件
        DalvikModule dm = vm.loadLibrary(new File("apks/che/libnative-lib.so"), false);   // 以后会动
        dm.callJNI_OnLoad(emulator); // jni开发动态注册，会执行JNI_OnLoad，如果是动态注册，需要执行一下这个，如果静态注册，这个不需要执行，车智赢案例是静态注册

        // 6.dm代表so文件，dm.getModule()得到module对象，基于module对象可以访问so中的成员。
        module = dm.getModule(); // 把so文件加载到内存后，后期可以获取基地址，偏移量等，该变量代指so文件

    }

    // sign 成员方法，用来破解加密
    public void sign() {
        // 1 找到java中 jni的类 native 类，必须用固定的写法写
        // 只要拿类，就要使用这个方法写，使用resolveClass把它包裹起来，中间用 /  区分
        DvmClass CheckSignUtil = vm.resolveClass("com/autohome/ahkit/jni/CheckSignUtil");

        // 2 找到类中的方法--》固定写法
        // 方法名(参数签名)返回值签名
        String method = "get3desKey(Landroid/content/Context;)Ljava/lang/String;";
        // 3 执行这个方法，传入参数
        //第一个参数是：设备对象
        // 第二个参数是：方法
        // 第三个参数往后的是：方法要传的参数,传参数的具体方式，下小结讲

        StringObject obj = CheckSignUtil.callStaticJniMethodObject(
                emulator,
                method,
                // 可能会出错--》如果so语言中使用了传入的这个context参数，而我们传的是空，就会报错，但是如果so中只是传了，没有使用，它就不会报错，先尝试传null试试
                vm.resolveClass("android/content/Context").newObject(null)
        );
        // 4 得到结果，打印出来
        String result = obj.getValue();
        System.out.println(result);

    }

    // 代码右键运行，创建一个main
    public static void main(String[] args) {
        CheZhiYing che = new CheZhiYing();
        che.sign();
    }
}

```



## 4.3 调用方法--》传参和返回值

```python
### 调用  jni中 Native方法时，传入的参数和返回值，不是java的 类型，而是需要使用unidbg提供的类型
StringObject obj = CheckSignUtil.callStaticJniMethodObject(emulator,method,
                                                           vm.resolveClass("android/content/Context").newObject(null)
        );




## 传参过程
Java类型                   包裹                                unidbg使用
字符串："justin"          StringObject("justin")                  使用
字节数组：{11,22}          ByteArray({11,22})                     使用
----------------------------------------------------------------------
布尔：True/False          True/False                              使用
数字：19                   19                                     使用
空：null                   null                                   使用
---------------------------自定义的类型------------------------------------------
自定义类型：Info         cls = vm.resolveClass("com/nb/utils/Info"); 使用
					   cls.newObject(对象)
    
刚刚的Context对象就是这样
cls=vm.resolveClass("android/content/Context")
cls.newObject('真正的对象')

# vm.resolveClass("android/content/Context").newObject(null)


### 返回值的过程
如果返回字符串 需要用 StringObject 类型接受---》拿到真正的字符串 需要 obj.getValue()
```





# 5 大姨妈案例

```python
# day21天讲的
# 破解sign时---》找到了 jni中的 Native方法encrypt_data---》当时觉得很难---》没有破--》用来Frida-rp和自己写app调用别人so，两种方案解决的

# 今天使用unidbg跑


### hook 得到的参数 
public static native String encrypt_data(long j2, String str, long j3);
#long j2 ：0
# String str： 拼接的明文   设备id+user/login+手机号+密码密文
#long j3：明文长度
j2=0
str=64e6176e45397c5989504e76f98ecf2e63b2679euser/login18953675221WA89qByLlDeaGjmVNzXm/w==
j3=85
```

![image-20231117181656873](imgs/day24-课堂笔记.assets/image-20231117181656873.png)



```java
package com.nb.demo;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.DalvikModule;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.memory.Memory;

import java.io.File;
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.jni.ProxyClassFactory;

import java.io.File;
public class DYM extends AbstractJni{
    public static AndroidEmulator emulator;  // 静态属性，以后对象和类都可以直接使用
    public static Memory memory;
    public static VM vm;
    public static Module module;
    public DYM() {
        // 1.创建设备（32位或64位模拟器）， 具体看so文件在哪个目录。 在armeabi-v7a就选择32位
        emulator = AndroidEmulatorBuilder.for64Bit().setProcessName("com.dym").build();
        // 2.获取内存对象（可以操作内存）
        memory = emulator.getMemory();
        // 3.设置安卓sdk版本（只支持19、23）
        memory.setLibraryResolver(new AndroidResolver(23));

        // 4.创建虚拟机（运行安卓代码需要虚拟机，就想运行py代码需要python解释器一样）    以后会动
        vm = emulator.createDalvikVM(new File("apks/dym/dymv8.6.0.apk"));
        vm.setJni(this); // 后期补环境会用，把要补的环境，写在当前这个类中，执行这个代码即可，但是必须继承AbstractJni
        //vm.setVerbose(true); //是否展示调用过程的细节

        // 5.加载so文件
        DalvikModule dm = vm.loadLibrary(new File("apks/dym/libCrypt.so"), false);   // 以后会动
        dm.callJNI_OnLoad(emulator); // jni开发动态注册，会执行JNI_OnLoad，如果是动态注册，需要执行一下这个，如果静态注册，这个不需要执行，车智赢案例是静态注册

        // 6.dm代表so文件，dm.getModule()得到module对象，基于module对象可以访问so中的成员。
        module = dm.getModule(); // 把so文件加载到内存后，后期可以获取基地址，偏移量等，该变量代指so文件

    }

    public void sign() {
        // 1 找到java中 jni的类 native 类，必须用固定的写法写
        DvmClass Crypt = vm.resolveClass("com/yoloho/libcore/util/Crypt");

        // 2 找到类中的方法--》固定写法
        String method = "encrypt_data(JLjava/lang/String;J)Ljava/lang/String;";
        // 3 执行这个方法，传入参数
        //第一个参数是：设备对象
        // 第二个参数是：方法
        // 第三个参数往后的是：方法要传的参数,传参数的具体方式，下小结讲

        StringObject obj = Crypt.callStaticJniMethodObject(
                emulator,
                method,
                0,
                new StringObject(vm,"bcae572b84d20c385d6d9d2d7d9e645da29da3c0user/login18953675221WA89qByLlDeaGjmVNzXm/w=="),
                85
        );
        // 4 得到结果，打印出来
        String result = obj.getValue();
        System.out.println(result);

    }

    public static void main(String[] args) {
        DYM dym = new DYM();
        dym.sign();
    }
}

```



# 6 得物案例

```python
# day 15 
```

![image-20231117183544499](imgs/day24-课堂笔记.assets/image-20231117183544499.png)

![image-20231117183526560](imgs/day24-课堂笔记.assets/image-20231117183526560.png)



```java
package com.nb.demo;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.DalvikModule;
import com.github.unidbg.linux.android.dvm.VM;
import com.github.unidbg.linux.android.dvm.array.ByteArray;
import com.github.unidbg.memory.Memory;

import java.io.File;

import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.Module;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.linux.android.dvm.jni.ProxyClassFactory;

import java.io.File;

public class Du extends AbstractJni{
    public static AndroidEmulator emulator;  // 静态属性，以后对象和类都可以直接使用
    public static Memory memory;
    public static VM vm;
    public static Module module;

    public Du() {
        // 1.创建设备（32位或64位模拟器）， 具体看so文件在哪个目录。 在armeabi-v7a就选择32位
        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.du").build();
        // 2.获取内存对象（可以操作内存）
        memory = emulator.getMemory();
        // 3.设置安卓sdk版本（只支持19、23）
        memory.setLibraryResolver(new AndroidResolver(23));

        // 4.创建虚拟机（运行安卓代码需要虚拟机，就想运行py代码需要python解释器一样）    以后会动
        vm = emulator.createDalvikVM(new File("apks/du/du-4.74.5.apk"));
        vm.setJni(this); // 后期补环境会用，把要补的环境，写在当前这个类中，执行这个代码即可，但是必须继承AbstractJni
        //vm.setVerbose(true); //是否展示调用过程的细节

        // 5.加载so文件
        DalvikModule dm = vm.loadLibrary(new File("apks/du/libJNIEncrypt.so"), false);   // 以后会动
        dm.callJNI_OnLoad(emulator); // jni开发动态注册，会执行JNI_OnLoad，如果是动态注册，需要执行一下这个，如果静态注册，这个不需要执行，车智赢案例是静态注册

        // 6.dm代表so文件，dm.getModule()得到module对象，基于module对象可以访问so中的成员。
        module = dm.getModule(); // 把so文件加载到内存后，后期可以获取基地址，偏移量等，该变量代指so文件
    }

    public void sign() {
        // 1 找到类
        DvmClass AESEncrypt = vm.resolveClass("com/duapp/aesjni/AESEncrypt");
        // 2 找到方法
        String method = "getByteValues()Ljava/lang/String;";
        // 3 调用方法
        StringObject byteValues = AESEncrypt.callStaticJniMethodObject(
                emulator,
                method
        );
        // 4 拿到真正的字符串
        String byteValuesString = byteValues.getValue();

        // 5 执行 把0变成 1，把1变成0
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < byteValuesString.length(); i++) {
            if (byteValuesString.charAt(i) == '0') {
                sb.append('1');
            } else {
                sb.append('0');
            }
        }

        String sbString = sb.toString();
        System.out.println(sbString);

        //6 找到方法
        String methodEncodeBytes = "encodeByte([BLjava/lang/String;)Ljava/lang/String;";

        String body = "loginTokenplatformandroidrouterVersion569timestamp1690882175032uuidaa39fda5dfb88d79v4.74.5";
        // 7 执行方法
        StringObject data = AESEncrypt.callStaticJniMethodObject(
                emulator,
                methodEncodeBytes,
                new ByteArray(vm, body.getBytes()),
                new StringObject(vm, sbString)
        );
        // 8 打印结果
        System.out.println(data.getValue());

    }

    public static void main(String[] args) {
        Du du = new Du();
        du.sign();
        //knGGXR0bR7LQn4eRCvJsdYgYdJOA87lB9pdSj5LyZPp5O1D7em+oNjsR/hxGs9U+qpTFl9wV3uwai4JQsrMnVtb6Kw/bXTHjZ7jViuThKQT+5aY2HvkoCjEoBzHTyfw1
    }
}

```



# 7 海南航空案例

```python
# 破解    hnairSign  加密---》unidgb跑出来

```

## 7.1 抓包

![image-20231117222013342](imgs/day24-课堂笔记.assets/image-20231117222013342.png)



## 7.2 反编译搜索

```python
# 1 搜索 ：hnairSign
# 2 搜到代码
String signRequest = signRequest(aVar);
u.a i10 = request.j().i();
i10.b("hnairSign", signRequest);

# 3 找 signRequest(aVar)

private final String signRequest(v.a aVar) {
    String str;
    ApiInterceptor.Companion companion = ApiInterceptor.Companion;
    companion.getRequestTag(aVar);
    y request = aVar.request();
    String headersForSign = headersForSign(request.f());
    String queryForSign = queryForSign(request.j());
    String requestBodyForSign = requestBodyForSign(request);
    if (companion.needAuth(request)) {
        str = Companion.extraSecret(request);
        if (str == null && (str = this.userManager.get().getSecret()) == null) {
            str = this.salt;
        }
    } else {
        str = this.salt;
    }
    String a10 = AppUtil.a(this.context);
    if (a10 == null) {
        a10 = "";
    }
    # 重点
    return (String) i.p(HNASignature.getHNASignature(headersForSign, queryForSign, requestBodyForSign, str, a10), new String[]{">>"}).get(0);
}
# 4  HNASignature.getHNASignature() 看它
public class HNASignature {
    public static native String getHNASignature(String str, String str2, String str3, String str4, String str5);
}

# 5 是个jni Native方法---》找不到它的so文件

# 接下来要干两个事：
	1 确定so文件是那个
    2 确定传入的参数时什么  String str, String str2, String str3, String str4, String str5
```

## 7.3 确定传入的参数--hook

```js
Java.perform(function () {
    var HNASignature = Java.use("com.rytong.hnair.HNASignature");
    HNASignature.getHNASignature.implementation = function (str,str2,str3,str4,str5) {
        console.log("---------------------")
        console.log("参数",str);
        console.log("参数",str2);
        console.log("参数",str3);
        console.log("参数",str4);
        console.log("参数",str5);
        var res = this.getHNASignature(str,str2,str3,str4,str5);
        console.log("返回值=",res);
        return res;
    }
});


//frida -U -f com.rytong.hnair -l hook-js.js
```

```js
// 抓包抓的值：A1098135EB40EA8D5A43159A6FEFE8EA58CECD23


/* hook到的结果
参数 {}
参数 {}
参数 {"abuild":"64249","akey":"184C5F04D8BE43DCBD2EE3ABC928F616","aname":"com.rytong.hnair","atarget":"standard","aver":"9.0.0","
caller":"AD_H5","did":"2c1c0689406f11f3","dname":"Google_Pixel 2 XL","gtcid":"0325877839a15262def29defcb8ac69a","hver":"9.0.0.354
17.7ac793f2e.standard","mchannel":"huawei","schannel":"AD","slang":"zh-CN","sname":"google\/taimen\/taimen:11\/RP1A.201005.004.A1
\/6934943:user\/release-keys","stime":"1700231549934","sver":"11","system":"AD","szone":"+0800","riskToken":"65577855Tzrn6sLZ3tepwoctkhO765TUH5AcxRH3"}
参数 21047C596EAD45209346AE29F0350491
参数 F6B15ABD66F91951036C955CB25B069F

返回值= A1098135EB40EA8D5A43159A6FEFE8EA58CECD23>>64249184C5F04D8BE43DCBD2EE3ABC928F616com.rytong.hnairstandard9.0.0AD_H52c1c0689
406f11f3Google_Pixel 2 XL0325877839a15262def29defcb8ac69a9.0.0.35417.7ac793f2e.standardhuawei65577855Tzrn6sLZ3tepwoctkhO765TUH5Ac
xRH3ADzh-CNgoogle/taimen/taimen:11/RP1A.201005.004.A1/6934943:user/release-keys170023154993411AD+0800>>F6B15ABD66F91951036C955CB25B069F




 */
```

## 7.4 寻找so文件

```python
getHNASignature 要么是动态注册，要么是静态注册
B站案例---》hook脚本--》hook动态注册打印出这个动态注册方法的so文件
---基地址---
```

![image-20231117192343346](imgs/day24-课堂笔记.assets/image-20231117192343346.png)

### 7.4.1 查看是否动态注册（B站案例）这个案例不是用动态注册

```js
var symbols = Module.enumerateSymbolsSync("libart.so");
var addrRegisterNatives = null;
for (var i = 0; i < symbols.length; i++) {
    var symbol = symbols[i];
    if (symbol.name.indexOf("art") >= 0 &&
        symbol.name.indexOf("JNI") >= 0 &&
        symbol.name.indexOf("RegisterNatives") >= 0 &&
        symbol.name.indexOf("CheckJNI") < 0) {
        addrRegisterNatives = symbol.address;
        console.log("RegisterNatives is at ", symbol.address, symbol.name);
    }
}
console.log("addrRegisterNatives=", addrRegisterNatives);

if (addrRegisterNatives != null) {
    Interceptor.attach(addrRegisterNatives, {
        onEnter: function (args) {
            var env = args[0];
            var java_class = args[1];
            var class_name = Java.vm.tryGetEnv().getClassName(java_class);
            // 只有类名为com.rytong.hnair.HNASignature，才打印输出

            var taget_class = "com.rytong.hnair.HNASignature";

            if (class_name === taget_class) {
                console.log("\n[RegisterNatives] method_count:", args[3]);
                var methods_ptr = ptr(args[2]);
                var method_count = parseInt(args[3]);

                for (var i = 0; i < method_count; i++) {
                    // Java中函数名字的
                    var name_ptr = Memory.readPointer(methods_ptr.add(i * Process.pointerSize * 3));
                    // 参数和返回值类型
                    var sig_ptr = Memory.readPointer(methods_ptr.add(i * Process.pointerSize * 3 + Process.pointerSize));
                    // C中的函数指针
                    var fnPtr_ptr = Memory.readPointer(methods_ptr.add(i * Process.pointerSize * 3 + Process.pointerSize * 2));

                    var name = Memory.readCString(name_ptr); // 读取java中函数名
                    var sig = Memory.readCString(sig_ptr); // 参数和返回值类型
                    var find_module = Process.findModuleByAddress(fnPtr_ptr); // 根据C中函数指针获取模块

                    var offset = ptr(fnPtr_ptr).sub(find_module.base) // fnPtr_ptr - 模块基地址
                    // console.log("[RegisterNatives] java_class:", class_name);
                    console.log("name:", name, "sig:", sig, "module_name:", find_module.name, "offset:", offset);
                    //console.log("name:", name, "module_name:", find_module.name, "offset:", offset);

                }
            }
        }
    });
}

// frida -U -f  com.rytong.hnair  -l hook22.js
```

### 7.4.2 静态注册so文件hook脚本

```js
Java.perform(function () {
    var dlsymadd = Module.findExportByName("libdl.so", 'dlsym');
    Interceptor.attach(dlsymadd, {
        onEnter: function (args) {
            this.info = args[1];

        }, onLeave: function (retval) {
            //那个so文件 module.name
            var module = Process.findModuleByAddress(retval);
            if (module == null) {
                return retval;
            }
            // native方法
            var funcName = this.info.readCString();
            if (funcName.indexOf("getHNASignature") !== -1) {
                console.log(module.name);
                console.log('\t', funcName);
            }
            return retval;
        }
    })
});

// Application(identifier="com.rytong.hnair", name="海南航空", pid=14958, parameters={})
// frida -U -f  com.rytong.hnair  -l static_find_so.js
```

![image-20231117223504030](imgs/day24-课堂笔记.assets/image-20231117223504030.png)

### 7.4.3 unidbg

```python

package com.nb.demo;
import com.github.unidbg.AndroidEmulator;
import com.github.unidbg.Emulator;
import com.github.unidbg.Module;
import com.github.unidbg.Symbol;
import com.github.unidbg.arm.context.RegisterContext;
import com.github.unidbg.hook.hookzz.*;
import com.github.unidbg.linux.android.AndroidEmulatorBuilder;
import com.github.unidbg.linux.android.AndroidResolver;
import com.github.unidbg.linux.android.dvm.*;
import com.github.unidbg.memory.Memory;
import com.github.unidbg.pointer.UnidbgPointer;
import com.github.unidbg.utils.Inspector;

import java.io.File;

public class HaiNan extends AbstractJni{
    public static AndroidEmulator emulator;
    public static Memory memory;
    public static VM vm;
    public static DalvikModule dm;
    public static Module module;
    public HaiNan() {
        // 1.创建设备（32位或64位模拟器）， 具体看so文件在哪个目录。 在armeabi-v7a就选择32位
        emulator = AndroidEmulatorBuilder.for32Bit().setProcessName("com.hainan").build();

        // 2.获取内存对象（可以操作内存）
        memory = emulator.getMemory();

        // 3.设置安卓sdk版本（只支持19、23）
        memory.setLibraryResolver(new AndroidResolver(23));

        // 4.创建虚拟机（运行安卓代码需要虚拟机，就想运行py代码需要python解释器一样）
        vm = emulator.createDalvikVM(new File("apks/hainan/v9.0.0.apk"));
        vm.setJni(this);
        // vm.setVerbose(true); //是否展示调用过程的细节

        // 5.加载so文件
        DalvikModule dm = vm.loadLibrary(new File("apks/hainan/libsignature.so"), false);
        dm.callJNI_OnLoad(emulator);

        module = dm.getModule();
    }

    public void sign() {
        // 找到java中native所在的类，并加载
        DvmClass HNASignature = vm.resolveClass("com/rytong/hnair/HNASignature");

        // 方法的符号表示
        String method = "getHNASignature(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;";

        // 执行类中的静态成员
        StringObject obj = HNASignature.callStaticJniMethodObject(
                emulator,
                method,
                new StringObject(vm, "{}"),
                new StringObject(vm, "{}"),
                new StringObject(vm, "{\"abuild\":\"64249\",\"akey\":\"184C5F04D8BE43DCBD2EE3ABC928F616\",\"aname\":\"com.rytong.hnair\",\"atarget\":\"standard\",\"aver\":\"9.0.0\",\"caller\":\"AD_H5\",\"did\":\"2c1c0689406f11f3\",\"dname\":\"Google_Pixel 2 XL\",\"gtcid\":\"eec0ce379c80f2f09c02c9a2a3f084ef\",\"hver\":\"9.0.0.35417.7ac793f2e.standard\",\"mchannel\":\"huawei\",\"schannel\":\"AD\",\"slang\":\"zh-CN\",\"sname\":\"google\\/taimen\\/taimen:11\\/RP1A.201005.004.A1\\/6934943:user\\/release-keys\",\"stime\":\"1700232607250\",\"sver\":\"11\",\"system\":\"AD\",\"szone\":\"+0800\",\"riskToken\":\"65577c77o2zQ1PCq7EK5e3lS0WS89uYCD0Akz1g3\"}"),
                new StringObject(vm, "21047C596EAD45209346AE29F0350491"),
                new StringObject(vm, "F6B15ABD66F91951036C955CB25B069F")
        );

        String keyString = obj.getValue();
        System.out.println(keyString);
    }

    public static void main(String[] args) {
        HaiNan hn = new HaiNan();
        hn.sign();
//        String s="{\"abuild\":\"64249\",\"akey\":\"184C5F04D8BE43DCBD2EE3ABC928F616\",\"aname\":\"com.rytong.hnair\",\"atarget\":\"standard\",\"aver\":\"9.0.0\",\"\ncaller\":\"AD_H5\",\"did\":\"2c1c0689406f11f3\",\"dname\":\"Google_Pixel 2 XL\",\"gtcid\":\"0325877839a15262def29defcb8ac69a\",\"hver\":\"9.0.0.354\n17.7ac793f2e.standard\",\"mchannel\":\"huawei\",\"schannel\":\"AD\",\"slang\":\"zh-CN\",\"sname\":\"google\\/taimen\\/taimen:11\\/RP1A.201005.004.A1\n\\/6934943:user\\/release-keys\",\"stime\":\"1700231549934\",\"sver\":\"11\",\"system\":\"AD\",\"szone\":\"+0800\",\"riskToken\":\"65577855Tzrn6sLZ3tepwoctkhO765TUH5AcxRH3\"}";
    }
}


```






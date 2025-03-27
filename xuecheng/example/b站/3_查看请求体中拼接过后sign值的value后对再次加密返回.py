import frida
import sys

#判断是AES加密 找到密钥与key与IV

# attach 程序已经处于运行状态才能进行监听hook
# 模拟器启动frida-server
# 运行程序开始监听，模拟器应用操作模拟，触发监听
# 连接手机设备
rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")  # app名字
# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：javax.crypto.spec.SecretKeySpec下的
    ///hook key值
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

# -----下面固定---以后不会动
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()

#确认KEY与IV
# 请求来了
# key= fd6b639dbcff0c2a1b03b389ec763c4b
# name= AES
# iv= 77b07a672d57d64c

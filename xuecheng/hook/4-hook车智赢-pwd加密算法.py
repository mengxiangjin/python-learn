import frida
import sys

#attach 程序已经处于运行状态才能进行监听hook
#模拟器启动frida-server
#运行程序开始监听，模拟器应用操作模拟，触发监听
# 连接手机设备
rdev = frida.get_remote_device()

#deviceId 437665
#udid中 des加密的key值 appapiche168comappapiche168comap  iv:appapich

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
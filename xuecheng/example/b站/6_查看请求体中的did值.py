import frida
import sys

#attach 程序已经处于运行状态才能进行监听hook
#模拟器启动frida-server
#运行程序开始监听，模拟器应用操作模拟，触发监听
# 连接手机设备
rdev = frida.get_remote_device()

session = rdev.attach("哔哩哔哩")  # app名字

# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：c2.f.b0.c.a.e下的
    var e = Java.use("com.bilibili.lib.biliid.utils.f.a");

    //替换类中的方法
    e.c.implementation = function(j2){
        console.log("传入的参数：",j2);
        var res = this.f(j2); //调用原来的函数
        console.log("返回值",res);
        return res; 
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

# 传入的参数： BiliApplication(tv.danmaku.bili)@e81f35
# 返回值 |||


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

# 打印当前函数调用栈信息
scr = """
Java.perform(function () {
    var a = Java.use('com.bilibili.commons.m.a');
    a.i.implementation = function(str){
        console.log("入参：",str);
        var res = this.i(str);
        console.log("返回值：",res);
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


# 第二个 同session比对后  真正入参为：1743387417586178117
# 入参： 1743387417517633209
# 返回值： a39fde17b26967c815ec5ff788bd4928c266d4fb
# 入参： 1743387417586178117
# 返回值： 2eadaeb50f824724feffb5fc263df584d1e7f8c2

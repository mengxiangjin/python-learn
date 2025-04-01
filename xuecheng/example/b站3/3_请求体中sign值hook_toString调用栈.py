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
    var signedQuery = Java.use('com.bilibili.nativelibrary.SignedQuery');
    signedQuery.toString.implementation = function(){
        console.log("执行了");
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        var res = this.toString();
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

# 执行了
# java.lang.Throwable
# 	at com.bilibili.nativelibrary.SignedQuery.toString(Native Method)
# 	at com.bilibili.okretro.f.a.c(BL:16)
# 	at com.bilibili.okretro.f.a.a(BL:6)
# 	at com.bilibili.okretro.d.a.execute(BL:24)
# 	at com.bilibili.okretro.d.a$a.run(BL:2)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:923)



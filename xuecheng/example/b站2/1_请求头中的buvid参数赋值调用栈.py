import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["tv.danmaku.bili"])
session = rdev.attach(pid)

# 打印当前函数调用栈信息
scr = """
Java.perform(function () {
    var c = Java.use('com.bilibili.api.c');
    c.b.implementation = function(str){
        console.log("执行了",str);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        this.b(str);
        
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


# '''
# java.lang.Throwable
# 	at com.bilibili.api.c.b(Native Method)   # 找谁调用了它
# 	at c2.f.b0.c.a.d.e(BL:1)                 # c2.f.b0.c.a.d.e调用了它b
# 	at c2.f.b0.c.a.d.a(BL:11)               #c2.f.b0.c.a.d.a 调用了e
# 	at tv.danmaku.bili.utils.x.a(BL:14)
# 	at tv.danmaku.bili.proc.y.f(BL:1)
# 	at tv.danmaku.bili.proc.c.run(Unknown Source:2)
# 	at android.os.Handler.handleCallback(Handler.java:938)
# 	at android.os.Handler.dispatchMessage(Handler.java:99)
# 	at android.os.Looper.loop(Looper.java:223)
# 	at android.os.HandlerThread.run(HandlerThread.java:67)
#
# '''
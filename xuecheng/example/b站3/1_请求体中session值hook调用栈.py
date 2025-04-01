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
    var h = Java.use('tv.danmaku.biliplayerimpl.report.heartbeat.h');
    h.t2.implementation = function(str){
        console.log("执行了",str);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        this.t2(str);
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

# 执行了 066f2d4693fa607860b0944a9a3c2fc80aa858cd
# java.lang.Throwable
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.h.t2(Native Method)
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.h$a.b(BL:5)
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.d.L7(BL:2)
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.d.u7(BL:3)
# 	at tv.danmaku.biliplayerimpl.core.PlayerCoreServiceV2$l.onPrepared(BL:2)
# 	at t3.a.i.b.i$j.onPrepared(BL:6)
# 	at tv.danmaku.ijk.media.player.AbstractMediaPlayer.notifyOnPrepared(BL:2)
# 	at tv.danmaku.ijk.media.player.IjkMediaPlayer$EventHandler.handleMessage(BL:107)
# 	at android.os.Handler.dispatchMessage(Handler.java:106)
# 	at android.os.Looper.loop(Looper.java:223)
# 	at android.app.ActivityThread.main(ActivityThread.java:7656)
# 	at java.lang.reflect.Method.invoke(Native Method)
# 	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:592)
# 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:947)

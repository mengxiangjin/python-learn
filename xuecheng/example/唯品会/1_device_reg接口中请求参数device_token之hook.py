import frida
import sys

#attach 程序已经处于运行状态才能进行监听hook
#模拟器启动frida-server
#运行程序开始监听，模拟器应用操作模拟，触发监听
# 连接手机设备
rdev = frida.get_remote_device()
session = rdev.attach("唯品会")  # app名字

# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码

scr = """
Java.perform(function () {
    var c = Java.use('hk.c');
    c.u0.implementation = function(str){
        console.log("入参：",str);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        var res = this.m0(str);
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

# 入参： 1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b
# 入参： 1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b
# java.lang.Throwable
# 	at hk.c.u0(Native Method)
# 	at sd.a.f(SourceFile:3)
# 	at com.achievo.vipshop.commons.push.NotificationManage.getPushRegisterUrl(SourceFile:1)
# 	at com.achievo.vipshop.commons.push.NotificationManage$d.run(SourceFile:1)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:923)
#
# java.lang.Throwable
# 	at hk.c.u0(Native Method)
# 	at sd.a.f(SourceFile:3)
# 	at com.achievo.vipshop.commons.push.NotificationManage.getMid(SourceFile:1)
# 	at com.achievo.vipshop.commons.push.MqttService.q(SourceFile:1)
# 	at com.achievo.vipshop.commons.push.MqttService.k(SourceFile:3)
# 	at com.achievo.vipshop.commons.push.NotificationManage.startPushService(SourceFile:15)
# 	at com.achievo.vipshop.proxy.PushProxyImp.startPush(SourceFile:4)
# 	at com.achievo.vipshop.commons.push.NotificationManage.startPushService(SourceFile:3)
# 	at com.achievo.vipshop.common.b.u(SourceFile:2)
# 	at com.achievo.vipshop.activity.LodingActivity$a.a(SourceFile:1)
# 	at com.achievo.vipshop.activity.LodingActivity$a.call(SourceFile:1)
# 	at c.g$i.run(SourceFile:3)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:923)
#
# 入参： 1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b
# java.lang.Throwable
# 	at hk.c.u0(Native Method)
# 	at com.achievo.vipshop.common.b.p(SourceFile:11)
# 	at com.achievo.vipshop.activity.LodingActivity$a.a(SourceFile:5)
# 	at com.achievo.vipshop.activity.LodingActivity$a.call(SourceFile:1)
# 	at c.g$i.run(SourceFile:3)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:923)





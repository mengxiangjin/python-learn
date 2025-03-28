import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["tv.danmaku.bili"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var a = Java.use("com.bilibili.api.a");

    a.o.implementation = function(arg0){   
       console.log("obj=",arg0);  // 打印参数
       console.log("obj=",JSON.stringify(arg0)); // 能打印出参数的类型
       this.o(arg0);
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
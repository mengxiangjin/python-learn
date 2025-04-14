import frida
import sys

# 连接手机设备
rdev = frida.get_remote_device()

session = rdev.attach("拼多多")

scr = """
Java.perform(function () {

    // 包.类
    var eu = Java.use("com.xunmeng.pinduoduo.secure.EU");

    eu.gad.implementation = function(){
        var res = this.gad();
        console.log("返回值",res); 
        return res;
    }

});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()

# 返回值 5da722f0ab2d638c


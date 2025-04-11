import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.yoloho.dayima"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var miscUtil = Java.use('com.yoloho.libcore.util.MiscUtil');
    miscUtil.isSimulator.implementation = function(ctx) {
        console.log("执行了isSimulator");
        return false;
    }
    miscUtil.isRooted.implementation = function() {
        console.log("执行了isRooted");
        return false;
    }
    
    var crypt = Java.use('com.yoloho.libcore.util.Crypt');
    crypt.encrypt_data.implementation = function(j2,str,j3) {
        console.log("入参1：",j2);
        console.log("入参2：",str);
        console.log("入参3：",j3);
        var res = this.encrypt_data(j2,str,j3)
        console.log("返回值：",res);
        return res;
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

# 执行了isSimulator
# 执行了isRooted
# 入参1： 0
# 入参2： 496245b6e3d137128935a312d866674fcfde3927user/login15655549539kerIUjxqnmtG1MkN6p6BWg==
# 入参3： 85
# 返回值： 8f13086539d0d1320950fa9d2c079f62
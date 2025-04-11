import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["cmt.chinaway.com.lite"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var p0 = Java.use('cmt.chinaway.com.lite.q.p0');
    p0.a.implementation = function(str1,str2,str3,str4){
        console.log("入参：",str1);
        console.log("入参：",str2);
        console.log("入参：",str3);
        console.log("入参：",str4);
        var res = this.a(str1,str2,str3,str4);
        console.log("返回值参：",res);
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


# 密钥：固定的 1KMrg0dfufc0wpnXEJacEQX1YEUYA0Ja

# 入参： 1KMrg0dfufc0wpnXEJacEQX1YEUYA0Ja
# 入参： POST
# 入参： 1743995753786
# 入参： inside.php
# 返回值参： rIE1G1y68UfhxaZvFe3SmnzpeEA%3D

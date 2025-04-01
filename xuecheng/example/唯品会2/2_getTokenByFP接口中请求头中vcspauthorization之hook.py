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
    var info = Java.use('com.vip.vcsp.KeyInfo');
    var treeMap = Java.use('java.util.TreeMap')
    info.gsNav.implementation = function(context,map,str,boolean){
        console.log("入参：",str);
        console.log("入参：",Java.cast(map,treeMap).toString());
        console.log("入参：",boolean);
        var res = this.gsNav(context,map,str,boolean);
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


# 入参： null
# 入参： {vcspKey=4d9e524ad536c03ff203787cf0dfcd29}
# 入参： true
# 返回值参： 05a68135d2bfd322e3a22f95bbc25a24c777f387


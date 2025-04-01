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
    info.getNavInfo.implementation = function(context,str){
        console.log("入参：",str);
        var res = this.getNavInfo(context,str);
        console.log("返回值参：",res);
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

# vcsp_key：固定值
# 入参： app_name
# 返回值参： shop_android
# 入参： vcsp_key
# 返回值参： 4d9e524ad536c03ff203787cf0dfcd29
# 入参： api_key
# 返回值参： 23e7f28019e8407b98b84cd05b5aef2c
# 入参： skey
# 返回值参： 6692c461c3810ab150c9a980d0c275ec
# 入参： skey
# 返回值参： 6692c461c3810ab150c9a980d0c275ec



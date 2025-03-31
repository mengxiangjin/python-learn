# 现象：hook就闪退（反调试） 删除 `libmsaoaidsec.so`
# 这个请求是注册设备---》删缓存---》卸载重载app

import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.achievo.vipshop"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");

    KeyInfo.getNavInfo.implementation = function (ctx, str) {
        console.log("-----------------");
        console.log("参数==>", str);
        var res = this.getNavInfo(ctx, str);
        console.log("返回的值==>", res);
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

# -----------------
# 参数==> app_name
# 返回的值==> shop_android
# -----------------
# 参数==> vcsp_key
# 返回的值==> 4d9e524ad536c03ff203787cf0dfcd29
# -----------------
# 参数==> api_key
# 返回的值==> 23e7f28019e8407b98b84cd05b5aef2c
# -----------------
# 参数==> skey
# 返回的值==> 6692c461c3810ab150c9a980d0c275ec
# -----------------
# 参数==> skey
# -----------------
# 参数==> skey
# 返回的值==> 6692c461c3810ab150c9a980d0c275ec
# 返回的值==> 6692c461c3810ab150c9a980d0c275ec

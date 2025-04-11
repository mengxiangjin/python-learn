# 清除一下数据
import frida
import sys

rdev = frida.get_remote_device()

session = rdev.attach("唯品会")

scr = """
Java.perform(function () {
    var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");
    var TreeMap = Java.use('java.util.TreeMap');


    KeyInfo.gsNav.implementation = function (ctx, map,str,z10) {
        console.log("-----------------gsNav-----------------");
        console.log("参数==>", Java.cast(map,TreeMap).toString());
        console.log("参数==>", str);
        console.log("参数==>", z10);
        var res = this.gsNav(ctx, map,str,z10);
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
sys.stdin.read()

# -----------------gsNav-----------------
# 参数==> {app_name=achievo_ad, app_version=7.83.3, channel=oziq7dxw:::, device=Pixel 2 XL, device_token=1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b, manufacturer=Google, os_version=30, regPlat=0, regid=null, rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1), skey=6692c461c3810ab150c9a980d0c275ec, status=1, vipruid=, warehouse=null}
# 参数==> null
# 参数==> false
# 返回的值==> 4723dd6cb5ece0183ad7ec8cd45d251db4b72ec2

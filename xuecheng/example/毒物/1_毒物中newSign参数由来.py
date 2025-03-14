import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")   # 老版本叫： 得物(毒)    新版本：  得物

scr = """
Java.perform(function () {
    var RequestUtils = Java.use("com.shizhuang.duapp.common.utils.RequestUtils");
    RequestUtils.c.implementation = function(map,j){
        console.log("----------------------------------------");
        console.log('1.参数字典为：',map); // 此处直接打印map，发现打印的是对象，我们需要转换一下
        console.log('2.参数字典类型为：',JSON.stringify(map));  // 查看一下类型 ：java.util.HashMap
        // 以下是固定格式
        var Map = Java.use('java.util.HashMap');
        var obj = Java.cast(map, Map);
        console.log('3.参数字典转成字符串类型为：',obj.toString());
        var res = this.c(map,j);
        console.log("4.newSign结果：", res);
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
# 1.参数字典为： [object Object]
# 2.参数字典类型为： "<instance: java.util.Map, $className: java.util.HashMap>"
# 3.参数字典转成字符串类型为： {abValue=1, deliveryProjectId=0, abRectagFengge=0, abType=social_brand_strategy_v454, limit=20, lastId=, abRecReason=0, abVideoCover=2}
# 4.newSign结果： 640cd8e586fd32070f181cc3982c65eb


# '''
# 1.参数字典为： [object Object]
# 2.参数字典类型为： "<instance: java.util.Map, $className: java.util.HashMap>"
# 3.参数字典转成字符串类型为： {abValue=1,
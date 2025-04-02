import frida
import sys

# spawn程序重启即开始监听hook
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
    
    var periodAPIV2 = Java.use("com.yoloho.controller.api.PeriodAPIV2");
    var flag = false;

    //替换类中的方法
    periodAPIV2.setDeviceCode.implementation = function(){
        console.log("进入了setDeviceCode--------------------");
        flag = true;
        this.setDeviceCode(); //调用原来的函数
    }
    
    periodAPIV2.getDeviceCode.implementation = function(){
        console.log("进入了getDeviceCode--------------------");
        var res = this.getDeviceCode(); //调用原来的函数
        console.log("device----------",res)
        return res
    }

     var MessageDigest = Java.use("java.security.MessageDigest");
     var ByteString = Java.use("com.android.okhttp.okio.ByteString");
     MessageDigest.update.overload("[B").implementation = function (data) {
        if (flag) {
            console.log(ByteString.of(data).utf8(), '' );
            console.log("---------------");
        }
        return this.update(data);
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

#分析结果后分隔
# null cb362844b93983e9 taimengooglearm64-v8ataimenRP1A.201005.004.A1abfarm-01392RP1A.201005.004.A1GooglePixel 2 XLtaimenrelease-keysuserandroid-build D2:74:CF:79:9D:DC 02:00:00:00:00:00


# nullcb362844b93983e9taimengooglearm64-v8ataimenRP1A.201005.004.A1abfarm-01392RP1A.201005.004.A1GooglePixel 2 XLtaimenrelease-keysuserandroid-buildD2:74:CF:79:9D:DC02:00:00:00:00:00
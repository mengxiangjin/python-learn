import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.soom.live999"])
session = rdev.attach(pid)


# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：com.autohome.ahkit.utils下的
    var OkHttpBuilder = Java.use("com.miss.common.http.OkHttpBuilder");

    //替换类中的方法
    OkHttpBuilder.req1.implementation = function(url,tag,cls){
        console.log("url：",url);
        console.log("tag：",tag);
        if(url.includes('User.getFollowsList2')) {
             console.log("命中：");
        }
        return this.req1(url,tag,cls);  
    }
    
    var req = Java.use("com.lzy.okgo.request.base.Request");
    
    // 假设有两个重载版本，首先明确指定重载签名
    req.params.overload("java.lang.String", "java.lang.String", "[Z").implementation = function(key, value, b) {
        console.log("key：", key);
        console.log("value：", value);
        return this.params(key, value, b);  // 调用原始方法
    };
    
    req.params.overload("java.lang.String", "int", "[Z").implementation = function(key, value, b) {
        console.log("key：", key);
        console.log("value：", value);
        return this.params(key, value, b);  // 调用原始方法
    };
    
    
    var Kiwi = Java.use("com.kiwi.sdk.Kiwi");
    
    //替换类中的方法
    Kiwi.ServerToLocal.implementation = function(name,ip,port){
        console.log("name：", name);
        console.log("ip：", ip);
        console.log("port：", port);
        var res = this.ServerToLocal(name,ip,port)
        console.log("ip：", ip);
        console.log("port：", port);
        console.log("res：", res);
        return res;
    }
    
     var SpUtil = Java.use("com.miss.common.utils.SpUtil");
    
    //替换类中的方法
    SpUtil.getStringValue.implementation = function(key){
        console.log("getStringValue key：", key);
        var res = this.getStringValue(key)
        console.log("getStringValue value：", res);
        if(key === 'host') {
            console.log("getStringValue 进来了：");
            res = '';
        }
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

# name： product_api
# ip：
# port：
# ip： 127.0.0.1
# port： 54545
# res： 0

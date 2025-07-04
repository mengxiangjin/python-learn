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
    var JSON = Java.use('com.alibaba.fastjson.JSON');
    var JSONObject = Java.use('com.alibaba.fastjson.JSONObject');
       
    JSON.toJavaObject.overload('com.alibaba.fastjson.JSON','java.lang.Class').implementation = function(json,clz) {
        console.log('toJavaObject ',json)
        console.log('toJavaObject ',clz)
        // 将 JSON 字符串转换为 JSONObject
        
         // 确保json是字符串类型
        var jsonString = json.toString(); // 转换为字符串类型
        var jsonObject = JSON.parseObject(jsonString); 
        jsonObject.put('paidprogram_switch','1');
        
        var newjson = JSON.parseObject(jsonObject.toString())
        console.log('Modified JSON: ', newjson);
        return this.toJavaObject(newjson,clz)
    }
    
    
     // 获取目标类的引用（即 com.miss.im.ChatUtil）
    var HttpCallback = Java.use('com.miss.im.ChatUtil$2');
    

    // Hook checkAllowed 方法（假设该方法是静态方法）
    HttpCallback.onSuccess.implementation = function (code,msg,infos) {
        console.log('onSuccess 被调用了',code);
        console.log('onSuccess 被调用了',msg);
        console.log('onSuccess 被调用了',infos);
        this.onSuccess(code,msg,infos)
    };
});
"""



script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
rdev.resume(pid)
sys.stdin.read()

# var
# SimpleX509TrustManager = Java.use("com.mob.tools.network.NetworkHelper$SimpleX509TrustManager");
# // 拦截
# getConfig
# 方法
# SimpleX509TrustManager.checkServerTrusted.implementation = function(q, p)
# {
#     console.log("SimpleX509TrustManager");
# this.checkServerTrusted(q, p);
# };
#
# SimpleX509TrustManager.$init.implementation = function(keystore)
# {
#     console.log("SimpleX509TrustManager$init");
# this.$init(keystore)
# }
#
# var
# SSLTrustManager = Java.use("cn.jiguang.net.SSLTrustManager");
#
# // 拦截
# getConfig
# 方法
# SSLTrustManager.$init.implementation = function(str)
# {
#     console.log("SSLTrustManager", str);
# this.$init(str)
# };



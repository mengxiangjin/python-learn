import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.soom.live999"])
session = rdev.attach(pid)

# var
# SpUtil = Java.use('com.miss.common.utils.SpUtil');
# SpUtil.getMultiStringValue.implementation = function(keys)
# {
#     console.log('getMultiStringValue 被调用了', keys);
# var
# res = this.getMultiStringValue(keys);
# console.log('res 返回值', res);
# return res;
# };
#
# var
# LauncherActivity = Java.use('com.soom.live999.activity.LauncherActivity$3');
# LauncherActivity.callback.overload('com.miss.common.bean.ConfigBean').implementation = function(bean)
# {
# console.log('callback 被调用了', bean);
# console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
# this.callback(bean);
# };


# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {

    var HttpCallback = Java.use('com.miss.common.http.HttpCallback');
    HttpCallback.onError.overload('com.lzy.okgo.model.Response').implementation = function (response) {
        console.log('onError 被调用了',response.getException());
        this.onError(response);
    };
    
     var Response = Java.use('com.lzy.okgo.model.Response');
    Response.error.implementation = function (a,b,c,d) {
        console.log('error 被调用了',a);
        console.log('error 被调用了',b);
        console.log('error 被调用了',c);
        console.log('error 被调用了',d);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        return this.error(a,b,c,d);
    };
    
    var Builder = Java.use('okhttp3.OkHttpClient$Builder');
    Builder.proxy.implementation = function (proxy) {
        console.log('proxy 被调用了',proxy);
        return this.proxy(proxy);
    };
    
    var OkHttpClient = Java.use('okhttp3.OkHttpClient');
    Builder.build.implementation = function () {
        console.log('build 被调用了');
        var res = this.build();
        var res_1 = Java.cast(res, OkHttpClient);
        console.log('build 返回值',res_1);
        console.log('build 返回值',res_1.interceptors().get(0));
         return res
    };
    
    var a1 = Java.use('java.net.URL');
    a1.openConnection.overload('java.net.Proxy').implementation = function (proxy) {
        console.log('a 被调用了',proxy);
         return this.openConnection(proxy)
    }
    
    a1.openConnection.overload().implementation = function () {
         console.log('openConnection 被调用了');
         return this.openConnection()
    }
    
    var RouteSelector = Java.use('okhttp3.internal.connection.RouteSelector');
    
    RouteSelector.resetNextProxy.implementation = function (a,b) {
        console.log('resetNextProxy 被调用了a ',a);
        console.log('resetNextProxy 被调用了b ',b);
        console.log('resetNextProxy 被调用了 --------------------------');
        this.resetNextProxy(a,b)
        console.log('resetNextProxy 被调用了',this.address);
    }
    
    
    var Util = Java.use('okhttp3.internal.Util')
    Util.immutableList.overload('[Ljava.lang.Object;').implementation = function (uri) {
        console.log('immutableList 被调用了',uri);
        return this.immutableList(uri)
    
    }
    
    
    var li = Java.use('java.util.List')
    
    Util.immutableList.overload('java.util.List').implementation = function (list) {
        console.log('immutableListlist 被调用了',list.toString());
        // 打印 list 中的每个元素，假设它们是 Proxy 对象
       // 使用传统的 for 循环来遍历 Java List
    for (var i = 0; i < list.size(); i++) {
        var item = list.get(i);
         console.log('Item at index ' + i + ' is ', item);
    }
    
        var res = Java.cast(list,li)
         console.log('immutableListlist res被调用了',res.length);
        return this.immutableList(list)
    
    }
    
    
    var Proxy = Java.use('java.net.Proxy')
    Proxy.$init.overload('java.net.Proxy$Type','java.net.SocketAddress').implementation = function(a,b){
        console.log("$init");
        console.log("a ",a); //bytes格式转成字符串
        console.log("b ",b);

        var res = this.$init(a,b);
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




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

    var AnonymousClass3 = Java.use('com.soom.live999.activity.LauncherActivity$3');
    AnonymousClass3.callback.overload('com.miss.common.bean.ConfigBean').implementation = function (params) {
        console.log('callback 被调用了',params);
        var res = this.callback(params);
        return res
    };
    
   
   
    var AnonymousClass1 = Java.use('com.miss.common.http.HttpClient$1');
    AnonymousClass1.setParams.implementation = function (params) {
        console.log('setParams 被调用了',params);
    };
    
    
    var Request = Java.use('com.lzy.okgo.request.base.Request');
    Request.params.overload('java.lang.String','java.lang.String','[Z').implementation = function (key,value,b) {
        console.log('Request 被调用了key ->',key);
        console.log('Request 被调用了value ->',value);
        console.log('Request 被调用了b ->',b);
        return this;
    };
    
    Request.params.overload('java.lang.String','int','[Z').implementation = function (key,value,b) {
        console.log('Request 被调用了key ->',key);
        console.log('Request 被调用了value ->',value);
        console.log('Request 被调用了b ->',b);
         return this;
    };
    
    
     var HttpClient = Java.use('com.miss.common.http.HttpClient');
    HttpClient.getHostUrl.implementation = function () {
        var res = this.getHostUrl();
        console.log('getHostUrl 被调用了',res);
        return res;
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




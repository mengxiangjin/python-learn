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
    // Hook CommonHttpUtil.getConfig 方法
    var HttpsUtils = Java.use("com.lzy.okgo.https.HttpsUtils");
    
    // 拦截 getConfig 方法
    HttpsUtils.getSslSocketFactoryBase.implementation = function(q,p,r,t) {
        console.log("getSslSocketFactoryBase q ",q);
        console.log("getSslSocketFactoryBase p ",p);
        console.log("getSslSocketFactoryBase r ",r);
        console.log("getSslSocketFactoryBase t ",t);
        return this.getSslSocketFactoryBase(q,p,r,t);
    };
    
    var SSLContext = Java.use("javax.net.ssl.SSLContext");
    
    // 拦截 getConfig 方法
    SSLContext.getInstance.overload("java.lang.String").implementation = function(protocol) {
        console.log("enableCustomTrustManager",protocol);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        console.log("------------------------------------------")
        return this.getInstance(protocol);
    };
    
    SSLContext.init.implementation = function(a,b,c) {
        console.log("init a ",a)
        console.log("init b ",b)
        if(b != null && b.length > 0) {
            console.log("TrustManager class: ",b[0]);
        }
        console.log("init c ",c)
        this.init(a,b,c)
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



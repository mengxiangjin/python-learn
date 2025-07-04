import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.aiwujie.shengmo"])
session = rdev.attach(pid)


# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
      // 获取目标类的引用（即 com.miss.im.ChatUtil）
    var UserInfoActivity = Java.use('com.aiwujie.shengmo.activity.user.UserInfoActivity');
    

    // Hook checkAllowed 方法（假设该方法是静态方法）
    UserInfoActivity.showContactGiftPop.implementation = function (str) {
        console.log('showContactGiftPop 被调用了',str);
        this.showContactGiftPop(str)
    };
    
    
    var ListBean = Java.use('com.aiwujie.shengmo.bean.UserContactStateBean$DataBean$ListBean');
    

    // Hook checkAllowed 方法（假设该方法是静态方法）
    ListBean.getIs_send.implementation = function () {
        var res = this.getIs_send()
        console.log('getIs_send 被调用了',res);
        return "1"
    };
    
    
    var bean = Java.use('com.aiwujie.shengmo.tim.newtim.TIMC2CChatActivity$getChatPower$$inlined$let$lambda$1');
    

    // Hook checkAllowed 方法（假设该方法是静态方法）
    bean.doFailCallback.implementation = function (i,p,q) {
        console.log('doFailCallback 被调用了',i);
        console.log('doFailCallback 被调用了',p);
        console.log('doFailCallback 被调用了',q);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        this.doFailCallback(i,p,q)
    };
    
    
     var helper = Java.use('com.aiwujie.shengmo.net.HttpHelper$14');
    

    // Hook checkAllowed 方法（假设该方法是静态方法）
    helper.onSuccess.implementation = function (str) {
        console.log('onSuccess 被调用了',str);
        var realStr = str.replace('3001','2000')
         console.log('realStr 被调用了',realStr);
        this.onSuccess(realStr)
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




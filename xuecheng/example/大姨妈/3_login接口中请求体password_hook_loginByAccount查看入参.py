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

    var loginByAccountPresenter = Java.use("com.yoloho.kangseed.presenter.entrance.LoginByAccountPresenter");

    loginByAccountPresenter.loginByAccount.implementation = function(str1,str2){
        console.log("进入了loginByAccount--------------------");
        console.log("入参1：",str1);
        console.log("入参2：",str2);
        this.loginByAccount(str1,str2); //调用原来的函数
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

# 密码加密后P0H0qk3BfiiBrKZ1WUVGFQ==


# 进入了loginByAccount--------------------
# 入参1： 15655549539
# 入参2： zj123456



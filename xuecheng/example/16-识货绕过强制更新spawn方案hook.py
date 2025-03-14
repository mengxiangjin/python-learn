import frida
import sys

#spawn程序重启即开始监听hook
rdev = frida.get_remote_device()
# spawn写包名
pid = rdev.spawn(["com.hupu.shihuo"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {
    var UpdateDialog = Java.use('com.azhon.appupdate.dialog.UpdateDialog');
    UpdateDialog.show.implementation = function(ctx){
        console.log("执行了");
        //this.show();
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
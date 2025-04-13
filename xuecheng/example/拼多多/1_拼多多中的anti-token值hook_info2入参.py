import frida
import sys

# 连接手机设备
rdev = frida.get_remote_device()

session = rdev.attach("拼多多")

scr = """
Java.perform(function () {

    // 包.类
    var deviceNative = Java.use("com.xunmeng.pinduoduo.secure.DeviceNative");

    deviceNative.info2.implementation = function(ctx,j){
        console.log("入参：",j);
        var res = this.info2(ctx,j);
        console.log("返回值",res); 
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

#二次测试是时间戳
# 入参： 1744545873608
# 返回值 2afx8InYRPI6fON2k2lK8YprxK0lM+rWhapt1z2uFT2MbkTrQrk7H+Fd0qIVbJ4qIUuhJmQ4O3cL/8IJUTSRl6hRp97btzJX7ArvuHtbWdTF2Acu/umDgr5abSBDFhS1OzqUGCI0w9+1Xf2UPc7XDK6Q3fXJW0VeH/34Bc/GuiSCxOvUyuSLd0MV1BSsIbFJhJC9bUftrqjRNQk/9TYbO/qdlFD0rRgW6Xxs80B2a3xRekQKz+bc3ixu+fESkK7XwPAHHhjRElfd8ME/A5NG6a3LGbG++5FsLR2hHP1enwLK3J2rMZs3XDbpUwT06Xw3eYmFEZwfKC2Bt6GPnyNkNEB4U25H+/3IlVO/xXf9UbXoaPeidXp+kXTLdf2APGlQep2C2rfzFpa78QFewtSCbVjS0UsnbhCkpn44iRsHTlSlC4=
# 入参： 1744545878855
# 返回值 2afx8InYRPI6fON2k2lK8YprxK0lM+rWhapt1z2uFT2MbkTrQrk7H+Fd0qIVbJ4qIUuhJmQ4O3cL/8IJUTSRl6hRp97btzJX7ArvuHtbWdTF2Acu/umDgr5abSBDFhS1OzqUGCI0w9+1Xf2UPc7XDK6Q3fXJW0VeH/34Bc/GuiSCxOvUyuSLd0MV1BSsIbFJhJC9bUftrqjRNQk/9TYbO/qdlFD0rRgW6Xxs80B2a3xRekQKz+bc3ixu+fESkK7XwPAHHhjRElfd8ME/A5NG6a3LGbG++5FsLR2hHP1enwLK3J2rMZs3XDbpUwT06Xw3eYm9IVER0E3AxOs+Z7O1TC5fbVNeR0S7qzIhUjpKC8AgHVWpMj0F1B6edtnoQoS/WqL5AvXXeSAGhY+Nsrizj4nCOqLoy647/t4GSsLIf2DFLI=

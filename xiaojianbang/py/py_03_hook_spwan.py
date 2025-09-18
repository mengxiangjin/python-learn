import frida
import sys


device = frida.get_usb_device()
pid = device.spawn(["com.dodonew.online"])

session = device.attach(pid)

script_code = """
Java.perform(function () {
    var utils = Java.use('com.dodonew.online.util.Utils')
    utils.md5.implementation = function (str) {
        console.log('执行了md5:',str)
        var res = this.md5(str)
        console.log('返回值md5:',res)
        return res
    }

    var RequestUtil = Java.use('com.dodonew.online.http.RequestUtil')
    RequestUtil.encodeDesMap.overload('java.lang.String','java.lang.String','java.lang.String').implementation = function (data,key,iv) {
        console.log('执行了encodeDesMap:',data)
        console.log('执行了encodeDesMap:',key)
        console.log('执行了encodeDesMap:',iv)
        var res = this.encodeDesMap(data,key,iv)
        console.log('返回值encodeDesMap:',res)
        return res
    }
});
"""
script = session.create_script(script_code)
script.load()

device.resume(pid)  # 加载完脚本, 恢复进程运行
print('正在运行中')
sys.stdin.read()


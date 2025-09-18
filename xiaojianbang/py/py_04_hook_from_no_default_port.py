import frida
import sys

#可以同时监听多个server，一直add_remote_device即可


device = frida.get_device_manager().add_remote_device("192.168.2.28:12444")
session = device.attach("嘟嘟牛在线")

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

print('正在运行中')
sys.stdin.read()


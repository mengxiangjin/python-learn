import frida
import sys

'''
JS发送数据给Python：
    JavaScrip代码中执行send(),
    python代码中定义好触发器函数，----> func(message,data)  注意：必须接受二个参数的函数，函数名称可任意，与注册时对应即可
    python中注册该函数  ---> script.on('message',函数名称)  注意：'message'是固定的
    
        send()：最多有二个参数message，data
                message:封装在其payload，注意第一个参数发送二进制数据会接受不到
                data：用来接受二进制数据，发送非二进制的数据会接受不到

'''


device = frida.get_device_manager().add_remote_device("192.168.2.28:12444")
session = device.attach("嘟嘟牛在线")

script_code = """
Java.perform(function () {
    var utils = Java.use('com.dodonew.online.util.Utils')
    utils.md5.implementation = function (str) {
        console.log('执行了md5:',str)
        var res = this.md5(str)
        console.log('返回值md5:',res)
        send(res,new ArrayBuffer(16))
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

def on_message(message,data):
    print("py端接收到了JS传递的数据")
    if message['type'] == 'send':
        print("message中的数据：",message['payload'])
    print("datas",data)


script = session.create_script(script_code)
script.on('message',on_message)
script.load()

print('正在运行中')
sys.stdin.read()


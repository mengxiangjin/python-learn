import time

import frida
import sys

'''
Python发送数据给JS 
    Python代码中发送数据 ----> script.post({"data": "1111111111111"})
    JS代码可等待监听 --->  recv(function(obj){
                            console.log(JSON.stringify(obj));
                            console.log("Python:", obj.data);
                            res = obj.data;
                        }).wait()
    此时的obj参数即为发送的数据，注意，key需要用字符串写，否则拿到数据可能为null                    
'''


device = frida.get_usb_device()
session = device.attach("嘟嘟牛在线")

script_code = """
Java.perform(function () {
    var utils = Java.use('com.dodonew.online.util.Utils')
    utils.md5.implementation = function (str) {
        console.log('执行了md5:',str)
        var res = this.md5(str)
        console.log('返回值md5:',res)
        send(res,new ArrayBuffer(16))
        
        //等待Python给我返回数据，我要修改结果为Python返回的数据，阻塞等待
        recv(function(obj){
            console.log(JSON.stringify(obj));
            console.log("Python:", obj.data);
            res = obj.data;
        }).wait()
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
    print("py端接收到了JS传递的数据",message)
    if message['type'] == 'send':
        print("message中的数据：",message['payload'])
        time.sleep(5)

        #发送我自定义的数据给你
        script.post({"data": "1111111111111"})
    print("datas",data)


script = session.create_script(script_code)
script.on('message',on_message)
script.load()

print('正在运行中')
sys.stdin.read()


import time

import frida
import sys

'''
RPC导出JS函数供Python主动调用 
    JS中编写导出映射表:
        rpc.exports = {
            # rpcfunc ---> 自定义中python调用的方法名称  active_call_md5 ---> JS中定义的方法名称
            rpcfunc: active_call_md5
        };
    Python中主动调用:
        result = script.exports.rpcfunc('11112222')  
        
        
    注意：
        映射函数名称时pyhton中调用不管方法名称大写还是小写都是对应JS中小写，除非加上下划线
            rpcfunc --->  rpcfunc
            RpCFunC --->  rpcfunc
            rpc_func ---> rpcFunc
         
        rpc导出函数需要在应用启动后才会生效，即device.resume(pid)之后生效，有时在这之后进行rpc调用仍有可能会报错，此时可以加个time延迟即可
                                      
'''


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
    
    
    function active_call_md5(data) {
        let result = ''
        Java.perform(function() {
            var utils = Java.use('com.dodonew.online.util.Utils')
            result = utils.md5(data)
        })
        return result
    }
    
    
    console.log("js中主动调用result--->",active_call_md5('11112222'))


    //通过rpc导出该函数映射到自定义的函数名称
    rpc.exports = {
        rpcfunc: active_call_md5
    };
x
});
"""





script = session.create_script(script_code)
script.load()
device.resume(pid)

#不进行延迟可能会导致报错
time.sleep(2)
result = script.exports.rpcfunc('11112222')
print('Python中主动调用result--->', result)
sys.stdin.read()


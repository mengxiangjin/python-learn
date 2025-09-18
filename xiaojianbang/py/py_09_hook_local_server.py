import time

import frida
import sys
from fastapi import FastAPI
import uvicorn


from pydantic import BaseModel

'''
    通过rpc导出关键函数，python中可以获取到结果，进行后续网络请求等相关业务逻辑操作
'''


device = frida.get_usb_device()
pid = device.spawn(["com.dodonew.online"])
session = device.attach(pid)

script_code = """
Java.perform(function () {
    function encrypt(phone_number,password) {
        var time = new Date().getTime();
        let str = 'equtype=ANDROID&loginImei=Androidnull&timeStamp=' + time +  '&userPwd=' + password + '&username=' + phone_number  + '&key=sdlkjsdljf0j2fsjk'
        var utils = Java.use('com.dodonew.online.util.Utils')
        let sign = utils.md5(str).toUpperCase()
        console.log('sign ----> ',sign)
    
        var encryptData = '{"equtype":"ANDROID","loginImei":"Android352689082129358","sign":"'+ 
            sign +'","timeStamp":"'+ time +'","userPwd":"' + password + '","username":"' + phone_number + '"}';
        var RequestUtil = Java.use('com.dodonew.online.http.RequestUtil')
        var encrypt = RequestUtil.encodeDesMap(encryptData,'65102933','32028092')
        console.log('encrypt ----> ',encrypt)
        return encrypt
    }

    //通过rpc导出该函数映射到自定义的函数名称
    rpc.exports = {
        rpcfunc: encrypt
    };
x
});
"""

script = session.create_script(script_code)
script.load()
device.resume(pid)
#不进行延迟可能会导致报错
time.sleep(2)


class Request(BaseModel):
    phone:str
    password:str

app = FastAPI()

@app.get('/enc')
async def get_enc(phone,password):
    result = script.exports.rpcfunc(phone, password)
    print('Python中主动调用result--->', result)
    return {'res': result}

@app.post('/enc1')
async def post_enc(request: Request):
    result = script.exports.rpcfunc(request.phone, request.password)
    print('Python中主动调用result--->', result)
    return {'res': result}

if __name__ == '__main__':
    uvicorn.run(app,port=8080)

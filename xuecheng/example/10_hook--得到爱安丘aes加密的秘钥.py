import frida
import sys

# 连接手机设备
rdev = frida.get_remote_device()

session = rdev.attach("爱安丘")

scr = """
Java.perform(function () {

    // 包.类
    var EncryptUtil = Java.use("com.iqilu.core.util.EncryptUtil");

    EncryptUtil.getMD5.implementation = function(str){
        console.log("明文：",str);
        var res = this.getMD5(str); // 调用原来的
        console.log("md5加密结果=",res);  // 咱们需要的是这个，这个就是秘钥
        
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

'''
      c058579161250b37     AppUtils.getSR()    APP   137   ---->通过md5加密得到--》秘钥---》以后不会变
明文： c058579161250b37     48dce77cf43eb6c3     APP  137
md5加密结果= 6d6656a37cdb7977c10f6d83cab168e9   # aes加密的秘钥

'''
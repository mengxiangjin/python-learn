# AES_128_ECB_PKCS5Padding_Encrypt
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
    //去libJNIEncrypt.so文件中找AES_128_ECB_PKCS5Padding_Encrypt方法
    var addr_func = Module.findExportByName("libJNIEncrypt.so", "AES_128_ECB_PKCS5Padding_Encrypt");
    Interceptor.attach(addr_func, {
        onEnter: function(args){
            console.log("--------------------------执行函数--------------------------");
            console.log("参数1：", args[0].readUtf8String());
            console.log("参数2：", args[1].readUtf8String());
        },
        onLeave: function(retValue){
            console.log("返回值:", retValue.readUtf8String());
        }
    })
});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()

# '''
# 参数1： loginTokenplatformandroidtimestamp1741921134712type1uuid4d46de23c1970252v4.74.5
# 参数2： d245a0ba8d678a61 aes加密的key 01010101转16进制的结果
# 返回值: knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs3QulLUT5Y9gUa0jqWMoitsxdUnez0HG5VIgvs3AzEA/ibOfWq5Gs0i+3tWePKGWk4=
# # 验证了，拿着明文，拿着秘钥，通过aes加密--》使用 base64编码---》得到返回值
# knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs3QulLUT5Y9gUa0jqWMoitsxdUnez0HG5VIgvs3AzEA/ibOfWq5Gs0i+3tWePKGWk4=

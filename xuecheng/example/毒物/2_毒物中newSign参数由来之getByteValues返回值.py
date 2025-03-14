import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
     var AESEncrypt = Java.use("com.duapp.aesjni.AESEncrypt");
    AESEncrypt.getByteValues.implementation = function(){
        var res = this.getByteValues();
        console.log('getByteValues返回值是：',res);
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

#getByteValues返回值是： 101001011101110101101101111100111000110100010101010111010001000101100101010010010101110111010011101001011101110101100101001100110000110100011101010111011011001101001101011101010100001101000011


import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
    var AESEncrypt = Java.use("com.duapp.aesjni.AESEncrypt");
    // encode是重载的方法，has more than one overload error
    // AESEncrypt.encode.implementation = function(obj,str){
    //    console.log('参数1 ',obj);
    //   console.log('参数2 ',str);
    //    var res = this.encode(obj,str);
    //    console.log('encode：',res);
    //    return res;
   // }
    
    AESEncrypt.encode.overload('java.lang.Object','java.lang.String').implementation = function(obj,str){
        console.log('参数1 ',obj);
        console.log('参数2 ',str);
        var res = this.encode(obj,str);
        console.log('encode：',res);
        return res;
    };
});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()

# 参数1  com.shizhuang.duapp.modules.app.DuApplication@3784f77
# 参数2  loginTokenplatformandroidtimestamp1741852561920type1uuid4d46de23c1970252v4.74.5
# encode： knGGXR0bR7LQn4eRCvJsdZ4D96wrRcYi2zPWWxLMOs1LGifdXR7pTKgsBWd5uDIsxdUnez0HG5VIgvs3AzEA/ibOfWq5Gs0i+3tWePKGWk4=
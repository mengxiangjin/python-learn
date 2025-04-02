import frida
rdev = frida.get_remote_device()
session = rdev.attach("大姨妈")

scr = """
rpc.exports = {   
    yy:function(j2,str,j3){
         var res;
         Java.perform(function () { 
            // 包.类
            var Crypt = Java.use("com.yoloho.libcore.util.Crypt");
            // 类中的方法
            res = Crypt.encrypt_data(j2,str,j3);
         });

         return res;
    }
}
"""
script = session.create_script(scr)
script.load()

# 使用python调用
sign = script.exports_sync.yy(0,
                              '929dd3baab6e4679798a1776c70bb0186d0ca3f3user/login15655549539P0H0qk3BfiiBrKZ1WUVGFQ==',
                              85)
print(sign)  # eae2f8f6456337b68388dcf5d56c8253


# 电脑必须连着手机--》手机上必须运行app

#b19552e03ac08dc753e660774223e0cb
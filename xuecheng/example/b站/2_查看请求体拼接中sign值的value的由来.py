import frida
import sys

#attach 程序已经处于运行状态才能进行监听hook
#模拟器启动frida-server
#运行程序开始监听，模拟器应用操作模拟，触发监听
# 连接手机设备
rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")  # app名字
# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    //找到类 反编译的首行+类名：com.bilibili.commons.m.a下的
    var d = Java.use("com.bilibili.commons.m.a");
    var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    
    //替换类中的方法
    d.g.implementation = function(bArr1,bArr2){
        console.log("传入的参数：",bArr1);
        console.log("传入的参数：",bArr2);
        console.log("bytes=",ByteString.of(bArr1).utf8());
        console.log("bytes2=",ByteString.of(bArr2).utf8());
        var res = this.g(bArr1,bArr2); //调用原来的函数
        console.log("返回值字节数组：",res);
        return res;  
    }
});
"""


# -----下面固定---以后不会动
script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()

#sign的由来：1 一串字符串aid=114085018475145&auto_play=0&build=6240300&cid=28630322467&did=IEV3QXlBIht-TnxFcBEjEVEBaBB1GStzPw&epid=&from_spmid=search.search-result.0.0&ftime=1742543780&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1743059499&sub_type=0&type=3
    # 2 通过盐：9cafa6466a028bfb  + sha256 加密 得到加密串  验证一样的返回值字节数组
    # 3 转成16进制

# 传入的参数： 97,105,100,61,49,49,52,48,56,53,48,49,56,52,55,53,49,52,53,38,97,117,116,111,95,112,108,97,121,61,48,38,98,117,105,108,100,61,54,50,52,48,51,48,48,38,99,105,100,61,50,56,54,51,48,51,50,50,52,54,55,38,100,105,100,61,73,69,86,51,81,88,108,66,73,104,116,45,84,110,120,70,99,66,69,106,69,86,69,66,97,66,66,49,71,83,116,122,80,119,38,101,112,105,100,61,38,102,114,111,109,95,115,112,109,105,100,61,115,101,97,114,99,104,46,115,101,97,114,99,104,45,114,101,115,117,108,116,46,48,46,48,38,102,116,105,109,101,61,49,55,52,50,53,52,51,55,56,48,38,108,118,61,48,38,109,105,100,61,48,38,109,111,98,105,95,97,112,112,61,97,110,100,114,111,105,100,38,112,97,114,116,61,49,38,115,105,100,61,48,38,115,112,109,105,100,61,109,97,105,110,46,117,103,99,45,118,105,100,101,111,45,100,101,116,97,105,108,46,48,46,48,38,115,116,105,109,101,61,49,55,52,51,48,53,57,52,57,57,38,115,117,98,95,116,121,112,101,61,48,38,116,121,112,101,61,51
# 传入的参数： 57,99,97,102,97,54,52,54,54,97,48,50,56,98,102,98
# bytes= aid=114085018475145&auto_play=0&build=6240300&cid=28630322467&did=IEV3QXlBIht-TnxFcBEjEVEBaBB1GStzPw&epid=&from_spmid=search.search-result.0.0&ftime=1742543780&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1743059499&sub_type=0&type=3
# bytes2= 9cafa6466a028bfb
# 返回值字节数组： b9228dd3809340d8ad290c7cc31986aa747751270b54b18480dd76f1345e830f

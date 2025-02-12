
// hook代码如下
Java.perform(function () {
    //找到类 反编译的首行+类名：com.autohome.ahkit.utils下的
    var SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");

    //替换类中的方法
    SecurityUtil.encodeMD5.implementation = function(str){
        console.log("传入的参数(未加密之前的)：",str);
        var res = this.encodeMD5(str); //调用原来的函数
        console.log("返回值（加密后的字符串）：",res);
        return str;  // 没加密的
    }
});

// 执行是，选择用attach还是  spwan方案


// attach 方案执行命令：   frida -UF -l 6-hook-pwd-attach.js

// spwan 方案执行命令：  frida -U -f com.che168.autotradercloud -l 6-hook-pwd-attach.js
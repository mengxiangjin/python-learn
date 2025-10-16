/*
* 修改native函数中的参数以及返回值
*
* HookDemo.apk + libxiaojianbang.so
* */


function updateIntValue() {
    let base_address = Module.findBaseAddress("libxiaojianbang.so")
    Interceptor.attach(base_address.add(0x165C),{
        onEnter:function (args) {
            //修改整形参数值
            args[2] = ptr(20)
            console.log("params2:",args[2].toInt32())
            console.log("params3:",args[3].toInt32())
            console.log("params4:",args[4].toInt32())
        },
        onLeave:function (retval) {
            //修改整形返回值
            retval.replace(ptr(1000))
            console.log("retval:",retval.toInt32())
        }
    })
}


Java.perform(function() {

    let base_address = Module.findBaseAddress("libxiaojianbang.so")


    var newStr = "gdfgdhfgjghjgkhjkh;kl;k;";
    var newStrAddr = Memory.allocUtf8String(newStr);

    Interceptor.attach(base_address.add(0x1D68), {
    onEnter: function (args) {
        this.args0 = args[0];
        this.args1 = args[1];
        if(args[1].readCString() == "xiaojianbang"){
            //修改字符串参数
            args[1] = newStrAddr;
            console.log(hexdump(args[1]));
            args[2] = ptr(newStr.length);
            console.log(args[2].toInt32());
        }
        }, onLeave: function (retval) {
            if(this.args1.readCString() == "xiaojianbang"){
                console.log(hexdump(this.args0));
            }
        }
    });

})
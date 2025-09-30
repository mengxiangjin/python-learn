/*
    对传入的params1和param2进行字符串拼接后用sha1加密返回
    拼接格式：
        snprintf(
             v11,
             v9 + 80,
             "%s&%s&%s&%s",
             "877a9ba7a98f75b90a9d49f53f15a858",
             "NjhhMDRiODE3N2JkYzllNWUxNmE4OWU2Nzc3YTdiNjY=",
             v5,
             v7);
    877a9ba7a98f75b90a9d49f53f15a858&NjhhMDRiODE3N2JkYzllNWUxNmE4OWU2Nzc3YTdiNjY=&4.0.0&1757324626928imrtsD 进行加密返回
*/
function call_active() {
    var Utils = Java.use('com.hoge.android.jni.Utils')
    var params1 = "4.0.0"
    var params2 = "1757324626928imrtsD"
    var instance = Utils.$new()
    var res = instance.signature(params1,params2)
    console.log("主动调用获取到的结果",res)

    //08165c94fc606e86613cea591592804bcd8016ec
}


Java.perform(function() {
    var Utils = Java.use('com.hoge.android.jni.Utils')
    Utils.signature.implementation = function (a,b) {
        console.log("params:1",a)
        console.log("params:2",b)
        var res = this.signature(a,b)
        console.log("result:",res)
        return res
    }

    var address = Module.findBaseAddress("libm2o_jni.so")
    console.log("base address",address)
    // //
    var sha1_addr = address.add(0xA86C + 1)
    Interceptor.attach(sha1_addr, {
        onEnter: function(args) {
            this.input = args[0];
            this.len = args[1];
            this.output = args[2];
            console.log("╔══════════════════════════════════╗");
            console.log("║          sha1_addr onEnter 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入缓冲: " + this.input + "        ║");
            console.log("║ 输入长度: " + this.len.toInt32() + "        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("╠══════════════════════════════════╣");
            console.log(hexdump(this.input,{
                offset:0,
                length:this.len.toInt32(),
                header:true,
                ansi:true
            }))
            console.log("输入字符串：",Memory.readUtf8String(this.input))

        },
        onLeave: function(retval) {
            console.log("╠══════════════════════════════════╣");
            console.log("║          sha1_addr onLeave 被调用          ║");
            console.log("╠══════════════════════════════════╣");
            console.log("返回值：",retval.toInt32())
            if (retval.toInt32() === 0) {
                var output_string = Memory.readUtf8String(this.output.readPointer());
                console.log("║          sha1加密的结果二级指针指向的值          ║");
                console.log(hexdump(this.output.readPointer(),{
                    offset:0,
                    length:output_string.length,
                    header:true,
                    ansi:true
                }))
                console.log("sha1加密的结果",output_string)
                //二种方式都可行
                // 使用 Memory.readPointer() 来解引用二级指针
                // var output_string_ptr = Memory.readPointer(this.output);
            }
            console.log("╚══════════════════════════════════╝");

        }
    });



})


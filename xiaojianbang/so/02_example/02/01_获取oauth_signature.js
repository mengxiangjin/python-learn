
//对传入的params2进行hmac加密（key是asfsaADDJF55b262d99cff7cac7459e8&）后再进行base64编码返回
function call_auth() {
    var AuthorizeHelper = Java.use('com.mfw.tnative.AuthorizeHelper')
    var params2 = "PUT&https%3A%2F%2Fmapi.mafengwo.cn%2Frest%2Fapp%2Fuser%2Flogin%2F&after_style%3Ddefault%26app_code%3Dcom.mfw.roadbook%26app_ver%3D8.1.6%26app_version_code%3D535%26brand%3Dgoogle%26channel_id%3DGROWTH-WAP-LC-3%26device_id%3D9E%253AAB%253A9F%253AAC%253A40%253A41%26device_type%3Dandroid%26hardware_model%3DPixel%25202%2520XL%26mfwsdk_ver%3D20140507%26o_lat%3D31.837912%26o_lng%3D117.134873%26oauth_consumer_key%3D5%26oauth_nonce%3D7be11328-cc8b-48dd-b6f4-bcdf2f56cb23%26oauth_signature_method%3DHMAC-SHA1%26oauth_timestamp%3D1757064754%26oauth_version%3D1.0%26open_udid%3D9E%253AAB%253A9F%253AAC%253A40%253A41%26put_style%3Ddefault%26screen_height%3D2712%26screen_scale%3D3.5%26screen_width%3D1440%26sys_ver%3D11%26time_offset%3D480%26x_auth_mode%3Dclient_auth%26x_auth_password%3D123456%26x_auth_username%3D15655549599"
    var params3 = ""
    var params4 = "com.mfw.roadbook"
    var params5 = true
    //拿到context上下文
    var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
    var context = currentApplication.getApplicationContext();
    var instance = AuthorizeHelper.$new("com.mfw.roadbook")

    var res = instance.xAuthencode(context,params2,params3,params4,params5)
    console.log("主动调用获取到的结果",res)
    //Cl7ihG9LlYOBQgbsDiFoa6diVoI=
}


Java.perform(function() {
    var AuthorizeHelper = Java.use('com.mfw.tnative.AuthorizeHelper')
    AuthorizeHelper.xAuthencode.implementation = function (a,b,c,d,e) {
        console.log("params:1",a)
        console.log("params:2",b)
        console.log("params:3",c)
        console.log("params:4",d)
        console.log("params:5",e)
        var res = this.xAuthencode(a,b,c,d,e)
        console.log("result:",res)
        return res
    }

    var address = Module.findBaseAddress("libmfw.so")
    console.log("base address",address)
    //
    var base64_addr = address.add(0x6e3c + 1)
    Interceptor.attach(base64_addr, {
        onEnter: function(args) {
            this.input = args[1];
            this.len = args[2];
            console.log("╔══════════════════════════════════╗");
            console.log("║          base64_addr onEnter 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入参数: " + this.input + "        ║");
            console.log("║ 输入长度: " + this.len.toInt32() + "        ║");

            var input = Memory.readByteArray(this.input, this.len.toInt32());
            console.log("╠══════════════════════════════════╣");
            console.log("║          base64_addr onEnter 输入的值          ║");
            console.log("╠══════════════════════════════════╣");
            console.log(hexdump(input, {
                offset: 0,
                length: this.len.toInt32(),
                header: true,
                ansi: true
            }));
        },
        onLeave: function(retval) {

            var output_string = Memory.readUtf8String(retval);

            var retval_result = Memory.readByteArray(retval, output_string.length);

            console.log("╠══════════════════════════════════╣");
            console.log("║          base64_addr onLeave 计算结果          ║");
            console.log("╠══════════════════════════════════╣");

            console.log(hexdump(retval_result, {
                offset: 0,
                length: output_string.length,
                header: true,
                ansi: true
            }));
            console.log("╚══════════════════════════════════╝");
    }
    });
    //

    var sha1Updateaddr = address.add(0x82A4 + 1)
    Interceptor.attach(sha1Updateaddr,{
        onEnter: function (args) {
            this.input = args[1];
            this.len = args[2];
            console.log("╔══════════════════════════════════╗");
            console.log("║          SHA1Update onEnter 被调用        ║");
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

        },
        onLeave:function (retval) {
             console.log("╠══════════════════════════════════╣");
             console.log("║          SHA1Update onLeave 输入的值          ║");
             console.log("╠══════════════════════════════════╣");
             console.log(hexdump(this.input,{
                offset:0,
                length:this.len.toInt32(),
                header:true,
                ansi:true
            }))
            console.log("╚══════════════════════════════════╝");
        }
    });
    //
    var sha1FinalAddr = address.add(0x6A80 + 1)
    Interceptor.attach(sha1FinalAddr,{
        onEnter:function (args) {
            this.input = args[1];
            this.len = args[2]
            console.log("╔══════════════════════════════════╗");
            console.log("║          sha1FinalAddr onEnter 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入数据input: " + this.input + "        ║");
            console.log("║ 输入数据len: " + this.len.toInt32() + "        ║");
            console.log(hexdump(this.input, {
                offset: 0,
                length: this.len.toInt32(),
                header: true,
                ansi: true
            }));

        },
        onLeave:function (retval){
            console.log("╠══════════════════════════════════╣");
            console.log("║         sha1FinalAddr onLeave 计算结果          ║");
            console.log("╠══════════════════════════════════╣");
            console.log(hexdump(this.input, {
                offset: 0,
                length: this.len.toInt32(),
                header: true,
                ansi: true
            }));
            console.log("╚══════════════════════════════════╝");
        }
    });
    //

    var setKeyAddr = address.add(0x6938 + 1)
    Interceptor.attach(setKeyAddr,{
        onEnter:function (args) {
            this.input = args[1];
            this.len = args[2]
            console.log("╔══════════════════════════════════╗");
            console.log("║          setKeyAddr onEnter 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入数据input: " + this.input + "        ║");
            console.log("║ 输入数据len: " + this.len.toInt32() + "        ║");
            console.log(hexdump(this.input, {
                offset: 0,
                length: this.len.toInt32(),
                header: true,
                ansi: true
            }));

        },
        onLeave:function (retval){
            console.log("╠══════════════════════════════════╣");
            console.log("║         setKeyAddr onLeave 计算结果          ║");
            console.log("╠══════════════════════════════════╣");
            console.log(hexdump(this.input, {
                offset: 0,
                length: this.len.toInt32(),
                header: true,
                ansi: true
            }));
            console.log("╚══════════════════════════════════╝");
        }
    });

})


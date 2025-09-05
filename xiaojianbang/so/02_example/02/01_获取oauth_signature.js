

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
            console.log("║          base64_addr 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入参数: " + this.input + "        ║");
            console.log("║ 输入长度: " + this.len.toInt32() + "        ║");

            var input = Memory.readByteArray(this.input, this.len.toInt32());
            console.log("╠══════════════════════════════════╣");
            console.log("║          base64_addr 输入的值          ║");
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
            console.log("║          base64_addr 计算结果          ║");
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
    // var sha1Inputaddr = address.add(0x15BE + 1)
    // Interceptor.attach(sha1Inputaddr,{
    //     onEnter: function (args) {
    //         this.output = args[1];
    //         this.len = args[2];
    //         console.log("╔══════════════════════════════════╗");
    //         console.log("║          SHA1Input 被调用        ║");
    //         console.log("╠══════════════════════════════════╣");
    //         console.log("║ 输入缓冲: " + this.output + "        ║");
    //         console.log("║ 输入长度: " + this.len.toInt32() + "        ║");
    //
    //     },
    //     onLeave:function (retval) {
    //          var result = retval.toInt32();
    //          console.log("SHA1Input║ 返回值: " + result + "                      ║");
    //          if (result === 0) {
    //              var sha1_result = Memory.readByteArray(this.output, this.len.toInt32());
    //              console.log("╠══════════════════════════════════╣");
    //              console.log("║          SHA-1 输入的值          ║");
    //              console.log("╠══════════════════════════════════╣");
    //              console.log(hexdump(sha1_result, {
    //                  offset: 0,
    //                  length: this.len.toInt32(),
    //                  header: true,
    //                  ansi: true
    //              }));
    //          }
    //          console.log("╚══════════════════════════════════╝");
    //     }
    // });
    //
    // var base64EncodeAddr = address.add(0x13b4 + 1)
    // Interceptor.attach(base64EncodeAddr,{
    //     onEnter:function (args) {
    //         this.input = args[0];
    //         this.output = args[1];
    //         this.len = args[2]
    //         console.log("╔══════════════════════════════════╗");
    //         console.log("║          Base64Encode 被调用        ║");
    //         console.log("╠══════════════════════════════════╣");
    //         console.log("║ 输入数据input: " + this.input + "        ║");
    //         console.log("║ 输入数据output: " + this.output + "        ║");
    //         console.log("║ 输入数据len: " + this.len.toInt32() + "        ║");
    //         var inputArray = Memory.readByteArray(this.input, this.len.toInt32());
    //         console.log(hexdump(inputArray, {
    //             offset: 0,
    //             length: this.len.toInt32(),
    //             header: true,
    //             ansi: true
    //         }));
    //
    //     },
    //     onLeave:function (retval){
    //         var result = retval.toInt32();
    //         console.log("Base64Encode ║ 返回值: " + result + "                      ║");
    //
    //         // 读取直到遇到 null 终止符
    //         var output_string = Memory.readUtf8String(this.output);
    //         this.input_len = output_string.length;
    //
    //         var base64_result = Memory.readByteArray(this.output, this.input_len);
    //
    //         console.log("╠══════════════════════════════════╣");
    //         console.log("║         Base64Encode 计算结果          ║");
    //         console.log("╠══════════════════════════════════╣");
    //         console.log(hexdump(base64_result, {
    //             offset: 0,
    //             length: this.input_len,
    //             header: true,
    //             ansi: true
    //         }));
    //         console.log("║ " + hex_output + " ║");
    //         console.log("╚══════════════════════════════════╝");
    //     }
    // });



})


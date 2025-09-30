

//传入的字符串拼接固定的字符串后进行Base64编码后再进行Sha1加密即为获取到的sign值
function call_sign() {
    var TreUtil = Java.use('com.maihan.tredian.util.TreUtil')
    var params = "app_ver=100&nonce=cw0vd81757051310679&timestamp=1757051310&tzrd=BwzXzSGFyiPstMIVuzTZb7LzTZzbXRJOFzpbQiIaT7v3yDIfKyKLV5KaiR6PxeWBCMDpXow3A" +
            "lphz0wVj0SKvcBfvPXquz2yJmu3k8rkroG5hrXPupk7cnjBYz1Ql+z9wkyGAMZcnlV0jEYsRn3f/2Kz/ZTsL0wSE/B2HEnKg6Ul7QvsJ5XzgfMTZ4fbIp8AG6guZBfBzctfsldUtp4Uv3m5kx" +
            "Zpw+dOaFbZCuoOsJ24UvOvAuKJVCA4H8Z/XOT9qRbmwQ/H2I+Jr57zFUs0Da6iZGEmu61L/s+bH1Qc4EwFH2ap2JKF7WsGxE/M3yYhKbwXjWr4ROrqOdKgTe+TlxBTA6T743hHbZK8DCDOkgU" +
            "ly8VTTUsmDqb0p6yOQytRIBBNEAfIDSgiU3UAgwQVSzjW8+B41dgNldwTzWSuC1rv75XIABNWi8pZNOTn+qw/aRe6wKzc4m+WSA75I+nesk5qtNYvS6upSw9zUM3S8X/sITVMpUfN13+pDU693zUr"
    var res = TreUtil.sign(params)
    console.log("主动调用获取到的结果",res)
}


Java.perform(function() {
    var TreUtil = Java.use('com.maihan.tredian.util.TreUtil')
    TreUtil.sign.implementation = function (str) {
        console.log("params:",str)
        var res = this.sign(str)
        console.log("results:",res)
        return res
    }

    var address = Module.findBaseAddress("libtre.so")
    console.log("base address",address)

    var sha1Result_addr = address.add(0x14c8 + 1)
    Interceptor.attach(sha1Result_addr, {
        onEnter: function(args) {
            this.output = args[1];
            console.log("╔══════════════════════════════════╗");
            console.log("║          SHA1Result 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输出缓冲: " + this.output + "        ║");
    },
        onLeave: function(retval) {
            var result = retval.toInt32();
            console.log("SHA1Result ║ 返回值: " + result + "                      ║");

            if (result === 0) {
                // 读取SHA-1结果
                var sha1_result = Memory.readByteArray(this.output, 20);

                console.log("╠══════════════════════════════════╣");
                console.log("║          SHA-1 计算结果          ║");
                console.log("╠══════════════════════════════════╣");
                console.log(hexdump(sha1_result, {
                    offset: 0,
                    length: 20,
                    header: true,
                    ansi: true
                }));

                // 转换为十六进制字符串
                var hex_chars = "0123456789abcdef";
                var hex_output = "";
                for (var i = 0; i < 20; i++) {
                    var byte = Memory.readU8(this.output.add(i));
                    hex_output += hex_chars[(byte >> 4) & 0x0F];
                    hex_output += hex_chars[byte & 0x0F];
                }
                console.log("║ " + hex_output + " ║");
            }

            console.log("╚══════════════════════════════════╝");
    }
    });

    var sha1Inputaddr = address.add(0x15BE + 1)
    Interceptor.attach(sha1Inputaddr,{
        onEnter: function (args) {
            this.output = args[1];
            this.len = args[2];
            console.log("╔══════════════════════════════════╗");
            console.log("║          SHA1Input 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入缓冲: " + this.output + "        ║");
            console.log("║ 输入长度: " + this.len.toInt32() + "        ║");

        },
        onLeave:function (retval) {
             var result = retval.toInt32();
             console.log("SHA1Input║ 返回值: " + result + "                      ║");
             if (result === 0) {
                 var sha1_result = Memory.readByteArray(this.output, this.len.toInt32());
                 console.log("╠══════════════════════════════════╣");
                 console.log("║          SHA-1 输入的值          ║");
                 console.log("╠══════════════════════════════════╣");
                 console.log(hexdump(sha1_result, {
                     offset: 0,
                     length: this.len.toInt32(),
                     header: true,
                     ansi: true
                 }));
             }
             console.log("╚══════════════════════════════════╝");
        }
    });

    var base64EncodeAddr = address.add(0x13b4 + 1)
    Interceptor.attach(base64EncodeAddr,{
        onEnter:function (args) {
            this.input = args[0];
            this.output = args[1];
            this.len = args[2]
            console.log("╔══════════════════════════════════╗");
            console.log("║          Base64Encode 被调用        ║");
            console.log("╠══════════════════════════════════╣");
            console.log("║ 输入数据input: " + this.input + "        ║");
            console.log("║ 输入数据output: " + this.output + "        ║");
            console.log("║ 输入数据len: " + this.len.toInt32() + "        ║");
            var inputArray = Memory.readByteArray(this.input, this.len.toInt32());
            console.log(hexdump(inputArray, {
                offset: 0,
                length: this.len.toInt32(),
                header: true,
                ansi: true
            }));

        },
        onLeave:function (retval){
            var result = retval.toInt32();
            console.log("Base64Encode ║ 返回值: " + result + "                      ║");

            // 读取直到遇到 null 终止符
            var output_string = Memory.readUtf8String(this.output);
            this.input_len = output_string.length;

            var base64_result = Memory.readByteArray(this.output, this.input_len);

            console.log("╠══════════════════════════════════╣");
            console.log("║         Base64Encode 计算结果          ║");
            console.log("╠══════════════════════════════════╣");
            console.log(hexdump(base64_result, {
                offset: 0,
                length: this.input_len,
                header: true,
                ansi: true
            }));
            console.log("║ " + " ║");
            console.log("╚══════════════════════════════════╝");
        }
    });



})


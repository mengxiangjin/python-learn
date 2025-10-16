



function stringToBytes(str){
    return hexToBytes(stringToHex(str));
}

// Convert a ASCII string to a hex string
function stringToHex(str) {
    return str.split("").map(function(c) {
        return ("0" + c.charCodeAt(0).toString(16)).slice(-2);
    }).join("");
}

function hexToBytes(hex) {
    for (var bytes = [], c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return bytes;
}

// Convert a hex string to a ASCII string
function hexToString(hexStr) {
    var hex = hexStr.toString();//force conversion
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}


function writeToMemory() {
    var module = Process.findModuleByName("libxiaojianbang.so");
     //修改内存地址的权限
     Memory.protect(module.base, module.size, 'rwx')

     let str_addr = module.base.add(0x38A1)
     //打印出以该内存起始的连续内存空间
     console.log(hexdump(str_addr));
     //打印出该字符串，读取到\0结束  com/xiaojianbang/ndk/NativeHelper
     console.log(str_addr.readCString())
     console.log("-----------------------------")

     //字符串写入到该内存中（一个字符串一个字节）
     console.log(module.base.add(0x38A1).writeByteArray(stringToBytes("0123456789abcdef")));
     //读取该内存的前33个字节 0123456789abcdef/ndk/NativeHelper
     console.log(module.base.add(0x38A1).readCString());
     console.log(module.base.add(0x38A1).readByteArray(33));
     console.log("-----------------------------")

     //十六进制格式写入到该内存内存中，01代表一个字节进行填充
     console.log(module.base.add(0x38A1).writeByteArray(hexToBytes("0123456789abcdef")));
     console.log(module.base.add(0x38A1).readByteArray(33));
}


/*
* 加法转减法
* 汇编指令中加法改写成减法，内存快中该条汇报的偏移地址是0x167C
* 其原始的机器码是08 01 09 0B 代表的汇编 ADD W8, W8, W9
* 询问deepseek或者在线网站https://armconverter.com/ 想将其汇编变为SUB W8, W8, W9,其对应的机器码 08 01 09 4B 故我们需要手动修改其内存中的值
* 08 01 09 0B    ADD W8, W8, W9  ---> 08 01 09 4B    SUB W8, W8, W9
*/
function add_2_sub(target_addr) {
    console.log("add_2_sub onEnter------------------>")
    console.log(hexdump(target_addr))
    console.log("原汇编：",Instruction.parse(target_addr).toString())
    //写入16进制08 01 09 4B （4个字节）
    target_addr.writeByteArray(hexToBytes("0801094B"))
    console.log("新汇编：",Instruction.parse(target_addr).toString())
    console.log(hexdump(target_addr))
    console.log("add_2_sub onLeave------------------>")
}


/*
* 删除（跳过）汇编中的某行
*  new Arm64Writer(target_addr,{pc:target_addr}).putNop()  实际是将16进制机器码1f2003d5写入到内存中
*   pc参数：相对偏移量 可加可不加，对于一些绝对指令的命令可无需添加PC，对于一些BL（跳转）需要添加 推荐无论什么都加上
* */
function del_target_addr(target_addr) {
    console.log("del_target_addr onEnter------------------>")
    console.log(hexdump(target_addr))
    console.log("原汇编：",Instruction.parse(target_addr).toString())

    new Arm64Writer(target_addr,{pc:target_addr}).putNop()

    console.log("新汇编：",Instruction.parse(target_addr).toString())
    console.log(hexdump(target_addr))
    console.log("del_target_addr onLeave------------------>")
}


function patch_code(target_addr) {
    console.log("patch_code onEnter------------------>")
    console.log(hexdump(target_addr))
    console.log("原汇编：",Instruction.parse(target_addr).toString())

    //更便捷写入到内存中，无需申请权限等繁琐
    Memory.patchCode(target_addr,4,function(code) {
        //写入机器码 对应乘法的汇编 回调参数code对应地址，大多数等同于target_addr，但不可使用target_addr
        code.writeByteArray(hexToBytes("087D091B"))


        var writer = new Arm64Writer(code,{pc:target_addr})
        writer.putNop() //跳过
        writer.putRet()//直接返回（return）
        writer.flush()
        writer.putBytes(hexToBytes("087D091B"))
    })
    console.log("新汇编：",Instruction.parse(target_addr).toString())
    console.log(hexdump(target_addr))
    console.log("patch_code onLeave------------------>")
}

Java.perform(function() {
    // writeToMemory()

    var module = Process.findModuleByName("libxiaojianbang.so");
     //申请权限
    Memory.protect(module.base,module.size,"rwx")
    var target_addr = module.base.add(0x167C)
    add_2_sub(target_addr)
    del_target_addr(target_addr)
    patch_code(target_addr)

})
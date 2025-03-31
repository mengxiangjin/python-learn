// 去内存中中 libkeyinfo.so  getByteHash
var addr = Module.findExportByName("libkeyinfo.so", "getByteHash");
console.log(addr); //0xb696387d



Interceptor.attach(addr,{
    onEnter:function (args){
        this.x1 = args[2];
        this.x2 = args[3];
    },
    onLeave:function(retval) {
        console.log("--------------------")
        console.log(Memory.readCString(this.x1));
        console.log(Memory.readCString(this.x2));
        console.log(Memory.readCString(retval));
    }

})

// frida -U -f com.achievo.vipshop -l hook04.js    重启app+hook（出问题）
// frida -UF -l hook04.js                          手动启动+hook


// 纯手动hook，可能不能---》拼手速，有时候很巧，就可以，有时候就不行
// 延迟hook
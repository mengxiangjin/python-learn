Java.perform(function() {


    //枚举so文件下的导入表
    console.log('------------------------------导入表开始');
    var improts = Module.enumerateImports("libencryptlib.so");
    for(let i = 0; i < improts.length; i++){
        // console.log(JSON.stringify(improts[i]));
        console.log(improts[i].name + " " + improts[i].address);
    }
    console.log('------------------------------导入表结束');

    console.log('------------------------------导出表开始');
    var exports = Module.enumerateExports("libencryptlib.so")
    for (let i = 0; i < exports.length; i++) {
        // console.log(JSON.stringify(improts[i]));
        console.log(exports[i].name + " " + exports[i].address);
    }
    console.log('------------------------------导出表结束');


    console.log('------------------------------符号表开始');
    var symbols = Module.enumerateSymbols("libencryptlib.so")
    for (let i = 0; i < exports.length; i++) {
        // console.log(JSON.stringify(improts[i]));
        console.log(symbols[i].name + " " + symbols[i].address);
    }
    console.log('------------------------------符号表结束');

    console.log('------------------------------枚举进程中已经加载的模块(lib)开始');
    var modules = Process.enumerateModules()
    for (let i = 0; i < modules.length; i++) {
        console.log(JSON.stringify(modules[i]));
        if (modules[i].name === 'libencryptlib.so') {
            console.log('-------------找到你了看看你的导出表')
            modules[i].enumerateExports()
        }
        // console.log(symbols[i].name + " " + symbols[i].address);
    }
    console.log('------------------------------枚举进程中已经加载的模块(lib)结束');

    var addr = Module.findExportByName("libxiaojianbang.so","_ZN7MD5_CTX11MakePassMD5EPhjS0_");
    console.log(addr)
})
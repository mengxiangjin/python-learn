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


    let addr = Module.findExportByName("libencryptlib.so","Java_com_pocket_snh48_base_net_utils_EncryptlibUtils_MD5");
    console.log(addr)
    Interceptor.attach(addr,{
        onEnter:function (args) {
            //参数是jstring需要转换输出
            try {
                var env = Java.vm.getEnv();
                if (!args[5].isNull()) {
                    var javaStr = env.getStringUtfChars(args[5]).readCString();
                    console.log("args[5] (as jstring):", javaStr);
                }
            } catch (e) {
                console.log("args[5] (address):", args[4]);
            }
        },
        onLeave:function (res) {
            console.log("Interceptor onLeave",res)
            try {
                var env = Java.vm.getEnv();
                if (!res.isNull()) {
                    var javaStr = env.getStringUtfChars(res).readCString();
                    console.log("res (as jstring):", javaStr);
                }
            } catch (e) {
                console.log("res (address):", res);
            }
        }
    })
})
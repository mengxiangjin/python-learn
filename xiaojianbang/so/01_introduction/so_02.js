Java.perform(function() {
    //hook任意函数  函数所在模块的基址+函数在模块的偏移量+1(arm64不需要加1)  Module.findExportByName找到的是绝对地址

    //找lib的基地址
    let module = Process.findModuleByName("libencryptlib.so")
    console.log("lib的基础",module.base)
    console.log("lib的基址:",Process.findModuleByName("libencryptlib.so").base)
    console.log("lib的基址:",Process.getModuleByName("libencryptlib.so").base)
    console.log("lib的基址:",Module.findBaseAddress("libencryptlib.so"))

    console.log("通过基址找module:",Process.findModuleByAddress(Module.findBaseAddress("libencryptlib.so")).name)
    console.log("通过基址找module:",Process.getModuleByAddress(Module.findBaseAddress("libencryptlib.so")).name)

    //绝对地址，知道函数的真正名称后
    let funcAddr = Module.findExportByName("libencryptlib.so","_ZN7MD5_CTX11MakePassMD5EPhjS0_")
    console.log("addr通过API直接找到绝对地址:",funcAddr)

    //通过ida反编译后导出表看到该函数的地址是0x1FA38（实际是偏移地址） 需要基址+偏移量
    console.log("addr提过得知函数的偏移量后加上基址",Process.findModuleByName("libencryptlib.so").base.add(0x1FA38))

    // 有手就行的so hook
    function print_arg(addr){
        var module = Process.findRangeByAddress(addr);
        if(module != null) return hexdump(addr) + "\n";
        return ptr(addr) + "\n";
    }
    function hook_native_addr(funcPtr, paramsNum){
        var module = Process.findModuleByAddress(funcPtr);
        Interceptor.attach(funcPtr, {
            onEnter: function(args){
                this.logs = [];
                this.params = [];
                this.logs.push("call " + module.name + "!" + ptr(funcPtr).sub(module.base) + "\n");
                for(let i = 0; i < paramsNum; i++){
                    this.params.push(args[i]);
                    this.logs.push("this.args" + i + " onEnter: \n" + print_arg(args[i]));
                }
            }, onLeave: function(retval){
                for(let i = 0; i < paramsNum; i++){
                    this.logs.push("this.args" + i + " onLeave: " + print_arg(this.params[i]));
                }
                this.logs.push("retval onLeave: " + print_arg(retval) + "\n");
                console.log(this.logs);
            }
        });
    }

    hook_native_addr(funcAddr, 4);

})
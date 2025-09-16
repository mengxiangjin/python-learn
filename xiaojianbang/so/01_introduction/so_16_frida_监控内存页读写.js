
function hook_dlopen(func_name,target_so_name,call_back) {
    let addr = Module.findExportByName(null,func_name)
    if (addr != null) {
        Interceptor.attach(addr,{
            onEnter:function (args) {
                var path = args[0].readCString()
                console.log('func_name onEnter',path)
                if (path.indexOf(target_so_name) !== -1) {
                    console.log("找到你了")
                    this.loadSo = true
                }

            },
            onLeave:function (retval) {
                if (this.loadSo) {
                    call_back()
                }
            }
        })
    }
}


/*
* 主要是监听异常的抛出去监控内存读写情况
* 自己手动制造异常（修改目标地址的读写权限），监听到异常产生，恢复读写权限（否则会死循环）导致闪退
* */

function hook_func() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    console.log("soAddr", soAddr);
    var target_addr = soAddr.add(0x3CFD);
    Process.setExceptionHandler(function (details) {

        //"access violation accessing 0x79ad3e3cf0"   我们修改的权限是0x3CFD为什么报错是0x79ad3e3cf0，因为报错的是内存页的首地址
        console.log("捕获到了",JSON.stringify(details,null,2))
        console.log("lr", DebugSymbol.fromAddress(details.context.lr));
        console.log("pc", DebugSymbol.fromAddress(details.context.pc));

        //console.log(Thread.backtrace(details.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');

        //恢复读写权限
        Memory.protect(target_addr,8, 'rwx');
        return true
    })
    //修改此target_addr所在的内存页权限，使其不具备读写权限
    Memory.protect(target_addr,8,'---')
}


Java.perform(function() {
    //不同机制平台打开so文件的函数名称不同 故需要同时hook dlopen与 android_dlopen_ext
    hook_dlopen("dlopen","libxiaojianbang.so",hook_func)
    hook_dlopen("android_dlopen_ext","libxiaojianbang.so",hook_func)
})
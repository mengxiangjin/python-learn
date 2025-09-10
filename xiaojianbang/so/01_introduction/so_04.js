/*
* hook dlopen加载so文件时机
*
* HookDemo.apk + libxiaojianbang.so
* */



/*
* 当加载目标target_so_name文件时，会触发call_back回调自动去监听
* 无需手动去触发某个so文件加载到内存后，然后去监听
* */
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

function hook_func() {
    var soAddr = Module.findBaseAddress("libxiaojianbang.so");
    console.log("soAddr", soAddr);
    var MD5Final = soAddr.add(0x3540);
    Interceptor.attach(MD5Final, {
        onEnter: function (args) {
            this.args1 = args[1];
        }, onLeave: function (retval) {
            console.log(hexdump(this.args1));
        }
    });
}


Java.perform(function() {
    //不同机制平台打开so文件的函数名称不同 故需要同时hook dlopen与 android_dlopen_ext
    hook_dlopen("dlopen","xiaojianbang.so",hook_func)
    hook_dlopen("android_dlopen_ext","xiaojianbang.so",hook_func)
})
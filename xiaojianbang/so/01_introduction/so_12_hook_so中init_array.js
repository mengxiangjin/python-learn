

/*  jni_onload同init_array相同
* 想要hook init_array 常规的思路是：当dlopen的时候去hook init_array
*                               1、onEnter中进行hook此时模块还并未加载，即使你知道init_array的偏移量也无法hook，不知道具体的基地址
*                               2、onLeave中进行hook，此时已经晚了，init_array已经执行完毕了
*
* 系统linker64.so文件中符号表的__dl__ZN6soinfo17call_constructorsEv方法是在dlopen与init_array之间进行，可通过此方法进行突破
*   init_array是在__dl__ZN6soinfo17call_constructorsEv被调用的,进入到__dl__ZN6soinfo17call_constructorsEv，我们去hook即可
*   __dl__ZN6soinfo17call_constructorsEv又是中dlopen中被调用的，进入到dlopen我们去hook即可
*
*
*   1、hook此方法__dl__ZN6soinfo17call_constructorsEv，onEnter之前进行hook_initArray,此时模块已经完全加载（即可得到基地址）
*   2、__dl__ZN6soinfo17call_constructorsEv是dlopen进入后进行调用的，我们可以在进入后得到具体的so文件名进行判断，如果是我们想要的so文件名，此时我们去hook
*          __dl__ZN6soinfo17call_constructorsEv（防止其他so文件的init_array执行过多干扰）
*          hook了此 __dl__ZN6soinfo17call_constructorsEv后，进入前去hook_initArray即可
*
*
*   想要hook xiaojianbang.so中的init_array
*       1、spwan启动时，开始hook  dlopen函数，onEnter中判断参数1即加载的so文件名是否与xiaojianbang.so相等
*       2、相等代表dlopen这个so文件，此时我们hook __dl__ZN6soinfo17call_constructorsEv这个函数，因为这个函数中会调用init_array,且模块的基址也加载完毕，我们hook_initarray即可
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
                    call_back()
                }

            },
            onLeave:function (retval) {

            }
        })
    }
}

function hook_constructor() {
    //__dl__ZN6soinfo17call_constructorsEv在此so中的符号表中
    let linke64_module = Process.findModuleByName("linker64")
    console.log('linke64_module',linke64_module.base)

    let symbols = linke64_module.enumerateSymbols()

    let target_address = null
    for (let i = 0; i < symbols.length; i++) {
        if (symbols[i].name.indexOf("__dl__ZN6soinfo17call_constructorsEv") !== -1) {
            console.log('找到__dl__ZN6soinfo17call_constructorsEv了',JSON.stringify(symbols[i]))
            target_address = symbols[i].address
        }
    }

    //防止多次触发
    let is_hooked = false

    if (target_address !== null) {
        Interceptor.attach(target_address,{
            onEnter:function (args) {
                if (!is_hooked) {
                    console.log("__dl__ZN6soinfo17call_constructorsEv 进来了")
                    hook_init_array()
                    hook_jni_onload()
                    is_hooked = true
                }
            },
            onLeave:function (retval) {

            }
        })
    }

}

function hook_init_array() {
    let module = Process.getModuleByName("libxiaojianbang.so")
    console.log("找到libxiaojianbang.so了---->",JSON.stringify(module))

    console.log('开始hook_init_array_了---------------------------')
    let array_one = module.base.add(0x1C54)
    let array_two = module.base.add(0x1C7C)
    let array_three = module.base.add(0x1C2C)

    Interceptor.replace(array_one,new NativeCallback(function () {
        console.log('array_one replace')
    },'void',[]))

    Interceptor.replace(array_two,new NativeCallback(function () {
        console.log('array_two replace')
    },'void',[]))

    Interceptor.replace(array_three,new NativeCallback(function () {
        console.log('array_three replace')
    },'void',[]))
    // Interceptor.attach(array_one,{
    //     onEnter: function (args) {
    //         console.log('拦截到了array_one')
    //     },
    //     onLeave: function (retval) {
    //
    //     }
    // })
}


/*
* hook-jniOnload函数中调用的创建线程的方法，打印
* */
function hook_jni_onload() {
    let module = Process.getModuleByName("libxiaojianbang.so")
    console.log("找到libxiaojianbang.so了---->",JSON.stringify(module))
    let target_addr = module.base.add(0x1CCC)
    Interceptor.replace(target_addr,new NativeCallback(function () {
        console.log('jni_onload 中pthread被替换')
    },'void',[]))
}


Java.perform(function() {
    //不同机制平台打开so文件的函数名称不同 故需要同时hook dlopen与 android_dlopen_ext
    hook_dlopen("dlopen","xiaojianbang.so", hook_constructor)
    hook_dlopen("android_dlopen_ext","xiaojianbang.so", hook_constructor)
})
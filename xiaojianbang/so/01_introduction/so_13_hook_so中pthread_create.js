
/*
* pthread_create函数在libc.so中，获取该地址直接hook即可
* 其中：   arg[0]:创建线程的ID，C语言特有的参数指针赋值最后返回
*         arg[1]:attr（一般为null），设置线程的属性
*         arg[2]:函数指针，线程的具体执行方法
*         arg[3]:一般为null
* */

function hook_pthread_create() {
    let pthread_create_addr = Module.findExportByName("libc.so","pthread_create")
    console.log('pthread_create_addrd地址：',pthread_create_addr)
    Interceptor.attach(pthread_create_addr,{
        onEnter: function (args) {
            console.log("参数0",args[0])
            console.log("参数1",args[1])
            console.log("参数2",args[2])
            console.log("参数3",args[3])

            //通过具体的线程执行逻辑获取其所在的模块，再通过其地址减去模块的基地址，即该函数中该模块中的相对地址
            let module = Process.findModuleByAddress(args[2]);
            if (module !== null) {
                console.log("线程执行所在的lib模块：",module.name)
                console.log("lib模块基础地址：",module.base)
                console.log("线程方法的地址：",args[2])
                console.log("线程执行所在的相对地址：",args[2].sub(module.base))
            }
        },
        onLeave: function (retval) {
            console.log("返回值",retval)
        }
    })

}

Java.perform(function() {
    hook_pthread_create()
})
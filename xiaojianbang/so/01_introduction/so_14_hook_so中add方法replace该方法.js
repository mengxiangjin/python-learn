


/*
* replace中调用原函数获取结果，类似于Java层的Hook一般
*
* */
function hook_add() {
    let module = Process.findModuleByName("libxiaojianbang.so")
    console.log('module：',JSON.stringify(module))
    let add_address = module.base.add(0x1A0C)

    let add_func = new NativeFunction(add_address,'int',['pointer','pointer','int','int','int'])

    Interceptor.replace(add_address,new NativeCallback(function (a,b,c,d,e) {
        console.log("c:",c)
        console.log("d:",d)
        console.log("e:",e)
        console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
        let res = add_func(a,b,c,d,e)
        console.log("调用原函数返回结果：",res)
        return 10
    },'int',['pointer','pointer','int','int','int']))

}

Java.perform(function() {
    hook_add()
})
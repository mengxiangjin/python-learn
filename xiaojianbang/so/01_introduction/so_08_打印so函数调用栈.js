

/*
* 想要hook_NewStringUTF函数,需要得知此函数地址
*   1、枚举符号表去获取地址,进行hook 可能存在多个,所以在循环中进行hook
*   2、自己手动去计算地址,NewStringUTF是在JNIEnv* 结构体中,我们可以通过getEnv拿到其基础地址,再查看NewStringUTF在此结构体中的偏移量即可获取到准确地址
*
*   //打印so函数调用栈
*   console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');

* */
function hook_newStringUtf() {
    //枚举NewStringUTF函数所在的so文件中的符号表,去拿到地址hook
    var symbols = Process.findModuleByName("libart.so").enumerateSymbols();
    for (let i = 0; i < symbols.length; i++) {
        if (symbols[i].name.indexOf("NewStringUTF") !== -1 && symbols[i].name.indexOf("CheckJNI") == -1) {
            console.log(JSON.stringify(symbols[i]))
            Interceptor.attach(symbols[i].address,{
                onEnter: function(args ) {
                    console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');

                    console.log("NewStringUTF onEnter ",JSON.stringify(symbols[i]))
                    console.log("NewStringUTF onEnter ",args[1].readCString())
                },
                onLeave: function (retval) {
                    console.log("newStringUtf onLeave", retval);
                }
            })
        }
    }
}


Java.perform(function() {

})
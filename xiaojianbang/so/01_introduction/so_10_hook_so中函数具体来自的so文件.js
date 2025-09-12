

/*
void* dlsym(void* handle, const char* symbol); 在动态库中查找符号的地址 (静态注册的函数)
当 Java 调用 native 方法时，Android 系统会：
    通过 dlsym 查找对应的 native 函数
    如果找到，将函数地址缓存起来
    后续直接调用该地址
* */
function hook_dlsym() {
    var dlsym_addr = Module.findExportByName("libdl.so", "dlsym");
    console.log(dlsym_addr)

    Interceptor.attach(dlsym_addr,{
        onEnter:function (args) {
            this.symbol = args[1]
        },
        onLeave:function (retval) {
            console.log("onLeave--->",this.symbol.readCString())
        }
    })
}

/*
* 对于动态注册的函数：
    jclass clazz = env->FindClass("com/jin/jni/MainActivity");
    JNINativeMethod methods[] = {
        {"stringFromJNIWithDynamic1", "(Ljava/lang/String;)Ljava/lang/String;",
            (void *)(realFunc1)
        },
        {
        "stringFromJNIWithDynamic2","(Ljava/lang/String;I)I",(void *)(realFunc2)
        }
    };
    env->RegisterNatives(clazz,methods,2);
    *
*   jint  (*RegisterNatives)(JNIEnv*, jclass, const JNINativeMethod*,
                        jint);
* */
function hook_RegisterNatives() {
    //找到RegisterNatives的地址
    var registerNatives_addr = null
    let symbols = Process.findModuleByName("libart.so").enumerateSymbols()
    for (let i = 0; i < symbols.length; i++) {
        if (symbols[i].name.indexOf("RegisterNatives") !== -1 && symbols[i].name.indexOf("CheckJNI") === -1) {
            console.log(JSON.stringify(symbols[i]))
            registerNatives_addr = symbols[i].address
        }
    }
    console.log(registerNatives_addr)

    Interceptor.attach(registerNatives_addr,{
        onEnter: function (args) {
            this.clazz = args[1]  //jclass类型
            this.native_method = args[2] //JNINativeMethod数组
            this.meth_count = args[3].toInt32()
            console.log("RegisterNatives 被调用");
            console.log("jclass:", this.clazz);
            console.log("JNINativeMethod 数组:", this.native_method);
            console.log("方法数量:", this.meth_count);

            // 将 jclass 转换为 Java 的 Class 对象
            var className = Java.vm.tryGetEnv().getClassName(args[1]);
            console.log("className:",className)

            for (let i = 0; i < this.meth_count; i++) {
                var offset_addr = 3 * Process.pointerSize * i
                var methodName = this.native_method.add(offset_addr).readPointer().readCString()
                var signature = this.native_method.add(offset_addr + Process.pointerSize).readPointer().readCString()
                var fnptr = this.native_method.add(offset_addr + Process.pointerSize * 2).readPointer()
                var module = Process.findModuleByAddress(fnptr)
                console.log("methodName",methodName)
                console.log("signature",signature)
                console.log("module",module.name)
                console.log("偏移量",fnptr.sub(module.base))
            }
        },
        onLeave: function (retval) {

        }
    })
}


Java.perform(function() {

})
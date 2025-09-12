


/*
* 想要hook_NewStringUTF函数,需要得知此函数地址
*   1、枚举符号表去获取地址,进行hook 可能存在多个,所以在循环中进行hook
*   2、自己手动去计算地址,NewStringUTF是在JNIEnv* 结构体中,我们可以通过getEnv拿到其基础地址,再查看NewStringUTF在此结构体中的偏移量即可获取到准确地址
* */
function hook_newStringUtf() {
    //枚举NewStringUTF函数所在的so文件中的符号表,去拿到地址hook
    var symbols = Process.findModuleByName("libart.so").enumerateSymbols();
    for (let i = 0; i < symbols.length; i++) {
        if (symbols[i].name.indexOf("NewStringUTF") !== -1 && symbols[i].name.indexOf("CheckJNI") == -1) {
            console.log(JSON.stringify(symbols[i]))
            Interceptor.attach(symbols[i].address,{
                onEnter: function(args ) {
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


/*
* 手动计算出FindClass函数在JNINativeInterface即JNIEnv* 偏移48个字节
* 8 * 6 = 48
*   struct JNINativeInterface {
    void*       reserved0; /
    void*       reserved1;
    void*       reserved2;
    void*       reserved3;

    jint        (*GetVersion)(JNIEnv *);

    jclass      (*DefineClass)(JNIEnv*, const char*, jobject, const jbyte*,
                        jsize);
    jclass      (*FindClass)(JNIEnv*, const char*);
    *
    env.handle.readPointer().add(48)得到此函数需要再次readPointer()得到其真正的函数代码
* */
function hook_FindClass() {
    //枚举NewStringUTF函数所在的so文件中的符号表,去拿到地址hook
    var env = Java.vm.tryGetEnv();
    console.log(hexdump(env.handle))
    console.log(hexdump(env.handle.readPointer()))

    Interceptor.attach(env.handle.readPointer().add(48).readPointer(),{
        onEnter: function(args ) {
           console.log("hook_FindClass onEnter ",args[1].readCString())
        },
        onLeave: function (retval) {
            console.log("hook_FindClass onLeave", retval);
        }
    })
}




Java.perform(function() {

})
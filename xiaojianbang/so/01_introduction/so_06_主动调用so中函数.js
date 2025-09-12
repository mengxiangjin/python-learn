
/*
* 主动调用so中的jstring2cstr方法
* 创建NativeFunction对象
*   1、方法的地址
*   2、方法的返回值（char*） ---> pointer
*   3、方法的参数（JNIEnv*，JString*） ----> [pointer,pointer]
*
*  支持的：void、pointer、int、uint、long、ulong、char、uchar、float、double
*        int8、uint8、int16、uint16、int32、uint32、int64、uint64、bool
*        size_t、ssize_t
* */
function call_jstring2cstr() {
    var module = Process.findModuleByName("libxiaojianbang.so");
    var jstring2cstr_addr = module.base.add(0x124C)
    var function_pointer = new NativeFunction(jstring2cstr_addr,"pointer",["pointer","pointer"])

    var env = Java.vm.tryGetEnv();
    var jstring = env.newStringUtf("xiaojianbangaaa");
    var retval = function_pointer(env.handle, jstring);
    console.log(retval.readCString());
}

/*
* 坑:需要正确关闭文件,才能将内容写入,注意权限问题
*  对于char* 字符串,我们可以通过 Memory.allocUtf8String去构造
*  对应jstring字符串,我们可以通过env.newStingUtf()去构造
* */
function call_write_file() {
    var fopenAddr = Module.findExportByName("libc.so","fopen")
    var fputsAddr = Module.findExportByName("libc.so","fputs")
    var fcloseAddr = Module.findExportByName("libc.so","fclose")
    console.log(fopenAddr, fputsAddr, fcloseAddr);

    var fopen = new NativeFunction(fopenAddr,"pointer",["pointer","pointer"])
    var fclose = new NativeFunction(fcloseAddr, 'int', ['pointer']);
    var fputs = new NativeFunction(fputsAddr, 'int', ['pointer', 'pointer']);
    var fileName = Memory.allocUtf8String("/data/data/com.xiaojianbang.app/xiaojianbang.txt")
    //打开创建该文件
    var openMode = Memory.allocUtf8String("w")

    var data = Memory.allocUtf8String("xxxxxxaaa\n");
    var file = fopen(fileName, openMode);
    fputs(data, file);
    fclose(file);
}



/*
* 找到NewStringUT函数的地址，主动调用函数，返回jstring
* 利用print_jstring方法打印jstring
* */
function call() {
     var symbols = Process.findModuleByName("libart.so").enumerateSymbols();
     var address_list = []
     for (let i = 0; i < symbols.length; i++) {
         if (symbols[i].name.indexOf("NewStringUTF") !== -1 && symbols[i].name.indexOf("CheckJNI") == -1) {
             console.log(JSON.stringify(symbols[i]))
             address_list.push(symbols[i].address)
         }
     }
    let str = Memory.allocUtf8String("zsydcsyl")

    for (let i = 0; i < address_list.length; i++) {
        let env = Java.vm.tryGetEnv()
        let newStringUtf_func = new NativeFunction(address_list[i],"pointer",["pointer","pointer"])

        let jstring = newStringUtf_func(env.handle,str)
        print_jstring(jstring)
    }

}


/*
* 手动计算GetStringUTFChars的偏移量得到其地址，（大多数通过枚举进行查找即可）
* 调用GetStringUTFChars函数得到char* 最后readCString即可
* */
function print_jstring(params) {
    console.log(params)
    let env = Java.vm.tryGetEnv()
    let getStringUtfChars_addr = env.handle.readPointer().add(0x548).readPointer()
    let getStringUtfChars_func = new NativeFunction(getStringUtfChars_addr,"pointer",["pointer","pointer","pointer"])
    let c_str_res = getStringUtfChars_func(env.handle,params,ptr(0))
    console.log(c_str_res.readCString())
}




Java.perform(function() {

})
/*
    ida中无法正确反编译的字符串
    //  v4 = (*(int (__fastcall **)(int *, char *))(*v3 + 24))(v3, asc_D060);  asc_D060值并未反编译出来
    1、可以拿到其地址，进行hexdump打印出即可，每个都需要进行手动打印过于繁琐
    2、使用jtrace，只能打印JNI系统类的函数有局限
    3、so文件加载到内存后，dump下来so再拖到ida中进行分析（需要dump以及可能还需要还原so）推荐
        1、运行dump_so函数传入需要打印的so文件名称，（前提是该so已经加载到内存）
        2、dump_so后将dump下来的so文件移动到公共目录下（便于复制相关）
        3、将dump_so移动到电脑上，（此时拖入IDA中可能会报错）
        4、准备进行so文件修复，根据类型的选择执行不同的SoFixer（x64与x32）
        4、cmd下执行命令
            sofixer -s orig.so -o fix.so -m 0x0 -d
            -s 待修复的so路径
            -o 修复后的so路径
            -m 內存dump的基地址(16位) 原dump_so的基地址0xb4a4b000
            -d 输出debug信息
        5、将修复好的so文件拖入即可进行正常分析
    4、手动分析代码然后进行还原函数
*/



//dump内存下的so文件
function dump_so(so_name) {
    Java.perform(function () {
        var currentApplication = Java.use("android.app.ActivityThread").currentApplication();
        var dir = currentApplication.getApplicationContext().getFilesDir().getPath();
        var libso = Process.getModuleByName(so_name);
        console.log("[name]:", libso.name);
        console.log("[base]:", libso.base);
        console.log("[size]:", ptr(libso.size));
        console.log("[path]:", libso.path);
        var file_path = dir + "/" + libso.name + "_" + libso.base + "_" + ptr(libso.size) + ".so";
        var file_handle = new File(file_path, "wb");
        if (file_handle && file_handle != null) {
            Memory.protect(ptr(libso.base), libso.size, 'rwx');
            var libso_buffer = ptr(libso.base).readByteArray(libso.size);
            file_handle.write(libso_buffer);
            file_handle.flush();
            file_handle.close();
            console.log("[dump]:", file_path);
        }
    });
}


Java.perform(function() {
    let address = Module.findBaseAddress("liblogin_encrypt.so")
    console.log("base address",address)
    let str1_address = address.add(0xD055)
    console.log(hexdump(str1_address,{
                offset:0,
                length:Memory.readUtf8String(str1_address).length,
                header:true,
                ansi:true
            }))
    console.log(hexdump(address.add(0xD060),{
                offset:0,
                length:Memory.readUtf8String(address.add(0xD060)).length,
                header:true,
                ansi:true
            }))

})


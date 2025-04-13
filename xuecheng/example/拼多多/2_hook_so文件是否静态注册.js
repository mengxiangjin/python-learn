Java.perform(function () {
    var dlsymadd = Module.findExportByName("libdl.so", 'dlsym');
    Interceptor.attach(dlsymadd, {
        onEnter: function (args) {
            this.info = args[1];

        }, onLeave: function (retval) {
            //那个so文件 module.name
            var module = Process.findModuleByAddress(retval);
            if (module == null) {
                return retval;
            }
            // native方法
            var funcName = this.info.readCString();
            if (funcName.indexOf("getHNASignature") !== -1) {
                console.log(module.name);
                console.log('\t', funcName);
            }
            return retval;
        }
    })
});

// Application(identifier="com.xunmeng.pinduoduo", name="拼多多", pid=9149, parameters={})
// frida -U -f  com.xunmeng.pinduoduo  -l 2_hook_so文件是否静态注册
//无输出 非静态注册

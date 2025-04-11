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

// Application(identifier="com.rytong.hnair", name="海南航空", pid=14958, parameters={})
// frida -U -f  com.rytong.hnair  -l static_find_so.js

// [Pixel 2 XL::com.rytong.hnair ]-> libsignature.so
//          Java_com_rytong_hnair_HNASignature_getHNASignature

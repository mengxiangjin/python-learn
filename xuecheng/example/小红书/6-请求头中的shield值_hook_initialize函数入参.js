function do_hook() {
    setTimeout(function () {
        Java.perform(function () {
            var XhsHttpInterceptor = Java.use('com.xingin.shield.http.XhsHttpInterceptor');
            XhsHttpInterceptor.initialize.implementation = function (str) {
                console.log("str=", str);
                return this.initialize(str);
            };
        })
    }, 10);


}

function load_so_and_hook() {
    // 加载某个so文件   dlopen("xxxx/xxxx.so") -> 函数执行完毕 -> Hook
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            // console.log("[dlopen:]", path);
            this.path = path;
        }, 
        onLeave: function (retval) {
            if (this.path.indexOf("libshield.so") !== -1) {
                console.log("[dlopen:]", this.path);
                do_hook();
            }
        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();

            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf("libshield.so") !== -1) {
                console.log("\nandroid_dlopen_ext加载：", this.path);
                do_hook();

            }
        }
    });
}

load_so_and_hook();

// frida -U -f com.xingin.xhs  -l 9.initValue.js
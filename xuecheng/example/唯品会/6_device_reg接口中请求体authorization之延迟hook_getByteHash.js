function do_hook() {
	setTimeout(function(){
        var addr = Module.findExportByName("libkeyinfo.so", "getByteHash");
        console.log(addr); //0xb696387d


        Interceptor.attach(addr, {
            onEnter: function (args) {
                this.x1 = args[2];
            },
            onLeave: function (retval) {
                console.log("--------------------")
                console.log(Memory.readCString(this.x1));
                console.log(Memory.readCString(retval));
            }
        })
     },10);

}

function load_so_and_hook() {
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            // console.log("[dlopen:]", path);
            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf("libkeyinfo.so") !== -1) {
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
            if (this.path.indexOf("libkeyinfo.so") !== -1) {
                console.log("\nandroid_dlopen_ext加载：", this.path);
                do_hook();

            }
        }
    });
}

load_so_and_hook();

// frida -U -f com.achievo.vipshop -l hook05.js

// --------------------
// aee4c425dbb2288b80c71347cc37d04b  app_name=achievo_ad&app_version=7.83.3&channel=oziq7dxw:::&device=Pixel 2 XL&device_token=1f3fb32d-9f6a-3cb8-86d2
// -4c8dc359650b&manufacturer=Google&os_version=30&regPlat=0&regid=null&rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)&skey=6692c461c3810ab150c9a980d0c275ec&status=1&vipruid=&warehouse=null
// 0be9fdb3f706c016fa6a13edfe8ff81af9e57b57

// --------------------
// aee4c425dbb2288b80c71347cc37d04b  0be9fdb3f706c016fa6a13edfe8ff81af9e57b57
// 4723dd6cb5ece0183ad7ec8cd45d251db4b72ec2

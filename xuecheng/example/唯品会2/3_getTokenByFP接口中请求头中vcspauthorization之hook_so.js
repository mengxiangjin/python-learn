function do_hook() {

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

// frida -U -f com.achievo.vipshop -l delay_hook.js
// da19a1b93059ff3609fc1ed2e04b0141vcspKey=4d9e524ad536c03ff203787cf0dfcd29
// 5a7c831821536f5a9d5244b99af681226dc8a277
// --------------------
// da19a1b93059ff3609fc1ed2e04b01415a7c831821536f5a9d5244b99af681226dc8a277
// 05a68135d2bfd322e3a22f95bbc25a24c777f387


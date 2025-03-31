### hook运行了那些so
import frida
import sys

rdev = frida.get_remote_device()
pid = rdev.spawn(["com.achievo.vipshop"])
session = rdev.attach(pid)

scr = """
Java.perform(function () {

    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            console.log("[dlopen:]", path);
        },
        onLeave: function (retval) {

        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            console.log("[dlopen_ext:]", path);
        },
        onLeave: function (retval) {

        }
    });


});
"""
script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
rdev.resume(pid)


# 删除此so文件导致的闪退
#
# C:\Users\hh\AppData\Local\Programs\Python\Python312\python.exe D:\life\python-learn\xuecheng\example\唯品会\3_device_reg接口中请求参数seky之hook闪退so文件打印.py
# [dlopen_ext:] /data/app/~~NZtzLabxDWCxgqKuQXVVcQ==/com.achievo.vipshop-uNFWzhMCkvM1-jMixQf3-Q==/lib/arm/libkeyinfo.so
# [dlopen_ext:] /data/app/~~NZtzLabxDWCxgqKuQXVVcQ==/com.achievo.vipshop-uNFWzhMCkvM1-jMixQf3-Q==/lib/arm/libxcrash.so
# [dlopen_ext:] /vendor/lib/hw/gralloc.msm8998.so
# [dlopen:] libadreno_utils.so
# [dlopen_ext:] /data/app/~~NZtzLabxDWCxgqKuQXVVcQ==/com.achievo.vipshop-uNFWzhMCkvM1-jMixQf3-Q==/lib/arm/libmsaoaidsec.so
# [dlopen:] libEGL_adreno.so

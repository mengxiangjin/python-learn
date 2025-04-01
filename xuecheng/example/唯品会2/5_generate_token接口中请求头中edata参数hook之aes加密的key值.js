
//hook几次发现 aes的key都为:cdd17ab29b84b32552ddcfbb4abf0225
function java_hook() {
    Java.perform(function () {
        var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");

        KeyInfo.esNav.implementation = function (ctx, str, str2, str3, i10) {
            console.log("-----------------gsNav-----------------");
            console.log("开始================>", str);
            var res = this.esNav(ctx, str, str2, str3, i10); // 一定会执行 getMD516 和 java的 SecretKeySpec
            console.log("结束================>", res);
            return res;
        }

        var SecretKeySpec = Java.use("javax.crypto.spec.SecretKeySpec");
        var ByteString = Java.use("com.android.okhttp.okio.ByteString");
        SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function (key, name) {
            if (name === 'AES') {
                console.log("-----------------------SecretKeySpec---------------------------");
                //console.log("4.key bytes=", JSON.stringify(key));
                console.log("java key hex =", ByteString.of(key).hex());
                //console.log("4.key", ByteString.of(key).utf8());
            }
            var res = this.$init(key, name);
            return res;
        }
    });

}

function delay_hook(so_name, hook_func) {
    var dlopen = Module.findExportByName(null, "dlopen");
    var android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");

    Interceptor.attach(dlopen, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            // console.log("[dlopen:]", path);
            this.path = path;
        }, onLeave: function (retval) {
            if (this.path.indexOf(so_name) !== -1) {
                console.log("[dlopen:]", this.path);
                hook_func();
            }
        }
    });

    Interceptor.attach(android_dlopen_ext, {
        onEnter: function (args) {
            var path_ptr = args[0];
            var path = ptr(path_ptr).readCString();
            this.path = path;
        },
        onLeave: function (retval) {
            if (this.path.indexOf(so_name) !== -1) {
                console.log("\nandroid_dlopen_ext加载：", this.path);
                hook_func();
            }
        }
    });
}

function so_hook() {
    var getMD516 = Module.findExportByName("libkeyinfo.so", "getMD516");
    console.log('getMD516 addr = ', getMD516);

    if (getMD516) {
        Interceptor.attach(getMD516, {
            onEnter: function (args) {
                console.log('getMD5参数：', hexdump(args[1], {length: args[2].toInt32()}), "\n");
                // console.log('2.getMD5 参数：', hexdump(args[1]), "\n");
            },
            onLeave: function (retval) {
                // console.log('3.getMD5 返回值：', hexdump(retval), "\n");
                console.log('getMD5=key 返回值：', hexdump(retval, {length: 16}), "\n");
            }
        });
    }
}

delay_hook("libkeyinfo.so", so_hook)
java_hook()

//frida -U -f  com.achievo.vipshop -l  5_generate_token接口中请求头中edata参数hook之aes加密的key值


// getMD516 addr =  0xb2a68605
// -----------------------SecretKeySpec---------------------------
// java key hex = bf8360269ccd8a0f185ae6275d096f3f
// -----------------------SecretKeySpec---------------------------
// java key hex = 3766653934653738663962383361373633653263636632633361656261366131
// -----------------gsNav-----------------
// 开始================> app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3
// A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pi
// xel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2
// C%22as3%22%3A%22%22%2C%22as4%22%3A%223a48d6bacc328464%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%221f3fb3
// 2d-9f6a-3cb8-86d2-4c8dc359650b%22%7D&mars_cid=1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b&phone_model=Pixel+2+XL&session_id=1f3fb32d-9f6a-3cb8-86d2-4c8d
// c359650b_shop_android_1743489113272&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzQ2MDgxMDkyfHx8.95db3654557f0d6bd5c4701f621b6fb4
// getMD5参数：            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
// ac8a9e50  61 65 65 34 63 34 32 35 64 62 62 32 32 38 38 62  aee4c425dbb2288b
// ac8a9e60  38 30 63 37 31 33 34 37 63 63 33 37 64 30 34 62  80c71347cc37d04b
//
// getMD5=key 返回值：            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
// ac8a9dd8  cd d1 7a b2 9b 84 b3 25 52 dd cf bb 4a bf 02 25  ..z....%R...J..%
//
// -----------------------SecretKeySpec---------------------------
// java key hex = cdd17ab29b84b32552ddcfbb4abf0225
// 结束================> MDExNWJiOGJkNGUwNjQ4Mn8GbKd/QGESAfsLRETPE49dVuzvgVSQ8Dn2pDIcSM7hfdtfJhr5apwKRmJrwf+4ycF84whpLsfeCOLovo8TC93p+tOYzbBR0j8uGlM
// epXxVXNGdjuARmVL26PML9AaKqSBuM6C1agLF3SedISIKp0ixIimkC2oap9/Dz1nfwZOSN5Xm4BQHs9TEaLL9zVe5qKWq+aK206afHhRd7eyrE1NV6iQ4FXukjF5ldf4+oA9qynuU3pPwC9Gt
// JDjK4lGY4RNdlGb0Re+VScwAVkZjGBmylCLg5BZw1ZEkjNpHjqhe3IvnnaLtiPdmHOlXEshYj1jZN3Dvw2z5aEZ83khfnO3UA/NXa7wIUdqntjxaxUJT/ocatOhE3qF5NcHlfgs5bQIIJl+PQ
// V6aJThuQcTAKLA9OGrvdQLXGd87kd+XrFUJq68YEz7fLHP2vrln2+lhl6N1ABVVX4C+1JwJ1ijb1Ic2h/FK+stwkQJtZmoJKsll7gumrCAqK6vZGXCUzupVzA2/p+fONOFsX55NQdmd4ARFeC
// lRXnH2ZM2K0kMFoKSP0AMpID9zdVfJtbrj0hZMPqzdc0BsR9R7DM2oLlvqrrFCMt443gnvyrwQVjlO3JOfuIc6iBf9Ih56QCxi0Tm3OGKZbYlC6jvysIIHx7ahBgf/7AmUBrE1rP5tK6qZizS
// Unx6S+7k/uK9Uo3lnEBxL4AhItcKHwUH46PlVmX+n6N3jcB4mQIO3dLIghd1EzoZ4sBFWSrAvHvTNYUTjpqRkuyCVNGIjAyZRFhVaEiF9N6IjPKvsQyThSZbV0KQcKvUCnZUGClyeGADJgnxU
// ITptOODte2m9qYBBexFMhFATA2gFHvJSSz0933ZsTZUBOKiGPP9hQWV7JjmWoogv6mj53aqdPeHJ/Ca1CROyWY2SN7aepTMiSrEpxgB+pnAbAedcd6AwWellk4egIvY0R0AWC3G0y0ATBI97e
// 228nKTRjFdEtppkk5SUbdDufv5Kgk6HJzLXjAlns7ObMmYU3pa0QNBZGLI233JWpeK7cK0KZLFcVPNqMmxWCwI0UJwFJvzT+hsZblAr8grIjowokBucDthdVnWkt+MrjHCamBujqWRquMMGn8l2a+2P4qjjJ8r1BtZe05Rp5dNDExjesErD2o3Hmvi02AziS3h4dFWcAfCXIC6PLy5sQNiTPz7D+QuvDe5mdJTQAEdZEv/vkRSVKA==

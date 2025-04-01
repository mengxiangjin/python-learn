// hook  KeyInfo的esNav---》内部执行了rand16Str---》又执行了java的IvParameterSpec
function java_hook() {
    Java.perform(function () {
        var KeyInfo = Java.use("com.vip.vcsp.KeyInfo");
        KeyInfo.esNav.implementation = function (ctx, str, str2, str3, i10) {
            console.log("开始================>", str);
            var res = this.esNav(ctx, str, str2, str3, i10);  // 一定会执行 rand16Str  和 IvParameterSpec 的构造方法
            console.log("结束================>", res);
            return res;
        }

        var IvParameterSpec = Java.use("javax.crypto.spec.IvParameterSpec");
        var ByteString = Java.use("com.android.okhttp.okio.ByteString");
        IvParameterSpec.$init.overload('[B').implementation = function (iv) {
            console.log("-----------------------IvParameterSpec---------------------------");
            //console.log("iv str=", ByteString.of(iv).utf8());
            console.log("java iv hex=", ByteString.of(iv).hex());
            //console.log("iv byte", JSON.stringify(iv));
            var res = this.$init(iv);
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
    var rand16Str = Module.findExportByName("libkeyinfo.so", "rand16Str");
    console.log('rand16Str addr = ', rand16Str);
    if (rand16Str) {
        Interceptor.attach(rand16Str, {
            onEnter: function (args) {
                this.x1 = args[0]
            },
            onLeave: function (retval) {
                // console.log('5.rand16Str 返回值：', hexdump(this.x1), "\n");
                console.log('so rand16Str=iv 返回值：', hexdump(this.x1, {length: 16}), "\n");
            }
        });
    }
}

delay_hook("libkeyinfo.so", so_hook)
java_hook()

//frida -U -f  com.achievo.vipshop -l  5-hook-esNav-IvParameterSpec构造方法-rand16Str.js

// 开始================> app_name=shop_android&app_version=7.83.3&client_type=android&dinfo=%7B%22ah1%22%3A%22%22%2C%22ah2%22%3A%22%22%2C%22ah3%22%3
// A%22%22%2C%22ah4%22%3A%22wifi%22%2C%22ah5%22%3A%221440_2712%22%2C%22ah6%22%3A1900800%2C%22ah7%22%3A8%2C%22ah8%22%3A3839954944%2C%22ah9%22%3A%22Pi
// xel+2+XL%22%2C%22ah10%22%3A%22%22%2C%22ah11%22%3A%22%22%2C%22ah12%22%3A%22%22%2C%22ah13%22%3A%22%22%2C%22as1%22%3A%2211%22%2C%22as2%22%3A%22%22%2
// C%22as3%22%3A%22%22%2C%22as4%22%3A%223a48d6bacc328464%22%2C%22as5%22%3A%22%22%2C%22as6%22%3A%22%22%2C%22as7%22%3A%2230%22%2C%22ac1%22%3A%221f3fb3
// 2d-9f6a-3cb8-86d2-4c8dc359650b%22%7D&mars_cid=1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b&phone_model=Pixel+2+XL&session_id=1f3fb32d-9f6a-3cb8-86d2-4c8d
// c359650b_shop_android_1743498686267&sys_version=30&vcspKey=4d9e524ad536c03ff203787cf0dfcd29&vcspToken=NGQ5ZTUyNGFkNTM2YzAzZmYyMDM3ODdjZjBkZmNkMjl8fHwxNzQ2MDkwNjY0fHx8.86468a170aaa365719d73f294187e176
// so rand16Str=iv 返回值：            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
// b9eeddb8  31 37 35 30 33 39 34 64 64 62 33 61 65 33 35 35  1750394ddb3ae355
//
// -----------------------IvParameterSpec---------------------------
// java iv hex= 31373530333934646462336165333535
// 结束================> MTc1MDM5NGRkYjNhZTM1NRu/+32aui+3Y8OTFu0rbyCsk25IFm6Q4JrZbp21UoQ8+SryauWDKDVkjflD59sTSW4G/pkaH6ZnXwLOcvZGK5NzP1uD4E+wzDOkw5t
// mRnhpOnCsUkNNZ4bjEV7xx1SsApps2FTMBrFyighVB8LNmmvX//KcpYJZIyz4kSIWWxYVT7f0g8K0xt94zLzAV+6TxCNxM8s4lZvSg/d+0bIVWSFJj2Y7hUjs9+AiiGTTDNdTlloKr9jaq56G
// ItqPW3ee+NxNuavXAkJnIIpYxR53atTQA/NfYGWOS7r9joo/yytMJm5oSMqu8FTSx001MsgU5vZDjblTOBGyuD4RhTirr59aNk2rv49S1WRRu609+uUIL7Vkxb80kEwIeg/cZCF/iXptaDD+z
// mp1FyLcAPse88HII1zKcMNOGHzW1ewU3PwmLv05D8DWGTnMsQZ6svKY+529NZG6iGtSNuLRmTYIJz4FNP7BJ4wRx3ndr6hCMAQobEU0URafbi5x3/rrL/4prygSarkg97EUdz9xz4nrEoUjbK
// aLlxUb2oJuA58m4SdoYEA/jthKM5OYzKbPhAcOKo4VpveSuRFboHjSxovKneXB5euxuZFFmhV89w1nJzE/XfiwG3M/tvF6oDDfJgqiI1rcyclcavu22Jm+oeYRrK8EmCK9/PUVSpPrdz+XNrE
// frUADkDex4tgat6dcc8r5bTue3EvDDrBv7t/gMwXW5D7pnG9QnHhmk3QkbFuVxAhDFwM3UWKwyeUJoTUP67PmnZL4j5VunnMpL3V42aRfj6CFea39XA4E53J5Ys9zTSCXG0R7uwqPaMVHXQBi
// DPZUx/r5/pqwh0O2IUIR/8iQ9CU/PK1Vq1oTQ8077lJZUTp1Z0lHCl/914B9YtT8nE73Hzwl6ATIUD3iLbgfwFl2Izf7gF3+ae6PE+7FTSfn13+xtyzcym6viEYk5Io2Q79yBF9xfFDDxQyzA
// 6whjboToOlV9fOAKxmVvQe/JHtLDK//8j0H/Fy35HpY42Oy3qrVhpPo5EmvnR9GHB1c4XI2pRTqBOXNOgFn7q92DXIRi0dIZglI6h+ewEqnMESXgLjnaHRA7zzTZBgK7sQhUOICWwDweWZtWh5Xtg5yBRT+ZGnbSsv18py7POb071xlG5iyvnQW+ZL0OI0zAmXAl3hqgqCWe95Yw/CXi3RwLFyV24qNw0NiXMc+rD4sZ5PX34K3RA==

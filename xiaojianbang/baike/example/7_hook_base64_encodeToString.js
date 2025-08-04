Java.perform(function() {
    var Base64 = Java.use("android.util.Base64");
    Base64.encodeToString.overload('[B','int').implementation = function (bytes,flag) {
        console.log('Base64.encodeToString',bytes.toString())
        console.log('Base64.encodeToString',flag)
        var res = this.encodeToString(bytes,flag);
        console.log('result',res)
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        return res
    }
})
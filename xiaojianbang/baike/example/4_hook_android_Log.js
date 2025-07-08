Java.perform(function() {
    var Log = Java.use("android.util.Log");
    Log.w.overload('java.lang.String', 'java.lang.String').implementation = function (a,b) {
        console.log("Log.w:a", a);
        console.log("Log.w:b ", b);
        return this.w(a,b);
    }
})
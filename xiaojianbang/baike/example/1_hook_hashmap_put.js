Java.perform(function() {
    var hashMap = Java.use("java.util.HashMap");
    hashMap.put.implementation = function (a, b) {
        if(a.equals("username")){
            console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
            console.log("hashMap.put: ", a, b);
        }
        return this.put(a, b);
    }
})
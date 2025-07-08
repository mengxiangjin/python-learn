Java.perform(function() {
    var ArrayList = Java.use("java.util.ArrayList");
    ArrayList.add.overload('java.lang.Object').implementation = function (a) {
        if(a.equals("username=18256027302")){
            console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
            console.log("arrayList.add: ", a);
        }
        return this.add(a);
    }

    ArrayList.add.overload('int', 'java.lang.Object').implementation = function (a, b) {
        console.log("arrayList.add: ", a, b);
        return this.add(a, b);
    }
})
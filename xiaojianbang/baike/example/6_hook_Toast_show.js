Java.perform(function() {
    var Toast = Java.use("android.widget.Toast");
    Toast.show.implementation = function () {
        console.log("show: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        this.show();
    }
})
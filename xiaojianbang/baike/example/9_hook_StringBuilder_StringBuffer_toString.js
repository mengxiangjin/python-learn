Java.perform(function() {
    var StringBuilder = Java.use("java.lang.StringBuilder");
    StringBuilder.toString.implementation = function () {
        var res = this.toString()
        console.log('StringBuilder toString',res)
        return res;
    }

    var StringBuffer = Java.use("java.lang.StringBuffer");
    StringBuffer.toString.implementation = function () {
        var res = this.toString()
        console.log('StringBuffer toString',res)
        return res;
    }
})
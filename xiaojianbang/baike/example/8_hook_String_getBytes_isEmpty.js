Java.perform(function() {
    var String = Java.use("java.lang.String");
    String.getBytes.overload().implementation = function (bytes,flag) {
        console.log('getBytes')
        return this.getBytes();
    }

    String.getBytes.overload('java.lang.String').implementation = function (charsetName) {
        console.log('getBytes',charsetName)
        return this.getBytes(charsetName);
    }
})
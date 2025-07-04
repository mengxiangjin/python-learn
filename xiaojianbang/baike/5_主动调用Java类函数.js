Java.perform(function() {
    var DESKeySpec = Java.use('javax.crypto.spec.DESKeySpec')

    var Base64 = Java.use('java.util.Base64')

    DESKeySpec.$init.overload('[B').implementation = function (byteArray) {
        console.log('$init:',byteArray)
        var res = Base64.getEncoder().encodeToString(byteArray)
        console.log('$init:res',res)
        this.$init(byteArray)
    }
})
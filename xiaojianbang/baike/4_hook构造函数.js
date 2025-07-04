Java.perform(function() {
    var DESKeySpec = Java.use('javax.crypto.spec.DESKeySpec')

    DESKeySpec.$init.overload('[B').implementation = function (byteArray) {
        console.log('$init:',byteArray)
        this.$init(byteArray)
    }
})
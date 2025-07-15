Java.perform(function() {
    var net = Java.use('java.net.NetworkInterface')
    net.getName.implementation = function () {
        let res = this.getName()
        console.log(res)
        if (res === 'tun0') {
            return ''
        }
        return res
    }

    var toast = Java.use('android.widget.Toast')
    toast.show.implementation = function () {
        console.log('show')
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        this.show()
    }
})
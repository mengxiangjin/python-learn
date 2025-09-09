Java.perform(function() {

    var LoginEncryptUtil = Java.use('com.ximalaya.ting.android.loginservice.LoginEncryptUtil')

    LoginEncryptUtil.AQqfJzIZgx.implementation = function(a,b,c) {
        console.log('params2',b)
        console.log('params3',c)
        var res = this.AQqfJzIZgx(a,b,c)
        console.log('res',res)
        return res
    }



})


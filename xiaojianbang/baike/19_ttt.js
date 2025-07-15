Java.perform(function() {

    var TPPlayerConfig = Java.use('com.tencent.thumbplayer.tcmedia.config.TPPlayerConfig')

    TPPlayerConfig.isUserIsVip.implementation = function() {
        var res = this.isUserIsVip()
        console.log('isUserIsVip19',res)
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        return true
    }

    TPPlayerConfig.isUseP2P.implementation = function() {
        var res = this.isUseP2P()
        return true
    }

    var e = Java.use('com.tencent.thumbplayer.tcmedia.c.e')
    e.l.implementation = function() {
        var res = this.l()
        console.log('resl',res)
        return res
    }
    e.p.implementation = function() {
        var res = this.p()
        return res
    }

    e.a.overload('java.lang.String', 'java.util.Map').implementation = function(str,map) {
        console.log('astr  ',str)
        console.log('amap  ',map)
        var res = this.a(str,map)
        console.log('res a',res)
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        return res
    }


    var q = Java.use('com.tencent.thumbplayer.tcmedia.utils.q')
    q.a.implementation = function (str) {

    }

})


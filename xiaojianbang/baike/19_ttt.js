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

    q.a.overload('int','java.lang.Object').implementation = function (int,obj) {
        console.log('1111',int)
        console.log('1111',obj)
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        return this.a(int,obj)
    }

    q.a.overload('int', 'int', 'int', 'java.lang.Object', 'boolean', 'boolean', 'long').implementation = function (i10, i11, i12,obj, z10, z11,j10) {
        console.log('2222')
        return this.a(i10, i11, i12,obj, z10, z11,j10)
    }

    q.b.overload('int', 'int', 'int', 'java.lang.Object', 'boolean', 'boolean', 'long').implementation = function (p1,p2,p3,p4,p5,p6,p7) {
        console.log('3333',p1,p2,p3,p4,p5,p6,p7)
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        return this.b(p1,p2,p3,p4,p5,p6,p7)
    }

    var ThumbMediaPlayer = Java.use('com.tencent.liteav.thumbplayer.ThumbMediaPlayer')
    ThumbMediaPlayer.release.implementation = function () {
        console.log('4444')
        this.release()
    }

})


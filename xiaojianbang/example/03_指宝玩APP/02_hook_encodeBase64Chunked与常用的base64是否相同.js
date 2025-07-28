Java.perform(function() {
    var MainActivity = Java.use('com.hfzs.zhibaowan.ui.MainActivity')
    MainActivity.checkUpdate.implementation = function () {
        console.log('checkUpdate--------')
    }

    var String = Java.use('java.lang.String')

    var Base64 = Java.use('org.apache.commons.codec.binary.Base64')
    Base64.encodeBase64Chunked.implementation = function (bytes) {
        var res = this.encodeBase64Chunked(bytes)
        var str = String.$new(bytes)
        console.log('params ---> :',str)
        var res_str = String.$new(res)
        console.log('res_str ---> :',res_str)
        return res
    }

    var Encrypt = Java.use('com.hfzs.zhibaowan.util.Encrypt')
    Encrypt.encode.implementation = function (str) {
        console.log('encode params ---> ',str)
        var res = this.encode(str)
        console.log('encode res ---> ',res)
        return res
    }
})


//基本一致，注意换行
// params ---> : {"appid":"2","username":"15655541234","password":"123456","cpsId":"tg001lxx","imei":"75c73634-a4e3-40af-b363-37879902f18f"}
// res_str ---> : eyJhcHBpZCI6IjIiLCJ1c2VybmFtZSI6IjE1NjU1NTQxMjM0IiwicGFzc3dvcmQiOiIxMjM0NTYi
// LCJjcHNJZCI6InRnMDAxbHh4IiwiaW1laSI6Ijc1YzczNjM0LWE0ZTMtNDBhZi1iMzYzLTM3ODc5
// OTAyZjE4ZiJ9

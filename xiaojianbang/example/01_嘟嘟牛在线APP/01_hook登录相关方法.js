Java.perform(function() {
    var jsonRequest = Java.use('com.dodonew.online.http.JsonRequest')
    jsonRequest.addRequestMap.overload('java.util.Map','int').implementation = function (map,a) {
        console.log('执行了addRequestMap:',map.toString())
        console.log('执行了addRequestMap:',a)

        var Map = Java.use('java.util.HashMap');
        var obj = Java.cast(map, Map);
        console.log('执行了addRequestMap:',obj.toString())
        this.addRequestMap(map,a)
    }

    var utils = Java.use('com.dodonew.online.util.Utils')
    utils.md5.implementation = function (str) {
        console.log('执行了md5:',str)
        var res = this.md5(str)
        console.log('返回值md5:',res)
        return res
    }

    var RequestUtil = Java.use('com.dodonew.online.http.RequestUtil')
    RequestUtil.encodeDesMap.overload('java.lang.String','java.lang.String','java.lang.String').implementation = function (data,key,iv) {
        console.log('执行了encodeDesMap:',data)
        console.log('执行了encodeDesMap:',key)
        console.log('执行了encodeDesMap:',iv)
        var res = this.encodeDesMap(data,key,iv)
        console.log('返回值encodeDesMap:',res)
        return res
    }

})
Java.perform(function() {
    var jsonRequest = Java.use('com.dodonew.online.http.JsonRequest')
    console.log("jsonRequest:",jsonRequest)

    jsonRequest.addRequestMap.overload('java.util.Map','int').implementation = function (map,a) {
        console.log('执行了addRequestMap:',map.toString())
        console.log('执行了addRequestMap:',a)

        var Map = Java.use('java.util.HashMap');
        var obj = Java.cast(map, Map);
        console.log('执行了addRequestMap:',obj.toString())
        this.addRequestMap(map,a)
    }
})
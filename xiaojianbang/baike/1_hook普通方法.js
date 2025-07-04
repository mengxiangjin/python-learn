Java.perform(function() {
    var jsonRequest = Java.use('com.dodonew.online.http.JsonRequest')
    console.log("jsonRequest:",jsonRequest)
    jsonRequest.paraMap.implementation = function (map) {
        console.log("执行了：",map);
        this.paraMap(map)
    }

    jsonRequest.addRequestMap.implementation = function (map,a) {
        console.log('执行了:',map)
        console.log('执行了:',a)
        this.addRequestMap(map,a)
    }
})
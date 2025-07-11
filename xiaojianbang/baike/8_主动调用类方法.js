Java.perform(function() {
    var jsonRequest = Java.use('com.dodonew.online.http.JsonRequest')
    //静态方法主动调用
    jsonRequest.setAAA('abc')

    //实例方法主动调用（需要先实例化对象） 创建新的对象
    var instance = jsonRequest.$new('abc',12)
    instance.setBBB('abc')

    //遍历内存中所有的Money对象，全部匹配完成回调onComplete
    Java.choose("com.xiaojianbang.hook.Money", {
        onMatch: function (obj){
            console.log(obj.getInfo());
        },
        onComplete: function (){
            console.log("内存中的Money对象搜索完毕");
        }
    });
})
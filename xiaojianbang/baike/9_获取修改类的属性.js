Java.perform(function() {
    var jsonRequest = Java.use('com.dodonew.online.http.JsonRequest')
    //静态属性主动调用
    jsonRequest.counts.value = 20

    //实例属性主动调用（需要先实例化对象） 创建新的对象
    var instance = jsonRequest.$new('abc',12)
    instance.counts.value = 20

    //遍历内存中所有的Money对象，全部匹配完成回调onComplete
    Java.choose("com.xiaojianbang.hook.Money", {
        onMatch: function (obj){
            //如果字段名与方法名一样，需要_区分
            console.log(obj.counts.value);
            console.log(obj._name.value)
        },
        onComplete: function (){
            console.log("内存中的Money对象搜索完毕");
        }
    });
})
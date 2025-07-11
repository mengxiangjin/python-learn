Java.perform(function() {

    //claas B 为JsonRequest的内部类
    var B = Java.use('com.dodonew.online.http.JsonRequest$B')
    B.aaa.implementation = function () {
        this.aaa()
    }

    //匿名内部类（后面的数字取决于你想要的匿名内部类在主类的所有匿名类的排序，从1开始）
    var B = Java.use('com.dodonew.online.http.JsonRequest$2')
    B.aaa.implementation = function () {
        this.aaa()
    }
})
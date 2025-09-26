
function call_active() {
    var EncryptlibUtils = Java.use('com.pocket.snh48.base.net.utils.EncryptlibUtils')
    var params1 = "1758879818020"
    var params2 = "60dff660611c47c4b0d8bb6a0569817c"

      //拿到context上下文
    var currentApplication = Java.use('android.app.ActivityThread').currentApplication();
    var context = currentApplication.getApplicationContext();
    var res = EncryptlibUtils.MD5(context,params1,params2,"")
    console.log("主动调用获取到的结果",res)
    //276daf9d85790fe2f5069f78a2ca0064
}

Java.perform(function() {
    var EncryptlibUtils = Java.use('com.pocket.snh48.base.net.utils.EncryptlibUtils')
    EncryptlibUtils.MD5.implementation = function (ctx,str1,str2,str3) {
        console.log("params:1",str1)
        console.log("params:2",str2)
        console.log("params:3",str3)
        var res = this.MD5(ctx,str1,str2,str3)
        console.log("result:",res)
        return res
    }

})


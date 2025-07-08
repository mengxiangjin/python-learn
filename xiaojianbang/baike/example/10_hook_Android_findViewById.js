Java.perform(function() {
    // Error: java.lang.ClassNotFoundException: Didn't find class "androidx.appcompat.app.AppCompatActivity" on path:
    // 使用Java.enumerateLoadedClassesSync()打印所有已经加载的类路径，发现是android.support.v7.app.AppCompat
    // var AppCompatActivity = Java.use("androidx.appcompat.app.AppCompatActivity");

    var AppCompatActivity = Java.use("android.support.v7.app.AppCompatActivity");
    console.log('AppCompatActivity:',AppCompatActivity)

    var id = Java.use("com.dodonew.online.R$id")
    var btn_login_id = id.btn_login.value
    console.log('btn_login_id',btn_login_id)

    AppCompatActivity.findViewById.implementation = function (id) {
        var res = this.findViewById(id)
        if (id === btn_login_id) {
            console.log('findViewById res',res)
            console.log('findViewById id',id)
        }
        return res;
    }




    //因为findViewById在界面初始化的时候就已经触发，所以需要以spawn方式去启动App才能监测到触发
    //frida -U -f com.dodonew.online -l HookDemo.js -o log.txt --no-pause
    // -f 代码让frida帮我们重新启动app，一开始就注入js
    // --no-pause 直接运行主线程，中途不暂停





})
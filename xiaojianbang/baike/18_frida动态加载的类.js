Java.perform(function() {

    //内存中找不到，可能是不同的类加载器加载的 导致找不到该类
    // var Dynamic = Java.use('com.xiaojianbang.app.Dynamic')
    // Dynamic.sayHello.implementation = function () {
    //     var res = this.sayHello()
    //     console.log(res)
    //     return 'xiaojianbang'
    // }


    //循环遍历所有的类加载器去加载该类即可
    Java.enumerateClassLoaders({
    onMatch: function (loader) {
        try {
            Java.classFactory.loader = loader;
            var dynamic = Java.use("com.xiaojianbang.app.Dynamic");
            console.log("dynamic: ", dynamic);
            //console.log(dynamic.$new().sayHello());
            dynamic.sayHello.implementation = function () {
                console.log("hook dynamic.sayHello is run!");
                return "xiaojianbang";
            }
        } catch (e) {
            console.log('eee');
        }
    },
    onComplete: function () {}
    });




})


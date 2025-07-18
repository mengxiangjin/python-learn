Java.perform(function() {

    //TestRegisterClass是一个接口
    var TestRegisterClass = Java.use('com.xiaojianbang.app.TestRegisterClass')

    var classes = Java.enumerateLoadedClassesSync();

    for (const index in classes) {
        let className = classes[index];
        if(className.indexOf("com.xiaojianbang") === -1) continue;
        try {
            let clazz = Java.use(className);
            let resultArr = clazz.class.getInterfaces();
            console.log("resultArr: ", resultArr);
            if(resultArr.length === 0) continue;
            for (let i = 0; i < resultArr.length; i++) {
                if(resultArr[i].toString().indexOf("com.xiaojianbang.app.TestRegisterClass") !== -1){
                    console.log(className, resultArr);
                }
            }
        }catch (e) {console.log("Didn't find class: " + className);}
    }

    //hook抽象类的实现类
     var TestAbstract = Java.use('com.xiaojianbang.app.TestAbstract')
    var classes = Java.enumerateLoadedClassesSync();
    for (const index in classes) {
        let className = classes[index];
        if(className.indexOf("com.xiaojianbang") === -1) continue;
        try {
            let clazz = Java.use(className);
            let resultClass = clazz.class.getSuperclass();
            console.log("resultClass: ", className, resultClass);
            if(resultClass == null) continue;
            if(resultClass.toString().indexOf("com.xiaojianbang.app.TestAbstract") !== -1){
                console.log(className, resultClass);
            }
        } catch (e) {}
    }
})


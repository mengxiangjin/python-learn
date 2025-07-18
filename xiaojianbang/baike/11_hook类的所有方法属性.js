Java.perform(function() {

    var wallet = Java.use('com.xiaojianbang.hook.Wallet')
    var methods = wallet.class.getDeclaredMethods()
    var constructors = wallet.class.getDeclaredConstructors()
    var fields = wallet.class.getDeclaredFields()
    var classes = wallet.class.getDeclaredClasses()

    for (var i = 0;i < methods.length;i++) {
        console.log(methods[i].getName())
    }
     for (var i = 0;i < constructors.length;i++) {
        console.log(constructors[i])
    }
     for (var i = 0;i < fields.length;i++) {
        console.log(fields[i])
    }

     for (var i = 0;i < classes.length;i++) {
        console.log(classes[i])
    }


     function hookFunc(methodName) {
        console.log(methodName);
        var overloadsArr = utils[methodName].overloads;
        for (var j = 0; j < overloadsArr.length; j++) {
            overloadsArr[j].implementation = function () {
                var params = "";
                for (var k = 0; k < arguments.length; k++) {
                    params += arguments[k] + " ";
                }
                console.log("utils." + methodName + " is called! params is: ", params);
                return this[methodName].apply(this, arguments);
            }
        }
    }

    var utils = Java.use("com.xiaojianbang.hook.Utils");
    var methods = utils.class.getDeclaredMethods();
    for (let i = 0; i < methods.length; i++) {
        let methodName = methods[i].getName();
        hookFunc(methodName);
    }
})
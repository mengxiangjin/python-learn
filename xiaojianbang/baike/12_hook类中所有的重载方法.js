Java.perform(function() {
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
        var methodName = methods[i].getName();
        hookFunc(methodName);
    }

})
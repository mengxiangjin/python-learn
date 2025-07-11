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

})
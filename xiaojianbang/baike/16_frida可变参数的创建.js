Java.perform(function() {
    //主动调用此方法需要传递可变长数组参数
    // public static String myPrint(Object... objArr) {
    //     StringBuilder sb = new StringBuilder();
    //     for (Object obj : objArr) {
    //         sb.append(obj);
    //         sb.append("|");
    //     }
    //     return sb.toString();
    // }


     var utils = Java.use('com.xiaojianbang.hook.Utils')
        var res = utils.myPrint(['aaa',Java.use('java.lang.Integer').$new(10),'ccc'])
        // var res = utils.myPrint(['aaa',10,'ccc'])   //会报错，需要用包装类包装一下

    console.log(res)

})
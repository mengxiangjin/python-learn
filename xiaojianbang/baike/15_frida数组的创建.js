Java.perform(function() {
    //主动调用此方法需要传递数组参数
    //  public static String myPrint(String[] strArr) {
    //     StringBuilder sb = new StringBuilder();
    //     for (String str : strArr) {
    //         sb.append(str);
    //         sb.append("|");
    //     }
    //     return sb.toString();
    // }

    var utils = Java.use('com.xiaojianbang.hook.Utils')
    var res = utils.myPrint(['aaa','bbb','ccc'])
    console.log(res)

    var array = Java.array(
        'Ljava.lang.String;',
        ['ddd','eee','fff']
    )
    console.log(utils.myPrint(array))
})
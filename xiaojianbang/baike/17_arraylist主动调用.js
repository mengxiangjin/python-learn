Java.perform(function() {
    var ArrayList = Java.use('java.util.ArrayList').$new()
    //添加整数类型
    let obj = Java.use('java.lang.Integer').$new(10)
    let bool = Java.use('java.lang.Boolean').$new(true)
    console.log(ArrayList.add(obj))
    console.log(ArrayList.add(bool))

})
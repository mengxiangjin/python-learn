Java.perform(function() {
    var class_list = Java.enumerateLoadedClassesSync()
    console.log(class_list)
})
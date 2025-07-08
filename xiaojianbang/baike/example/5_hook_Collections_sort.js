Java.perform(function() {
    var Collections = Java.use("java.util.Collections");
    Collections.sort.overload('java.util.List').implementation = function (list) {
        var ArrayList = Java.use('java.util.ArrayList');
        var obj = Java.cast(list, ArrayList);
        console.log("Collections.sort", obj);
        this.sort(list);
    }
})
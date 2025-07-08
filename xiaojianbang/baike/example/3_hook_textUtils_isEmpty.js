Java.perform(function() {
    var TextUtils = Java.use("android.text.TextUtils");
    TextUtils.isEmpty.implementation = function (a) {
        console.log("isEmpty: ", a);
        return this.isEmpty(a);
    }
})
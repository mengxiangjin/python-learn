Java.perform(function () {
    var contextHolder = Java.use('com.xingin.shield.http.ContextHolder');
    console.log('sAppId=',contextHolder.sAppId.value);
    console.log('sDeviceId=',contextHolder.sDeviceId.value);
    console.log('sExperimentd=',contextHolder.sExperiment.value);
})

// frida -UF -l  5.vlaue.js


//sAppId= -319115519
//sDeviceId= cbd4f703-1198-3bb3-8edf-5f8b14a338f4

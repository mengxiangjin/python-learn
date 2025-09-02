Java.perform(function() {


    //找lib的基地址
    console.log('------------------------------导入表开始');
    let module = Process.findModuleByName("libencryptlib.so")
    console.log("lib的基址:",Process.findModuleByName("libencryptlib.so").base)
    console.log("lib的基址:",Process.getModuleByName("libencryptlib.so").base)
    console.log("lib的基址:",Module.findBaseAddress("libencryptlib.so"))

})
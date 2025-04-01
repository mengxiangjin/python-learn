// 后期这个代码，所有app都可以直接用
//1 加载安卓手机底层包，系统自带的库，我们hook的NewStringUTF在这个包中  不是app自己写的，是安卓底层库，所有安卓只要支持jni，都有这个so
var symbols = Module.enumerateSymbolsSync("libart.so");  // 底层包中有很多内置的函数 ：NewStringUTF
//2 定义一个变量，用来接收一会找到的NewStringUTF的地址
var addrNewStringUTF = null;
//3 循环找出libart.so中所有成员，匹配是NewStringUTF的函数，取出地址，赋值给上面的变量
for (var i = 0; i < symbols.length; i++) {
    //3.1 取出libart.so的一个个方法对象
    var symbol = symbols[i];
    //3.2 判断方法对象的名字是不是包含 NewStringUTF和CheckJNI---》因为在真正底层，函数名不叫NewStringUTF，前后有别的字符串
    // 实际它真正的名字：asdfa_NewStringUTF_dadsfasfd
    if (symbol.name.indexOf("NewStringUTF") >= 0 && symbol.name.indexOf("CheckJNI") < 0) {
        // 3.3 找到后，把地址赋值个上面的变量
        addrNewStringUTF = symbol.address;
        // 3.4 控制台打印一下
        console.log("NewStringUTF is at ", symbol.address, symbol.name);
        break
    }
}
// 4 如果不为空，我们开始hook它(通过地址hook，有onEnter和onExit，所有的参数都给了args，通过位置取到每个参数)
if (addrNewStringUTF != null) {
    Interceptor.attach(addrNewStringUTF, {
        onEnter: function (args) { // args 是入参
            // 4.1 取出NewStringUTF传入的第一个参数 ，就是 c语言的那个字符串
            var c_string = args[1];
            // 4.2 第一个参数是c的字符串，我们把它转一下，变成真正的字符串---》c中是字符串数组，转成真正的字符串
            var dataString = c_string.readCString();
            // 4.3 改字符串不为空，且长度为32，我们输出一下，并且打印出它的调用栈
            if (dataString) {
                if (dataString.length === 32) {
                    console.log(dataString);
                    // 4.4 读取当前在执行那个so文件,及so文件中的地址
                    console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
                    // 4.5 打印调用栈
                    console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
                }
            }

        }
    });
}

// frida -UF  -l  5-通用的hook-NewStringUTF.js -o v1.txt
/*
319f91e745a7e34897fce41cd216fb50
0xb58321a5 libbili.so!0x31a5
java.lang.Throwable
	at com.bilibili.nativelibrary.LibBili.s(Native Method)
	at com.bilibili.nativelibrary.LibBili.g(BL:1)
	at com.bilibili.okretro.f.a.h(BL:1)
	at com.bilibili.okretro.f.a.d(BL:7)
	at com.bilibili.okretro.f.a.a(BL:4)
	at com.bilibili.okretro.d.a.execute(BL:24)
	at tv.danmaku.biliplayerv2.service.SeekService$b.run(BL:9)
	at android.os.Handler.handleCallback(Handler.java:938)
	at android.os.Handler.dispatchMessage(Handler.java:99)
	at android.os.Looper.loop(Looper.java:223)
	at android.os.HandlerThread.run(HandlerThread.java:67)
 */
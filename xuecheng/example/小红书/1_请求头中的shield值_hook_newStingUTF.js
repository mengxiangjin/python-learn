var symbols = Module.enumerateSymbolsSync("libart.so");
var addrNewStringUTF = null;
for (var i = 0; i < symbols.length; i++) {
    var symbol = symbols[i];

    if (symbol.name.indexOf("NewStringUTF") >= 0 && symbol.name.indexOf("CheckJNI") < 0) {
        addrNewStringUTF = symbol.address;
        console.log("NewStringUTF is at ", symbol.address, symbol.name);
         break
    }
}


if (addrNewStringUTF != null) {
    Interceptor.attach(addrNewStringUTF, {
        onEnter: function (args) {
            var c_string = args[1];
            var dataString = c_string.readCString();
            if (dataString.indexOf("XYAAAAAQAAAAEAAAB") != -1) {
                console.log(dataString);
                
//                console.log(Thread.backtrace(this.context, Backtracer.ACCURATE).map(DebugSymbol.fromAddress).join('\n') + '\n');
                console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
                
            }
        }
    });
}

// frida -UF  -l  1.so_utfstring.js


//XYAAAAAQAAAAEAAABTAAAAUzUWEe0xG1IbD9/c+qCLOlKGmTtFa+lG43AJf+FXQaoRl9C0yLFnT535/ulXz8N4js5+2fdmRgxLR23aZb+l3yho0OB0XR11oWU0j8EyEs3oyxyO
//java.lang.Throwable
//        at com.xingin.shield.http.XhsHttpInterceptor.intercept(Native Method)
//        at com.xingin.shield.http.XhsHttpInterceptor.intercept(XhsHttpInterceptor.java:5)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.g1.j.a.intercept(UserAgentInterceptor.kt:4)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.g1.j.b.intercept(ValueRewriteInterceptor.kt:6)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.e0.b.intercept(ExceptionWithUrlInterceptor.kt:3)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.g1.k.a.intercept(XYFixOkhttpInterceptor.kt:1)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.e0.r0.k.intercept(XhsNetTrackInterceptor.kt:8)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.e0.c0.intercept(XhsSavingResponseInterceptor.kt:1)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.e0.y.intercept(UnicomKingInterceptor.kt:5)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.b0.d.a.intercept(LoginInterceptor.kt:2)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.j.b.intercept(AntiSpamNativeInterceptor.kt:2)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at p.d0.v1.e0.d0.b.intercept(CustomHeadersInterceptor.kt:7)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:10)
//        at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:1)
//        at okhttp3.RealCall.getResponseWithInterceptorChain(RealCall.java:13)
//        at okhttp3.RealCall.execute(RealCall.java:8)
//        at d0.m.execute(OkHttpCall.java:8)
//        at p.d0.g1.b.b.b(XYRxJava2CallAdapterFactory.kt:5)
//        at s.a.r.a(Observable.java:153)
//        at p.d0.g1.b.a.b(XYRxJava2CallAdapterFactory.kt:1)
//        at s.a.r.a(Observable.java:153)
//        at s.a.j0.e.e.s.b(ObservableDoOnEach.java:1)
//        at s.a.r.a(Observable.java:153)
//        at s.a.j0.e.e.a1$b.run(ObservableSubscribeOn.java:1)
//        at p.d0.g1.i.a.run(SkynetScheduler.kt:4)
//        at p.d0.q1.i.k.a$b$a.invoke(LightHelper.kt:2)
//        at p.d0.q1.i.k.a$b$a.invoke(LightHelper.kt:1)
//        at p.d0.q1.i.k.a$b.run(LightHelper.kt:19)
//        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
//        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
//        at java.lang.Thread.run(Thread.java:923)
//        at p.d0.q1.i.k.i.d$b.run(LightBaseThreadFactory.kt:2)

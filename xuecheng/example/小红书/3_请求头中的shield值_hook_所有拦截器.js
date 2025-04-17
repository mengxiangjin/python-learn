Java.perform(function () {
    var Builder = Java.use('okhttp3.OkHttpClient$Builder');

    Builder.addInterceptor.implementation = function (inter) {
        //console.log("实例化：");

        console.log( JSON.stringify(inter) );
        //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        return this.addInterceptor(inter);
    };
})

//  frida -U -f com.xingin.xhs  -l 6.all_inter.js


//[Pixel 2 XL::com.xingin.xhs ]-> "<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.e>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.k0.f$a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.k.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.l0.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.e>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.k0.f$a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.k.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.d0.b>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.j.b>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.b0.d.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.y>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.c0>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.r0.k>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.k.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.b>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.j.b>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.j.a>"
//"<instance: okhttp3.Interceptor, $className: com.xingin.shield.http.XhsHttpInterceptor>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.n0.h>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.k.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.r0.k>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.j.b>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.j.a>"
//"<instance: okhttp3.Interceptor, $className: okhttp3.logging.HttpLoggingInterceptor>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.r0.k>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.k.a>"
//"<instance: okhttp3.Interceptor, $className: p.d0.g1.j.b>"
//"<instance: okhttp3.Interceptor, $className: p.d0.v1.e0.n0.h>"
//"<instance: okhttp3.Interceptor, $className: com.xingin.shield.http.XhsHttpInterceptor>"

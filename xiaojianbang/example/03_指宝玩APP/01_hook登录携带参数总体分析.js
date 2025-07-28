Java.perform(function() {
    var MainActivity = Java.use('com.hfzs.zhibaowan.ui.MainActivity')
    MainActivity.checkUpdate.implementation = function () {
        console.log('checkUpdate--------')
    }

    var String = Java.use('java.lang.String')
    String.getBytes.overload().implementation = function () {
        var res = this.getBytes()
        var str = String.$new(res)
        console.log('res1 ---> :',str)
        return res
    }

    String.getBytes.overload('java.nio.charset.Charset').implementation = function (charset) {
        console.log('getBytes--------3',charset)
         var res = this.getBytes(charset)
        var str = String.$new(res)
        console.log('res3 ---> :',str)
        console.log("stack: ",Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()))
        return res
    }

})

// 登录抓包发现请求体中都是16进制的字节串，此时hook String中的getBytes得到如下 继续打印堆栈分析
// getBytes--------3 UTF-8
// res3 ---> : {"appid":"2","username":"15655541234","password":"123456","cpsId":"tg001lxx","imei":"75c73634-a4e3-40af-b363-37879902f18f"}
//stack:  java.lang.Throwable
//         at java.lang.String.getBytes(Native Method)
//         at java.lang.String.getBytes(String.java:978)
//         at java.lang.String.getBytes(Native Method)
//         at com.hfzs.zhibaowan.util.Encrypt.decodeStr(Encrypt.java:82)
//         at com.hfzs.zhibaowan.util.Encrypt.decode(Encrypt.java:51)
//         at com.hfzs.zhibaowan.network.GetDataImpl.unzip(GetDataImpl.java:158)
//         at com.hfzs.zhibaowan.network.GetDataImpl.requestLoginUrl(GetDataImpl.java:1018)
//         at com.hfzs.zhibaowan.ui.LoginActivity$1.doInBackground(LoginActivity.java:100)
//         at com.hfzs.zhibaowan.ui.LoginActivity$1.doInBackground(LoginActivity.java:96)
//         at android.os.AsyncTask$3.call(AsyncTask.java:394)
//         at java.util.concurrent.FutureTask.run(FutureTask.java:266)
//         at android.os.AsyncTask$SerialExecutor$1.run(AsyncTask.java:305)
//         at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
//         at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
//         at java.lang.Thread.run(Thread.java:923)

//  x149_170_124_155_151_125_120_167_146_124_170_152_172_206_174_207_179_171_179_155_206_158_195_231_209_221_183_230_205_199_190_172_192_
// 226_190_171_143_172_152_117_147_154_152_192_150_180_152_124_150_183_198_185_180_153_153_206_184_137_187_206_188_199_123_138_127_154_123_171_129_1
// 59_131_103_134_141_186_203_112_110_177_169_177_210_204_178_185_182_199_177_184_166_186_224_197_226_194_186_184_240_219_194_169_118_140_173_188_17
// 5_168_159_122_182_172_159_150_132_152_186_180_131_172_206_184_208_165_194_166_138_118_120_117_97_140_135_129_169_132_123_122_161_187_203_148_205_178_224_192_226_181_190_184_159_188_178_210_165_126_124_194_200_182_239_209_226_190_174_155_171_141_125_82_80y

//res3 ---> : eyJhIjotMSwiYiI6Ilx1NzUyOFx1NjIzN1x1NTQwZFx1NGUwZFx1NWI1OFx1NTcyOFx1NjIxNlx1NWRmMlx1ODhhYlx1NjJjOVx1OWVkMVx1ZmYwMSIsImMiOnsidXNlcm5hbWUiOiIiLCJuaWNlbmFtZSI6IiIsInBhc3N3b3JkIjoiIn19
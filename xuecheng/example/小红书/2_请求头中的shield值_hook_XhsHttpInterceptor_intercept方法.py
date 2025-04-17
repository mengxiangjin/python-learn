import frida
import sys

#模拟器启动frida-server
rdev = frida.get_remote_device()

#deviceId 437665
#udid中 des加密的key值 appapiche168comappapiche168comap  iv:appapich

# 包名：com.che168.autotradercloud
# 车智赢+
session = rdev.attach("小红书")  # app名字

# ----上面固定------以后只会动src中代码
# src 是字符串，写js代码
scr = """
Java.perform(function () {
    var xhsHttpInterceptor = Java.use("com.xingin.shield.http.XhsHttpInterceptor");
    var Buffer = Java.use("okio.Buffer");
    var Charset = Java.use("java.nio.charset.Charset");
    //替换类中的方法
    xhsHttpInterceptor.intercept.overload('okhttp3.Interceptor$Chain','long').implementation = function(chain,j){
        console.log('-----------------请求来了-------------------');
        var request = chain.request();

        console.log("网址：")
        console.log(request.url().toString())

        console.log("请求头：")
        console.log(request.headers().toString());

        var requestBody = request.body();
        if (requestBody) {
            var buffer = Buffer.$new();
            requestBody.writeTo(buffer);
            console.log("请求体：")
            console.log(buffer.readString(Charset.forName("utf8")));
        }
        console.log("参数2：",j)

        var res = this.intercept(chain, j);
        return res;
    }
});
"""


# -----下面固定---以后不会动
script = session.create_script(scr)

def on_message(message, data):
    print(message, data)

script.on("message", on_message)
script.load()
sys.stdin.read()

# -----------------请求来了-------------------
# 网址：
# https://www.xiaohongshu.com/api/sns/v1/system_service/check_code?zone=86&phone=15655542558&code=123456
# 请求头：
# X-B3-TraceId: 03036b94491c0400
# xy-common-params: fid=174489558010907696d9426c0a9d4592be034529d16a&device_fingerprint=2025041721124389b728ba32dde6c23ba49fda9098452401946d56dff2f2cb&device_fingerprint1=2025041721124389b728ba32dde6c23ba49fda9098452401946d56dff2f2cb&launch_id=1744897972&tz=Asia%2FShanghai&channel=YingYongBao&versionName=6.73.0&deviceId=cbd4f703-1198-3bb3-8edf-5f8b14a338f4&platform=android&sid=session.1744896751298845707272&identifier_flag=0&t=1744898921&project_id=ECFAAF&build=6730157&x_trace_page_current=welcome_page&lang=zh-Hans&app_id=ECFAAF01&uis=light
# User-Agent: Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1) Resolution/1440*2880 Version/6.73.0 Build/6730157 Device/(Google;Pixel 2 XL) discover/6.73.0 NetType/WiFi
#
# 参数2： 4026063056
import frida
import sys

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")
scr = """
Java.perform(function () {

    var libbili = Module.findBaseAddress("libbili.so");
	// hook sub_22B0函数，通过偏移量找到 偏移量 22B0
	var s_func = libbili.add(0x22b0 + 1); // 32位的so文件都要 +1
    console.log(s_func);

    Interceptor.attach(s_func, {
        onEnter: function (args) {
            // args[0]
            // args[1]，明文字符串
            // args[2]，明文字符串长度

            console.log("执行update，长度是：",args[2], args[2].toInt32());

            // console.log( hexdump(args[1], {length: args[2].toInt32()})  );
            console.log(args[1].readUtf8String())
        },
        onLeave: function (args) {
            console.log("=======================结束===================");
        }
    });
});
"""
script = session.create_script(scr)
script.load()
sys.stdin.read()

# 执行update，长度是： 0x2d5 725
# actual_played_time=0&aid=114193634166089&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=28974451112&epid=0&epid_status=&from=64&from_spmid=main.my-history.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=32&s_locale=zh-Hans_CN&session=cebb89d429244e4fba8addb00913a8cf2c004a23&sid=0&spmid=main.ugc-video-detail.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&sub_type=0&total_time=0&ts=1743399934&type=3&user_status=0&video_duration=2397
# =======================结束===================
# 执行update，长度是： 0x8 8
# 560c52cc
# =======================结束===================
# 执行update，长度是： 0x8 8
# d288fed0
# =======================结束===================
# 执行update，长度是： 0x8 8
# 45859ed1
# =======================结束===================
# 执行update，长度是： 0x8 8
# 8bffd973
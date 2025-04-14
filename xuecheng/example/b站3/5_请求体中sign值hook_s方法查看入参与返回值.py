import frida
import sys

# 连接手机设备
rdev = frida.get_remote_device()

session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function () {
    var LibBili = Java.use("com.bilibili.nativelibrary.LibBili");
    var TreeMap = Java.use("java.util.TreeMap");

    LibBili.s.implementation = function(map){   
        console.log("--------------------------");
       console.log("map=",JSON.stringify(map));
       var obj = Java.cast(map,TreeMap);
       console.log("map=",obj.toString());

       var res = this.s(map);
       console.log("返回值=",res.toString());
       return res;
    }
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)

script.load()
sys.stdin.read()


# --------------------------
# map= "<instance: java.util.SortedMap, $className: java.util.TreeMap>"
# map= {actual_played_time=0, aid=114193634166089, appkey=1d8b6e7d45233436, auto_play=0, build=6240300, c_locale=zh-Hans_CN, channel=xxl_gdt_wm_253, cid=28974451112, epid=0, epid_status=, from=64, from_spmid=main.my-history.0.0, last_play_progress_time=0, list_play_time=0, max_play_progress_time=0, mid=0, miniplayer_play_time=0, mobi_app=android, network_type=1, paused_time=0, platform=android, play_status=0, play_type=1, played_time=0, quality=32, s_locale=zh-Hans_CN, session=f9174a204e4cf4e9def40b5048c64ead107f66be, sid=0, spmid=main.ugc-video-detail.0.0, start_ts=0, statistics={"appId":1,"platform":3,"version":"6.24.0","abtest":""}, sub_type=0, total_time=0, type=3, user_status=0, video_duration=2397}
# 返回值= actual_played_time=0&aid=114193634166089&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=28974451112&epid=0&epid_status=&from=64&from_spmid=main.my-history.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=32&s_locale=zh-Hans_CN&session=f9174a204e4cf4e9def40b5048c64ead107f66be&sid=0&spmid=main.ugc-video-detail.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&sub_type=0&total_time=0&ts=1743390299&type=3&user_status=0&video_duration=2397&sign=72577313768d4051c07bf32931682272
# --------------------------
# map= "<instance: java.util.SortedMap, $className: java.util.TreeMap>"
# map= {aid=114193634166089, appkey=1d8b6e7d45233436, build=6240300, c_locale=zh-Hans_CN, channel=xxl_gdt_wm_253, cid=28974451112, mobi_app=android, platform=android, s_locale=zh-Hans_CN, statistics={"appId":1,"platform":3,"version":"6.24.0","abtest":""}}
# 返回值= aid=114193634166089&appkey=1d8b6e7d45233436&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=28974451112&mobi_app=android&platform=android&s_locale=zh-Hans_CN&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&ts=1743390299&sign=375829e0734b1782768829a33f5f4c48
# --------------------------
# map= "<instance: java.util.SortedMap, $className: java.util.TreeMap>"
# map= {access_key=, appkey=1d8b6e7d45233436, build=6240300, buvid=XX3862036564C58B283B051A0A365E6A2B343, c_locale=zh-Hans_CN, channel=xxl_gdt_wm_253, device=android, from_spmid=main.my-history.0.0, install_apps=, mobi_app=android, oid=114193634166089, platform=android, s_locale=zh-Hans_CN, share_id=main.ugc-video-detail.0.0.pv, share_origin=vinfo_share, sid=28974451112, statistics={"appId":1,"platform":3,"version":"6.24.0","abtest":""}}
# 返回值= access_key=&appkey=1d8b6e7d45233436&build=6240300&buvid=XX3862036564C58B283B051A0A365E6A2B343&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&device=android&from_spmid=main.my-history.0.0&install_apps=&mobi_app=android&oid=114193634166089&platform=android&s_locale=zh-Hans_CN&share_id=main.ugc-video-detail.0.0.pv&share_origin=vinfo_share&sid=28974451112&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&ts=1743390300&sign=34f0791124474fe03d4271abe6a13f97


# --------------------------
# map= "<instance: java.util.SortedMap, $className: java.util.TreeMap>"
# map= {actual_played_time=0, aid=1501630152, appkey=1d8b6e7d45233436, auto_play=0, build=6240300, c_locale=zh-Hans_CN, channel=xxl_gdt_wm_253, cid=1467056786, epid=0, epid_status=, from=3, from_spmid=search.search-result.0.0, last_play_progress_time=0, list_play_time=0, max_play_progress_time=0, mid=0, miniplayer_play_time=0, mobi_app=android, network_type=1, paused_time=0, platform=android, play_status=0, play_type=1, played_time=0, quality=32, s_locale=zh-Hans_CN, session=a93e86ca7c337f8809a7a8e88df8f1620573b7bf, sid=0, spmid=main.ugc-video-detail.0.0, start_ts=0, statistics={"appId":1,"platform":3,"version":"6.24.0","abtest":""}, sub_type=0, total_time=0, type=3, user_status=0, video_duration=2887}
#         actual_played_time=0&aid=1501630152&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=1467056786&epid=0&epid_status=&from=3&from_spmid=search.search-result.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=32&s_locale=zh-Hans_CN&session=a93e86ca7c337f8809a7a8e88df8f1620573b7bf&sid=0&spmid=main.ugc-video-detail.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D%2C%20sub_type%3D0%2C%20total_time%3D0%2C%20type%3D3%2C%20user_status%3D0%2C%20video_duration%3D2887%7D&sub_type=0&total_time=0&ts=1744464595&type=3&user_status=0&video_duration=2887
#         actual_played_time=0&aid=1501630152&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=1467056786&epid=0&epid_status=&from=3&from_spmid=search.search-result.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=32&s_locale=zh-Hans_CN&session=a93e86ca7c337f8809a7a8e88df8f1620573b7bf&sid=0&spmid=main.ugc-video-detail.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D%2C%20sub_type%3D0%2C%20total_time%3D0%2C%20type%3D3%2C%20user_status%3D0%2C%20video_duration%3D2887%7D&ts=1744464948&sign=6a4dd4f2be7f69b0a950375a1912bc55
#         actual_played_time=0&aid=1501630152&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=1467056786&epid=0&epid_status=&from=3&from_spmid=search.search-result.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=32&s_locale=zh-Hans_CN&session=a93e86ca7c337f8809a7a8e88df8f1620573b7bf&sid=0&spmid=main.ugc-video-detail.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&sub_type=0&total_time=0&ts=1744465023&type=3&user_status=0&video_duration=2887&sign=2c1e48f3d311d37c659ad2734784a57c
#
# # 返回值= actual_played_time=0&aid=1501630152&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh-Hans_CN&channel=xxl_gdt_wm_253&cid=1467056786&epid=0&epid_status=&from=3&from_spmid=search.search-result.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=32&s_locale=zh-Hans_CN&session=a93e86ca7c337f8809a7a8e88df8f1620573b7bf&sid=0&spmid=main.ugc-video-detail.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&sub_type=0&total_time=0&ts=1744462231&type=3&user_status=0&video_duration=2887&sign=e440ee101f5d27afda74cb5de98546d2

import requests
import subprocess

method = "get"
url = "https://edith.xiaohongshu.com/api/sns/v1/note/feed?note_id=63b01b4d0000000022034d77&page=1&num=5&fetch_mode=1&source=explore&ads_track_id="
common_params = "fid=167337148910401a044595fd44d95587c504e09275d9&device_fingerprint=2022112007045266bb5eba5505d24d7b1d35dec1975913018dc5b30ffa5ab5&device_fingerprint1=2022112007045266bb5eba5505d24d7b1d35dec1975913018dc5b30ffa5ab5&launch_id=1673372503&tz=Asia%2FHong_Kong&channel=YingYongBao&versionName=6.73.0&deviceId=d7a8fa4f-98a2-398a-a7a5-417bf5e0b971&platform=android&sid=session.1673372424638448802568&identifier_flag=0&t=1673372498&project_id=ECFAAF&build=6730157&x_trace_page_current=explore_feed&lang=zh-Hans&app_id=ECFAAF01&uis=light"

body = "null"

cmd = f'java -jar  unidbg-android.jar {method} "{url}" "{common_params}" "{body}"'
signature = subprocess.check_output(cmd, shell=True, cwd="unidbg_android_jar")
data_string = signature.strip().decode('utf-8').split("\n")[-1]
shield_string = data_string.lstrip("shield=")

res = requests.get(
    url=url,
    headers={
        "xy-common-params": common_params,
        "xy-platform-info": "platform=android&build=6730157&deviceId=d7a8fa4f-98a2-398a-a7a5-417bf5e0b971",
        "shield": shield_string
    }
)

print(res.status_code, res.text)
import requests
import subprocess

method = "post"
url = "https://www.xiaohongshu.com/api/sns/v4/user/login/password"
common_params = "fid=174507372610907696d9426c0a9d4592be034529d16a&device_fingerprint=2025041721124389b728ba32dde6c23ba49fda9098452401946d56dff2f2cb&device_fingerprint1=2025041721124389b728ba32dde6c23ba49fda9098452401946d56dff2f2cb&launch_id=1745172683&tz=Asia%2FShanghai&channel=YingYongBao&versionName=6.73.0&deviceId=cbd4f703-1198-3bb3-8edf-5f8b14a338f4&platform=android&sid=session.1745073696691463090486&identifier_flag=0&t=1745377317&project_id=ECFAAF&build=6730157&x_trace_page_current=login_full_screen_sms_page&lang=zh-Hans&app_id=ECFAAF01&uis=light"
body = "password=e03079c5f4a883fe00d2adadfc1a7311&zone=86&phone=18256027382&imsi=unknow&android_version=30&type=phone&android_id=e7636641400676c8&mac=9e:ab:9f:ac:40:41"

cmd = f'java -jar  unidbg-android.jar {method} "{url}" "{common_params}" "{body}"'
signature = subprocess.check_output(cmd, shell=True, cwd="unidbg_android_jar")
data_string = signature.strip().decode('utf-8').split("\n")[-1]
shield_string = data_string.lstrip("shield=")

print(shield_string)


body = {
    "password": "e03079c5f4a883fe00d2adadfc1a7311",
    "zone": "86",
    "phone": "18256027382",
    "imsi": "unknow",
    "android_version": "30",
    "type": "phone",
    "android_id": "e7636641400676c8",
    "mac": "9e:ab:9f:ac:40:41"
}

res = requests.post(
    url=url,
    headers={
        "xy-common-params": common_params,
        "xy-platform-info": "platform=android&build=6730157&deviceId=d7a8fa4f-98a2-398a-a7a5-417bf5e0b971",
        "shield": shield_string,
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1) Resolution/1440*2880 Version/6.73.0 Build/6730157 Device/(Google;Pixel 2 XL) discover/6.73.0 NetType/Unknown",
        "xy-platform-info": "platform=android&build=6730157&deviceId=cbd4f703-1198-3bb3-8edf-5f8b14a338f4"
    },
    data=body
)

print(res.text)
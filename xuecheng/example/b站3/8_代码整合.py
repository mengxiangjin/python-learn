import datetime
import uuid
import base64
import hashlib
import time
import requests
import re
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus
import string
import random
import time
import hashlib
import ctypes
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BiliBili(object):
    def __init__(self, aid, bvid, cid, duration, proxies):
        self.aid, self.bvid, self.cid, self.duration = aid, bvid, cid, duration

        self.wifi_mac = self.create_random_mac().upper()
        self.device_id = self.create_device_id(self.wifi_mac)  # did
        self.buvid = self.create_buvid_by_wifi()
        self.session_id = self.create_session_id()

        self.build_brand = "HUAWEI"
        self.build_model = 'Mate 10 Pro'

        self.fp_local = self.create_local(self.buvid, self.build_model, "")
        self.fp_remote = self.create_local(self.buvid, self.build_model, "")

        self.app_first_run_time = str(int(time.time()) - random.randint(0, 24 * 60 * 60))  # fts
        self.ts = str(int(time.time() - 10))

        self.session = requests.Session()
        # self.session.proxies = proxies
        self.start_ts = None
        self.heart_beat_session_id = None

    def create_random_mac(self, sep=":"):
        """ 随机生成mac地址 """
        data_list = []
        for i in range(1, 7):
            part = "".join(random.sample("0123456789ABCDEF", 2))
            data_list.append(part)
        mac = sep.join(data_list)

        return mac

    def create_device_id(self, mac):
        """
        根据mac地址生成 3.device_id
        :param mac: 传入参数的格式是 00:00:00:00:00
        :return:
        """

        def gen_sn():
            return "".join(random.sample("123456789" + string.ascii_lowercase, 10))

        def base64_encrypt(data_string):
            data_bytes = bytearray(data_string.encode('utf-8'))
            data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
            for i in range(1, len(data_bytes)):
                data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
            res = base64.encodebytes(bytes(data_bytes))
            return res.strip().strip(b"==").decode('utf-8')

        # 1. 生成mac地址（保证mac中的每个元素是不重复的，例如：0000000000)
        mac_str = mac

        # 2. 去除IP地址中的符号，只保留 48e1e828e02e（变小写）
        mac_str = re.sub("[^0-9A-Fa-f]", "", mac_str)
        mac_str = mac_str.lower()

        # 3. 获取手续序列号
        sn = gen_sn()

        # 4. 拼接并进行base64加密
        total_string = "{}|||{}".format(mac_str, sn)
        return base64_encrypt(total_string)

    def create_buvid_by_wifi(self):
        """
            基于wifi mac地址生成buvid （ B站app中有四种获取buvid的方式：设备ID、wifi mac地址、3.device_id、uuid ）
        """
        md5 = hashlib.md5()
        md5.update(self.wifi_mac.encode('utf-8'))
        v0_1 = md5.hexdigest()
        return "XY{}{}{}{}".format(v0_1[2], v0_1[12], v0_1[22], v0_1).upper()

    def create_session_id(self):
        # return "".join([hex(item)[2:] for item in random.randbytes(4)])
        return "".join([hex(random.randint(1, 255))[2:] for i in range(4)])

    def create_local(self, buvid, phone_model, phone_band):
        """
        fp_local和fp_remote都是用这个算法来生成的，在手机初始化阶段生成 fp_local，
        :param buvid: 根据算法生成的buvid，例如："XYBA4F3B2789A879EA8AEEDBE2E4118F78303"
        :param phone_model:  手机型号modal，例如："Mate 10 Pro"
        :param phone_band:  手机品牌band，在模拟器上是空字符串（我猜是程序员想要写成 brand ）哈哈哈哈
        :return:
        """

        def a_b(arg8):
            v3 = 0
            v4 = 60
            v0_1 = 2
            v5 = 0
            while True:
                v6 = arg8[v3:v3 + 2]
                v5 += int(v6, base=16)
                if v3 != v4:
                    v3 += v0_1
                    continue
                break
            xx = "%02x" % (v5 % 0x100,)
            return xx

        def misc_helper_kt(data_bytes):
            data_list = []
            v7 = len(data_bytes)
            v0 = 0
            while v0 < v7:
                v2 = data_bytes[v0]
                data_list.append("%02x" % v2)
                v0 += 1
            return ''.join(data_list)

        data_string = "{}{}{}".format(buvid, phone_model, phone_band)
        hash_object = hashlib.md5()
        hash_object.update(data_string.encode('utf-8'))
        data = hash_object.digest()

        arg1 = misc_helper_kt(data)
        arg2 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # arg3 = misc_helper_kt(random.randbytes(8))
        arg3 = misc_helper_kt([random.randint(1, 255) for i in range(8)])

        str2 = "{}{}{}".format(arg1, arg2, arg3)
        local = str2 + a_b(str2)
        return local

    def x_report_click_android2(self):
        SALT = "9cafa6466a028bfb"
        KEY = "fd6b639dbcff0c2a1b03b389ec763c4b"
        IV = "77b07a672d57d64c"

        def sha_256_encrypt(data_string):
            sha = hashlib.sha256()
            sha.update(data_string.encode('utf-8'))
            sha.update(SALT.encode('utf-8'))
            return sha.hexdigest()

        def aes_encrypt(data_string):
            aes = AES.new(
                key=KEY.encode('utf-8'),
                mode=AES.MODE_CBC,
                iv=IV.encode('utf-8')
            )
            raw = pad(data_string.encode('utf-8'), 16)
            return aes.encrypt(raw)

        ctime = int(time.time())
        info = {
            'aid': self.aid,
            'cid': self.cid,
            'part': 1,
            'mid': 0,
            'lv': 0,
            'ftime': ctime - random.randint(100, 1000),
            'stime': ctime,
            'did': self.device_id,
            'type': 3,
            'sub_type': 0,
            'sid': '0',
            'epid': '',
            'auto_play': 0,
            'build': 6240300,
            'mobi_app': 'android',
            'spmid': 'main.ugc-video-detail.0.0',
            'from_spmid': 'search.search-result.0.0'
        }
        data = "&".join(["{}={}".format(key, info[key]) for key in sorted(info.keys())])
        sign = sha_256_encrypt(data).lower()
        data = "{}&sign={}".format(data, sign)
        aes_string = aes_encrypt(data)

        res = self.session.post(
            url="https://api.bilibili.com/x/report/click/android2",
            headers={
                "accept-length": "gzip",
                "content-type": "application/json; charset=utf-8",
                "app-key": "android",
                "User-Agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/Mate 10 Pro mobi_app/android build/6240300 channel/bili innerVer/6240300 osVer/6.0.1 network/2",
                "env": "prod",
                "buvid": self.buvid,
                "device-id": self.device_id,
                "session_id": self.session_id,
                "fp_local": self.fp_local,
                "fp_remote": self.fp_remote,
            },
            data=aes_string,
            timeout=10,
            verify=False

        )
        # print(res.text)
        res.close()

    def get_param_sign_s(self, param_dict):
        """
        :param param_dict: 要签名的参数字典
        :return:
        """
        ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])
        encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest()

        return "{}&sign={}".format(ordered_string, sign)

    def create_heart_beat_session_id(self):
        arg0 = str(int(time.time() * 1000)) + str(random.randint(1, 1000000))
        # sha1加密
        hash_object = hashlib.sha1()
        hash_object.update(arg0.encode('utf-8'))
        arg7 = hash_object.hexdigest()
        return arg7

    def heart_beat_start(self, aid, cid, duration):
        self.start_ts = ts = int(time.time() - 10)
        self.heart_beat_session_id = self.create_heart_beat_session_id()
        form_dict = {
            "actual_played_time": "0",
            "aid": aid,
            "appkey": "1d8b6e7d45233436",
            "auto_play": "0",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "bili",
            "cid": cid,
            "epid": "0",
            "epid_status": "",
            "from": "2",
            "from_spmid": "main.ugc-video-detail.0.0",
            "last_play_progress_time": "0",
            "list_play_time": "0",
            "max_play_progress_time": "0",
            "mid": "0",
            "miniplayer_play_time": "0",
            "mobi_app": "android",
            "network_type": "1",
            "paused_time": "0",
            "platform": "android",
            "play_status": "0",
            "play_type": "1",
            "played_time": "0",
            "quality": "32",
            "s_locale": "zh_CN",
            "session": self.heart_beat_session_id,
            "sid": "0",
            "spmid": "main.ugc-video-detail.0.0",
            "start_ts": "0",
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(',', ':'))),
            "sub_type": "0",
            "total_time": "0",
            "type": "3",
            "user_status": "0",
            "video_duration": duration,
            "ts": ts,
        }

        total_body_string = self.get_param_sign_s(form_dict)

        res = self.session.post(
            url="https://api.bilibili.com/x/report/heartbeat/mobile",
            data=total_body_string.encode('utf-8'),
            headers={
                "accept-length": "gzip",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8",
                "app-key": "android",
                "User-Agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/Mate 10 Pro mobi_app/android build/6240300 channel/bili innerVer/6240300 osVer/6.0.1 network/2",
                "env": "prod",
                "buvid": self.buvid,
                "device-id": self.device_id,
                "session_id": self.session_id,
                "fp_local": self.fp_local,
                "fp_remote": self.fp_remote,
            },
            verify=False
        )
        res.close()

    def heart_beat_end(self, aid, cid, duration):
        current_ts = int(time.time())

        form_dict = {
            "actual_played_time": duration,  # 实际播放时间
            "aid": aid,
            "appkey": "1d8b6e7d45233436",
            "auto_play": "0",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "bili",
            "cid": cid,
            "epid": "0",
            "epid_status": "",
            "from": "2",
            "from_spmid": "main.ugc-video-detail.0.0",
            "last_play_progress_time": duration,
            "list_play_time": "0",
            "max_play_progress_time": duration,
            "mid": "0",
            "miniplayer_play_time": "0",
            "mobi_app": "android",
            "network_type": "1",
            "paused_time": current_ts - self.start_ts - duration,  # 暂停时间
            "platform": "android",
            "play_status": "0",
            "play_type": "1",
            "played_time": duration,
            "quality": "32",
            "s_locale": "zh_CN",
            "session": self.heart_beat_session_id,
            "sid": "0",
            "spmid": "main.ugc-video-detail.0.0",
            "start_ts": self.start_ts,
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(',', ':'))),
            "sub_type": "0",
            "total_time": current_ts - self.start_ts,
            "type": "3",
            "user_status": "0",
            "video_duration": self.duration,
            "ts": current_ts,
            # "sign": "b098ca2c4caa53de22720a9755fde742"
        }

        total_body_string = self.get_param_sign_s(form_dict)

        res = self.session.post(
            url="https://api.bilibili.com/x/report/heartbeat/mobile",
            headers={
                "accept-length": "gzip",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8",
                "app-key": "android",
                "User-Agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/Mate 10 Pro mobi_app/android build/6240300 channel/bili innerVer/6240300 osVer/6.0.1 network/2",
                "env": "prod",
                "buvid": self.buvid,
                "device-id": self.device_id,
                "session_id": self.session_id,
                "fp_local": self.fp_local,
                "fp_remote": self.fp_remote,
            },
            data=total_body_string.encode('utf-8'),
            verify=False
        )
        res.close()


headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

def get_video_id_info(exec_url, proxies):
    session = requests.Session()
    bvid = exec_url.rsplit('/')[-1]
    res = session.get(
        url="https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp".format(bvid),
        # proxies=proxies,
        verify=False,
        headers=headers
    )

    cid = res.json()['data'][0]['cid']

    res = session.get(
        url="https://api.bilibili.com/x/web-interface/view?cid={}&bvid={}".format(cid, bvid),
        # proxies=proxies,
        verify=False,
        headers=headers
    )
    res_json = res.json()
    aid = res_json['data']['aid']
    view_count = res_json['data']['stat']['view']
    duration = res_json['data']['duration']
    session.close()
    return aid, bvid, cid, duration, int(view_count)


def get_proxy_dict():
    key = "..."
    passwd = "..."
    host = "..."
    return {
        "http": 'http://{}:{}@{}'.format(key, passwd, host),
        "https": 'http://{}:{}@{}'.format(key, passwd, host)
    }


def run():
    url = "https://www.bilibili.com/video/BV1Mu4y1Y7Ho"
    while True:
        try:
            # 1.IP代理
            # proxies = get_proxy_dict()
            proxies = {}

            # 2.获取视频信息
            aid, bvid, cid, duration, view_count = get_video_id_info(url, proxies)
            print("\n播放量为：{}".format(view_count))

            # 3.创建对象 -> buvid、session生成
            bili = BiliBili(aid, bvid, cid, duration, proxies=proxies)

            # 4.播放
            bili.x_report_click_android2()

            # 5.心跳开始
            bili.heart_beat_start(aid, cid, duration)

            # 6.模拟观看视频
            time.sleep(10)

            # 7.结束心跳
            bili.heart_beat_end(aid, cid, duration)

            # 8.关闭连接
            bili.session.close()
        except Exception as e:
            print("异常：", e)


if __name__ == '__main__':
    run()


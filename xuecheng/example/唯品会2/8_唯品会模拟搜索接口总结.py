import random
import time
import uuid
from base64 import b64encode
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import hashlib
from urllib.parse import quote_plus
import requests
import hashlib

requests.packages.urllib3.disable_warnings()  # https 会有红色警告，去掉

# ====================== 注册设备 ======================
api_key = "23e7f28019e8407b98b84cd05b5aef2c"
skey = '6692c461c3810ab150c9a980d0c275ec'

mars_cid = device_token = str(uuid.uuid4())
android_id = ''.join(["%x" % random.randint(1, 15) for i in range(16)])
build_model = "Pixel 2 XL"
ctime = str(int(time.time()))
session_id = "{}_shop_android_1669730552506".format(mars_cid, ctime)


def sha1(data_string):
    # sha1加密
    hash_object = hashlib.sha1()
    hash_object.update(data_string.encode('utf-8'))
    arg7 = hash_object.hexdigest()
    return arg7

device_token = str(uuid.uuid4())
param_dict = {
    'app_name': 'achievo_ad',
    'app_version': '7.83.3',
    'device_token': device_token,
    'status': 1,
    'warehouse': 'null',
    'manufacturer': 'Google',
    'device': build_model,
    'os_version': '30',
    'channel': 'oziq7dxw:::',
    'vipruid': '',
    'regPlat': '0',
    'regid': '',
    'rom': 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)',
    'skey': '6692c461c3810ab150c9a980d0c275ec',

}

ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])

salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{ordered_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.get(
    url="https://mp.appvipshop.com/apns/device_reg",
    params=param_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },verify=False
)
print("1.注册设备", res.text)


# ====================== getTokenByFP ======================
res = requests.get(
    url="https://vcsp-api.vip.com/token/getTokenByFP?vcspKey=4d9e524ad536c03ff203787cf0dfcd29",
    headers={
        "vcspauthorization": "vcspSign=05a68135d2bfd322e3a22f95bbc25a24c777f387"
    },verify=False
)

print(res.text)
vsp_dict = res.json()['data']

# ====================== generate_token ======================

dinfo = '{"ah1":"","ah2":"","ah3":"","ah4":"wifi","ah5":"1080_2189","ah6":1804800,"ah7":8,"ah8":7742595072,"ah9":"%s","ah10":"","ah11":"","ah12":"","ah13":"","as1":"10","as2":"","as3":"","as4":"%s","as5":"","as6":"","as7":"29","ac1":"%s"}' % (
    build_model, android_id, device_token)

data_dict = {
    "app_name": "shop_android",
    "app_version": "7.83.3",
    "client_type": "android",
    "dinfo": quote_plus(dinfo),
    "mars_cid": mars_cid,
    "phone_model": build_model,
    "session_id": "{}_shop_android_{}".format(mars_cid, ctime),
    "sys_version": "29",
    "vcspKey": "4d9e524ad536c03ff203787cf0dfcd29",
    "vcspToken": vsp_dict['vcspToken']
}

data = "&".join(["{}={}".format(key, data_dict[key]) for key in sorted(data_dict.keys())])
iv = ''.join(["%x" % random.randint(1, 15) for i in range(16)])

obj = hashlib.md5()
obj.update(b'aee4c425dbb2288b80c71347cc37d04b')
key = obj.digest()

aes = AES.new(
    key=key,
    mode=AES.MODE_CBC,
    iv=iv.encode('utf-8')
)
raw = pad(data.encode('utf-8'), 16)
encrypt_bytes = aes.encrypt(raw)
total_bytes = iv.encode('utf-8') + encrypt_bytes
edata = b64encode(total_bytes).decode('utf-8')

body_dict = {
    'api_key': "23e7f28019e8407b98b84cd05b5aef2c",
    'did': "",
    'edata': edata,
    'eversion': "0",
    'skey': "6692c461c3810ab150c9a980d0c275ec",
    'timestamp': int(time.time())
}

body_string = "&".join(["{}={}".format(key, body_dict[key]) for key in sorted(body_dict.keys())])
# print(body_string)
salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{body_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.post(
    url="https://mapi.appvipshop.com/vips-mobile/rest/device/generate_token",
    data=body_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },
    verify=False
)
print("3.token", res.text)
did = res.json()['data']['token']['did']

# ====================== 搜索 ======================

key_word = "裤子"

search_dict = {
    "api_key": api_key,
    "app_name": "shop_android",
    "app_version": "7.83.3",
    "bigSaleTagIds": "",
    "brandIds": "",
    "brandStoreSns": "",
    "categoryId": "",
    "channelId": "1",
    "channel_flag": "0_1",
    "client": "android",
    "client_type": "android",
    "darkmode": "0",
    "deeplink_cps": "",
    "device_model": "".format(build_model),
    "did": did,
    "elder": "0",
    "extParams": '{"priceVer":"2","mclabel":"1","cmpStyle":"1","statusVer":"2","ic2label":"1","video":"2","preheatTipsVer":"4","floatwin":"1","superHot":"1","exclusivePrice":"1","router":"1","coupons":"1","needVideoExplain":"1","rank":"2","needVideoGive":"1","bigBrand":"1","couponVer":"v2","videoExplainUrl":"1","live":"1","sellpoint":"1","reco":"1","vreimg":"1","search_tag":"2","tpl":"1","stdSizeVids":"","labelVer":"2"}',
    "fdc_area_id": "101103104123",
    "functions": "RTRecomm,flagshipInfo,feedback,otdAds,zoneCode,slotOp,survey,hasTabs,floaterParams",
    "harmony_app": "0",
    "harmony_os": "0",
    "headTabType": "all",
    "height": "2189",
    "isMultiTab": "0",
    "keyword": key_word,
    "lastPageProperty": '{"isBgToFront":"0","suggest_text":"%s","scene_entry_id":"-99","refer_page_id":"page_te_globle_classify_search_1669733882852","text":"%s","tag":"1","module_name":"com.achievo.vipshop.search","type":"all","typename":"全部","is_back_page":"0"}' %(key_word,key_word),
    "maker": "REDMI",
    "mars_cid": mars_cid,
    "mobile_channel": "oziq7dxw:::",
    "mobile_platform": "3",
    "net": "WIFI",
    "operator": "中国电信",
    "os": "Android",
    "osv": "10",
    "otddid": "",
    "other_cps": "",
    "page_id": "page_te_commodity_search_{}".format(int(time.time() * 1000) - 200),
    "phone_model": build_model,
    "priceMax": "",
    "priceMin": "",
    "props": "",
    "province_id": "101103",
    "referer": "com.achievo.vipshop.search.activity.TabSearchProductListActivity",
    "rom": "Dalvik/2.1.0 (Linux; U; Android 10; M2007J17C MIUI/V12.0.11.0.QJSCNXM)",
    "sd_tuijian": "0",
    "service_provider": "46011",
    "session_id": session_id,
    "skey": skey,
    "sort": "0",
    "source": "app",
    "source_app": "android",
    "standby_id": "oziq7dxw:::",
    "sys_version": "29",
    "timestamp": ctime,
    "union_mark": "blank&_&blank&_&oziq7dxw:::&_&blank&_&blank",
    "vipService": "",
    "warehouse": "VIP_BJ",
    "width": "1080"
}

search_string = "&".join(["{}={}".format(key, search_dict[key]) for key in sorted(search_dict.keys())])
# print(body_string)
salt = "aee4c425dbb2288b80c71347cc37d04b"
tmp = sha1(f"{salt}{search_string}")
api_sign = sha1(f"{salt}{tmp}")

res = requests.post(
    url="https://mapi.appvipshop.com/vips-mobile/rest/shopping/search/product/list/v1",
    data=search_dict,
    headers={
        "Authorization": "OAuth api_sign={}".format(api_sign)
    },
    verify=False
)
print(res.text)
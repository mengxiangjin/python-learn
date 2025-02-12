import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/28.0)'
}
data={"password":"lqz12345","username":"17717823244"}
res=requests.post('https://miappshop.jshulin.com/memberLogin/login',json=data,verify=False,headers=headers)
print(res.text)
import requests
import ssl
import urllib3
import certifi
import logging


url = 'https://fanyi.baidu.com/sug'


headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
data = {
    'kw' : 'dog'
}
print(certifi.where())
logging.captureWarnings(True)

resp = requests.post(url,headers = headers,data = data,verify=False)
print(resp.json())
import requests
import json
import re

headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

res = requests.get("http://www.bilibili.com/video/BV1HC4y1v7gW/?spm_id_from=333.337.search-card.all.click",verify=False,headers=headers)
data_list = re.findall(r'__INITIAL_STATE__=(.+);\(function', res.text)
data_dict = json.loads(data_list[0])

aid = data_dict['aid']
cid = data_dict['videoData']['cid']

print(aid)
print(cid)

# 793434948 aid
# 1398237398 cid
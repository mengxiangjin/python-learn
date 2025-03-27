import hashlib
data = 'aid=114085018475145&auto_play=0&build=6240300&cid=28630322467&did=IEV3QXlBIht-TnxFcBEjEVEBaBB1GStzPw&epid=&from_spmid=search.search-result.0.0&ftime=1742543780&lv=0&mid=0&mobi_app=android&part=1&sid=0&spmid=main.ugc-video-detail.0.0&stime=1743059499&sub_type=0&type=3'
salt = '9cafa6466a028bfb'
obj = hashlib.sha256()

obj.update(data.encode('utf-8')) # 先对 明文 update，再加盐
obj.update(salt.encode('utf-8'))
print(obj.hexdigest())
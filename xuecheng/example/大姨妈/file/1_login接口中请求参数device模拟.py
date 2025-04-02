import hashlib

# null deviceID
# cb362844b93983e9:android_id
# taimengooglearm64-v8ataimenRP1A.201005.004.A1abfarm-01392RP1A.201005.004.A1GooglePixel 2 XLtaimenrelease-keysuserandroid-build:设备信息
# D2:74:CF:79:9D:DC：mac地址
# 02:00:00:00:00:00：蓝牙信息
if __name__ == '__main__':
    str = 'nullcb362844b93983e9taimengooglearm64-v8ataimenRP1A.201005.004.A1abfarm-01392RP1A.201005.004.A1GooglePixel 2 XLtaimenrelease-keysuserandroid-buildD2:74:CF:79:9D:DC02:00:00:00:00:00'
    obj = hashlib.sha1()
    obj.update(str.encode('utf-8'))
    print(obj.hexdigest())

# 929dd3baab6e4679798a1776c70bb0186d0ca3f3
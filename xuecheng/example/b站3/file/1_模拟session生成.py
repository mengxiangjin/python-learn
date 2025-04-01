import hashlib

#的确是sha1加密
if __name__ == '__main__':
    datas = '1743387417586178117'
    obj = hashlib.sha1()
    obj.update(datas.encode('utf-8'))
    print(obj.hexdigest())
import hashlib

#无法逆向解密
if __name__ == '__main__':
    m = hashlib.md5()
    m.update('123456'.encode('utf-8'))  #md5加密 必须为字节格式，可能会有盐
    print(m.hexdigest())
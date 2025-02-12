import hashlib

#无法逆向解密
if __name__ == '__main__':
    m = hashlib.sha1()
    m.update('helloworld'.encode('utf-8'))  #sha1加密 必须为字节格式，可能会有盐
    print(m.hexdigest())
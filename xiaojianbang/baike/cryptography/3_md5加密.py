import hashlib

def encrypt_str(data):
    md5 = hashlib.md5()
    md5.update(data.encode())
    print(md5.hexdigest())
    print(md5.digest())

def encrypt_bytes(data):
    md5 = hashlib.md5()
    md5.update(data)
    print(md5.hexdigest())
    print(md5.digest())

if __name__ == '__main__':
    encrypt_str("123456")
    encrypt_bytes(b'123456')


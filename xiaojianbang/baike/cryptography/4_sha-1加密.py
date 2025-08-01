import hashlib


def encrypt_str(data):
    sha1 = hashlib.sha1()
    sha1.update(data.encode())
    print(sha1.hexdigest())
    print(sha1.digest())

def encrypt_bytes(data):
    md5 = hashlib.sha1()
    md5.update(data)
    print(md5.hexdigest())
    print(md5.digest())


if __name__ == '__main__':
   encrypt_str("123456")
   encrypt_bytes(b"123456")


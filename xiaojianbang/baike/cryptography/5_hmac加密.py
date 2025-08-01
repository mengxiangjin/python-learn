import hashlib
import hmac


def encrypt_str(key,data):
    hmac_object = hmac.new(key.encode(),data.encode(),hashlib.sha1)
    print(hmac_object.hexdigest())
    print(hmac_object.digest())

def encrypt_bytes(key,data):
    hmac_object = hmac.new(key, data, hashlib.sha1)
    print(hmac_object.hexdigest())
    print(hmac_object.digest())




if __name__ == '__main__':
    encrypt_str("123456","abcd")
    encrypt_bytes(b'123456',b'abcd')

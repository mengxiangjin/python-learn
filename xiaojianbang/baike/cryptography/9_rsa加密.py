
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5


from Crypto.Signature import PKCS1_v1_5
from Crypto.Signature import pkcs1_15

from Crypto.PublicKey import RSA

public_key_base64 = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDA04AyPfNOx3191YpWOBQ5pmic
VOKVqGMKcX6J4DwFGe94aHQweHyLlthDJFCgMEfu5xyeUK1b26qgCZeTRUGRQMHr
diqZz/di6TcIdwrmRAlzn4FJ//qql4JLODGB2W76k52t3zyJJoULckMfbDIpZS0M
nDnsyLj2IRRl9cSjoQIDAQAB
-----END PUBLIC KEY-----'''

private_key_base64 = '''-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAMDTgDI9807HfX3V
ilY4FDmmaJxU4pWoYwpxfongPAUZ73hodDB4fIuW2EMkUKAwR+7nHJ5QrVvbqqAJ
l5NFQZFAwet2KpnP92LpNwh3CuZECXOfgUn/+qqXgks4MYHZbvqTna3fPIkmhQty
Qx9sMillLQycOezIuPYhFGX1xKOhAgMBAAECgYEAryw0zO/MpmfCUFt69gKyFQFh
DYxr34t+lhEu5HBp9jRugVNbImGCu4kI5E4MVMonvxgDvqsKImX3prWwFqEXAxdY
tZnQRnFHvSI/m/HqtOAGHQF/Xxsqcje+fJqV7hkJXuEF83Mce/KxyBkW0RhDSeo6
e6mppaPGp0gtC2YfmAECQQD/XPZDVS9wiIMD6/B8IZlwUa0AgXVi1Joo6VrSe8cQ
6qsZvljnkA0ojkFXi2NJIRDPjrB8H0xLznipbwPOvPJBAkEAwU6cmi5W7S5bn7OP
2nHWneWQl0Q/QaDco7kqN4/Gtyo5hyfE9x+o6FDBjXJUjaZVmNiX2YMYPb3J5MHu
kmSZYQJAJXHyQolZPX0nCQot52Xd5BR1898H4YgfWuRtBvRTim1+zXWV/86lv06s
0jOESZLpriXURz8npu4Nz3qR6lzWgQJBAIZfEtTKKXqtotscgn6ia0FO9ndv5VjF
bRoR+Jquwr9IBr1Ak9YEl/EFUcX1F3lviki5JrT4P72LU/BELoZsj4ECQQCGI8ZG
LrXJIZQmeXh3JqcGlY1ednvdrzjz26rLXrrdZ+0zP8nU34sepOWePJkLTN0h0KhN
LUaqtodQau0URoVR
-----END PRIVATE KEY-----'''



# RSA加密中的公钥私钥是需要去生成的，可借助APi也可去网站进行生成
#PKCS1_OAEP填充模式下，因为是随机填充会导致对于同一个明文，每次加密后的结果是不一样的
def generate_rsa_keys():
    # key = RSA.generate(1024)
    # public_key = key.public_key().exportKey()
    # private_key = key.exportKey()
    return public_key_base64,private_key_base64

def encrypt_data(public_key,data):
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

def decrypted_data(private_key,encrypted_data):
    rsa_key = RSA.importKey(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data



if __name__ == '__main__':
    public_key,private_key = generate_rsa_keys()
    print('公钥---》',public_key)
    print('私钥---》',private_key)
    encrypted_data = encrypt_data(public_key,'这是abcd')
    print('加密的密文---》',encrypted_data.hex())
    decrypted_data = decrypted_data(private_key,encrypted_data)
    print('解密后的明文---》',decrypted_data.decode())



from Crypto.Hash import SHA256
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



#数字签名即私钥对已经进行加密过的数据（sha1，sha-256）再次进行签名加密，得到signature
#验证时首先对 待验证的数据，加密（sha1，sha-256），然后用RSA公钥对其解密与上述signature进行比对验证
def generate_rsa_keys():
    # key = RSA.generate(1024)
    # public_key = key.public_key().exportKey()
    # private_key = key.exportKey()
    return public_key_base64, private_key_base64


#RSA中私钥对SHA256加密后的数据进行签名（加密）
def sign_data_with_sha256(private_key, data):
    #字符串私钥转换成对象
    private_key = RSA.import_key(private_key)
    #通过私钥创建签名对象
    signer = pkcs1_15.new(private_key)
    #对data数据进行sha256加密
    if (isinstance(data,bytes)):
        sha256_data = SHA256.new(data)
    else:
        sha256_data = SHA256.new(data.encode())
    #对加密后的data进行签名,得到签名后的字节串
    signature = signer.sign(sha256_data)
    return signature

#RSA中的公钥对SHA256加密后的验证数据进行验证
def verify_data_with_sha256(public_key, verify_data, signature):
    rsa_key = RSA.importKey(public_key)
    signer = pkcs1_15.new(rsa_key)
    if (isinstance(verify_data,bytes)):
        sha256_verify_data = SHA256.new(verify_data)
    else:
        sha256_verify_data = SHA256.new(verify_data.encode())
    try:
        signer.verify(sha256_verify_data, signature)
        return True
    except (ValueError):
        return False


if __name__ == '__main__':
    public_key, private_key = generate_rsa_keys()
    data = '这是abcd'
    print('签名的元数据---》',data)
    signature = sign_data_with_sha256(private_key, data)
    print('签名后值---》', signature.hex())
    verify_data = '这是abcd'
    verify_result = verify_data_with_sha256(public_key, verify_data, signature)
    print(f'验证的数据是：{verify_data},验证的结果是：{verify_result}')

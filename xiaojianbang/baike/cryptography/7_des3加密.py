from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad,unpad


#3DES实际上是DES加密、DES解密、DES加密
#3DES分组加密（组的大小为24字节），IV为8字节，密钥必须为24字节，填充同DES，密钥的前8个字节用于DES加密，中间8个字节为DES解密。后面8个字节为DES加密


def encrypt_ECB(key,data):
    if isinstance(key,bytes):
        real_key = key
    else:
        real_key = key.encode()

    if isinstance(data,bytes):
        real_data = data
    else:
        real_data = data.encode()

    cipher = DES3.new(key=real_key,mode=DES3.MODE_ECB)
    padding_data = pad(real_data,DES3.block_size)
    encrypto_txt = cipher.encrypt(padding_data)
    return encrypto_txt


def decrypt_ECB(key,encrypt_txt):
    if isinstance(key, bytes):
        real_key = key
    else:
        real_key = key.encode()

    if isinstance(encrypt_txt, bytes):
        real_encrypt_txt = encrypt_txt
    else:
        real_encrypt_txt = bytes.fromhex(encrypt_txt)

    cipher = DES3.new(key=real_key,mode=DES3.MODE_ECB)

    #先解密、后去除填充
    decrypted_data = cipher.decrypt(real_encrypt_txt)
    decrypted_data = unpad(decrypted_data,DES3.block_size)

    return decrypted_data.decode()
def encrypt_CBC(key,data,iv):
    if isinstance(key,bytes):
        real_key = key
    else:
        real_key = key.encode()

    if isinstance(data, bytes):
        real_data = data
    else:
        real_data = data.encode()

    if isinstance(iv, bytes):
        real_iv = iv
    else:
        real_iv = iv.encode()

    cipher = DES3.new(key=real_key,iv=real_iv,mode=DES3.MODE_CBC)
    real_data = pad(real_data,DES3.block_size)

    return cipher.encrypt(real_data)

def decrypt_CBC(key,encrypt_txt,iv):
    if isinstance(key,bytes):
        real_key = key
    else:
        real_key = key.encode()

    if isinstance(encrypt_txt, bytes):
        real_encrypt_txt = encrypt_txt
    else:
        real_encrypt_txt = bytes.fromhex(encrypt_txt)

    if isinstance(iv, bytes):
        real_iv = iv
    else:
        real_iv = iv.encode()


    cipher = DES3.new(key=real_key,iv=real_iv,mode=DES3.MODE_CBC)
    decrypted_data = cipher.decrypt(real_encrypt_txt)
    decrypted_data = unpad(decrypted_data,DES3.block_size)
    return decrypted_data.decode()

if __name__ == '__main__':
    key = '123456788765432112345678'
    data = "这是abcd"
    encrypt_txt_ECB = encrypt_ECB(key,data)
    print(f'ECB模式下密钥：{key},数据：{data}')
    print('ECB加密--》',encrypt_txt_ECB.hex())
    print('ECB解密--》',decrypt_ECB(key,encrypt_txt_ECB))
    print('----------------------------------------------')

    iv = '12345678'
    print(f'CBC模式下密钥：{key},数据：{data},iv:{iv}')
    encrypt_txt_CBC = encrypt_CBC(key,data,iv)
    print('CBC加密--》',encrypt_txt_CBC.hex())
    print('CBC解密--》',decrypt_CBC(key,encrypt_txt_CBC,iv))



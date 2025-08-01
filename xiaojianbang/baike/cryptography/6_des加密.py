from Crypto.Cipher import DES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

#DES分组加密（分块加密），每块大小为8字节，故加密数据以8的倍数为填充，密钥8字节，iv也需要为8字节
#DES加密需要密钥key，且key必须为8个字节（实际计算时参与加密的只有56位，剩余8位进行校验），否则会报错
#DES加密只能加密64位数据，即8个字节，不足的会通过你调用的填充方式进行填充然后加密，超过的话，会进行单独分组加密
#DES加密模式常见ECB与CBC模式：ECB模式不需要IV向量的参与，ECB模式下会将每个分组进行单独加密，会导致每相同的8个字节，加密的结果是一样的
#CBC模式下需要IV向量的参与增加算法的复杂性，CBC模式下也会对每个分组进行单独加密，对当前分组的加密依赖于上一个分组的加密结果去计算加密。所以即使每8个字节相同但是加密结果是不一样的
#CBC模式下IV向量的长度也需要是8个字节64位，否则会报错
#填充Python中默认pkcs7，填充值为需要填充的字节数，如需要填充3个字节，则填充0x06,0x06,0x06
#pkcs5,同pkcs7.不同的是pkcs5仅适用于8字节块的加密算法（DES），而pkcs7可适用于任何块的填充

def encrypt_ECB(key,data):
    if isinstance(key,bytes):
        real_key = key
    else:
        real_key = key.encode()

    if isinstance(data,bytes):
        real_data = data
    else:
        real_data = data.encode()

    cipher = DES.new(key=real_key,mode=DES.MODE_ECB)
    padding_data = pad(real_data,DES.block_size)
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

    cipher = DES.new(key=real_key,mode=DES.MODE_ECB)

    #先解密、后去除填充
    decrypted_data = cipher.decrypt(real_encrypt_txt)
    decrypted_data = unpad(decrypted_data,DES.block_size)

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

    cipher = DES.new(key=real_key,iv=real_iv,mode=DES.MODE_CBC)
    real_data = pad(real_data,DES.block_size)

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


    cipher = DES.new(key=real_key,iv=real_iv,mode=DES.MODE_CBC)
    decrypted_data = cipher.decrypt(real_encrypt_txt)
    decrypted_data = unpad(decrypted_data,DES.block_size)
    return decrypted_data.decode()

if __name__ == '__main__':
    key = '123456789'
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



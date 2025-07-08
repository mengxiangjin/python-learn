import base64
import hashlib

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad,unpad


class Utils:
    @staticmethod
    def MD5_HEX(str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))  # md5加密 必须为字节格式，可能会有盐
        return m.hexdigest()

    @staticmethod
    def MD5_BYTE(str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))  # md5加密 必须为字节格式，可能会有盐
        return m.digest()

    @staticmethod
    def DES_ENCRYPT(plaintext,key,iv):
        if isinstance(plaintext,str):
            padded_data = pad(plaintext.encode('utf-8'), DES.block_size)
        else:
            padded_data = pad(plaintext, DES.block_size)

        if isinstance(key,str):
            if isinstance(iv,str):
                enciper = DES.new(key.encode(), DES.MODE_CBC, iv.encode())
            else:
                enciper = DES.new(key.encode(), DES.MODE_CBC, iv)
        else:
            if isinstance(iv,str):
                enciper = DES.new(key, DES.MODE_CBC, iv.encode())
            else:
                enciper = DES.new(key, DES.MODE_CBC, iv)
        result = enciper.encrypt(padded_data)
        return result

    @staticmethod
    def DES_DECRYPT(cipertext,key,iv):
        if isinstance(key,str):
            if isinstance(iv,str):
                deciper = DES.new(key.encode(), DES.MODE_CBC, iv.encode())
            else:
                deciper = DES.new(key.encode(), DES.MODE_CBC, iv)
        else:
            if isinstance(iv,str):
                deciper = DES.new(key, DES.MODE_CBC, iv.encode())
            else:
                deciper = DES.new(key, DES.MODE_CBC, iv)
        decrypt_data = deciper.decrypt(cipertext)
        plaintext = unpad(decrypt_data,DES.block_size)
        return plaintext.decode()

    @staticmethod
    def base64_to_str(data):
        encode_data = base64.b64encode(data)
        return encode_data.decode()

    @staticmethod
    def base64_decode(data):
        decode_data = base64.b64decode(data)
        return decode_data
import hashlib

from Crypto.Cipher import DES


class Utils:
    @staticmethod
    def MD5(str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))  # md5加密 必须为字节格式，可能会有盐
        return m.hexdigest()

    # def des(data,key,iv):
    #     key = b'88888888'
    #     count = 8 - (len(data) % 8)
    #     plaintext = data + count * "="
    #     des = DES.new(key, DES.MODE_ECB)
    #     ciphertext = des.encrypt(plaintext.encode())
    #     print(base64.b64encode(ciphertext))
    #     print(ciphertext)
    #     plaintext = des.decrypt(ciphertext)
    #     print(plaintext)
    #     plaintext = plaintext[:len(plaintext) - count]
    #     print(plaintext)
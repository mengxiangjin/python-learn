from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_v1_5, AES
from base64 import b64encode


def c(data_text):
    array = "0123456789ABCDEF"
    data_list = []
    for b in data_text.encode('utf-8'):
        data_list.append(array[(b & 240) >> 4])
        data_list.append(array[b & 15])
    return "".join(data_list)


data = "18953675221"

rsa_pub_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCsAwGz+E7PEppCUWrM46wf9Sj2Zv+dlSIjwGtMoG9iG36HFYy0BC+uAgNDun0joo4UFW0qejyc2ExjFXBRiYENnseY3jb9qI0c3thAj2qd5iofGCWaRO1DA707xwD7MOjvHur7c7nvBNv+vwWFvMDiZzj4JqaaV8ZNTT2oO9+aJQIDAQAB
-----END PUBLIC KEY-----"""
key = RSA.importKey(rsa_pub_key)
cipher = PKCS1_v1_5.new(key)
encrypt_bytes = cipher.encrypt(data.encode('utf-8'))
cipher_text = b64encode(encrypt_bytes).decode('utf-8')
cipher_text = cipher_text.replace(r"\n", "")


result = c(cipher_text)
print(result)
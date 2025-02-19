import base64

from Crypto.Cipher import AES,DES3


def pad(text):
    return text + (8 - len(text) % 8) * chr(8 - len(text) % 8)


if __name__=='__main__':
    #CBC加密的key为前24为
    key = b'appapiche168comappapiche168comap'[0:24]
    iv = b'appapich'
    plaintext = pad("351564261441893|1739957368.000000|437665").encode("utf-8")

    cipher = DES3.new(key, AES.MODE_CBC, iv)
    result = cipher.encrypt(plaintext)
    print(result)
    print(base64.b64encode(result))

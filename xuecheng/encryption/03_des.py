import base64

from Crypto.Cipher import DES


#key+iv
if __name__ == '__main__':
    key = b'88888888'
    data = 'Hello World'
    count = 8 - (len(data) % 8)
    plaintext = data + count * "="
    des = DES.new(key,DES.MODE_ECB)
    ciphertext = des.encrypt(plaintext.encode())
    print(base64.b64encode(ciphertext))
    print(ciphertext)
    plaintext = des.decrypt(ciphertext)
    print(plaintext)
    plaintext = plaintext[:len(plaintext) - count]
    print(plaintext)
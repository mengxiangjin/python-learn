import rsa

if __name__ == '__main__':
    public_key, private_key = rsa.newkeys(1024)
    print(public_key)
    print(private_key)

    plaintext = b'Hello World!'
    ciphertext = rsa.encrypt(plaintext, public_key) #公钥加密
    print(ciphertext)
    plaintext = rsa.decrypt(ciphertext, private_key) #私钥解密、
    print(plaintext)

    #使用私钥签名
    sign_message = rsa.sign(plaintext, private_key,'MD5')
    print(sign_message)

    #验证私钥签名
    text = b'Hello World!' #通过   Hello World!!!即报错
    method = rsa.verify(text, sign_message,public_key)
    print(method)

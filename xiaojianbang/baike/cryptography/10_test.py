from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5  # 不使用填充的加密方法
from Crypto.Random import get_random_bytes



# 生成 RSA 密钥对
rsa_key = RSA.generate(2048)

# 公钥
public_key = rsa_key.publickey()

# 创建一个 PKCS1_v1_5 cipher
cipher = PKCS1_v1_5.new(public_key)

# 要加密的明文
data = "这是abcd"

# 加密数据，None 表示不使用填充
ciphertext = cipher.encrypt(data.encode())

print("加密后的密文:", ciphertext.hex())
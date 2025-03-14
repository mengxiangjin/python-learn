from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
def aes_encrypt(data_string,key):
    aes = AES.new(
        key=key.encode('utf-8'),
        mode=AES.MODE_ECB,
    )
    raw = pad(data_string.encode('utf-8'), 16)
    return aes.encrypt(raw)

if __name__ == "__main__":
    data_string = "loginTokenplatformandroidtimestamp1741921134712type1uuid4d46de23c1970252v4.74.5"
    res = aes_encrypt(data_string,'d245a0ba8d678a61')
    value = base64.encodebytes(res)
    result = value.replace(b"\n", b'')
    print(result)
    pass


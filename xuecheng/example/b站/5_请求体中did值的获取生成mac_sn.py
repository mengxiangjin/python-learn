import random
import string
import base64

def base64_encrypt(data_string):
    data_bytes = bytearray(data_string.encode('utf-8'))
    data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
    for i in range(1, len(data_bytes)):
        data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
    res = base64.encodebytes(bytes(data_bytes))
    return res.strip().strip(b"==").decode('utf-8')

def create_random_mac(sep=":"):
    """ 随机生成mac地址 """
    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
    return mac

def gen_sn():
    return "".join(random.sample("123456789" + string.ascii_lowercase, 10))


mac_string = create_random_mac(sep="")
sn = gen_sn()

prev_did = "{}|||{}".format(mac_string, sn)
print(prev_did)
import random
# pip3 install pycryptodome

from Crypto.Cipher import AES
import base64
# def gen_imei():
#     # 这个不够标准
#     return "".join(random.choices('0123456789abcdef', k=15))

def gen_imei():
    # # 生成随机的TAC（前六位）
    tac = ''.join(random.choices('0123456789', k=6))

    # 生成随机的FAC（接下来的两位）
    fac = ''.join(random.choices('0123456789', k=2))

    # 生成随机的SNR（后面的六位）
    snr = ''.join(random.choices('0123456789', k=6))

    # 计算校验位
    imei_base = tac + fac + snr
    imei_list = [int(digit) for digit in imei_base]
    check_digit = sum(imei_list[::-2] + [sum(divmod(d * 2, 10)) for d in imei_list[-2::-2]]) % 10

    # 生成最终的IMEI
    imei = imei_base + str((10 - check_digit) % 10)

    return imei


def header_str_to_dict(header_str):
    res = [item for item in header_str.split('\n')]
    res = res[1:len(res) - 1]
    d = {item.split('\t')[0]: item.split('\t')[1] for item in res}
    return d


# 加密的字符串，必须是固定长度，处理成固定长度
def pad_data(data):
    # 计算需要填充的字节数
    pad_len = AES.block_size - (len(data) % AES.block_size)
    # 使用填充字节进行填充
    padding = bytes([pad_len] * pad_len)
    padded_data = data + padding
    return padded_data
def encrypt_data(password):
    # 创建 AES 密码对象
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # 密钥（16 字节）
    key = b'6d6656a37cdb7977c10f6d83cab168e9'
    # 初始化向量（16 字节）
    iv = b'0000000000000000'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 填充数据
    padded_data = pad_data(password.encode('utf-8'))
    print(padded_data)
    # 加密数据
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode('utf-8')

if __name__ == '__main__':
    res=encrypt_data('lzy832857')  # m2mEwGdXWWo/3CsovxxQSA== 抓包抓到的
    print(res)                    # m2mEwGdXWWo/3CsovxxQSA== 自己加密
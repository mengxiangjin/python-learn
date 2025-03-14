### python 生成手机设备id号
import random


def gen_imei():
    # 这个不够标准
    return "".join(random.choices('0123456789abcdef', k=15))

print(gen_imei())
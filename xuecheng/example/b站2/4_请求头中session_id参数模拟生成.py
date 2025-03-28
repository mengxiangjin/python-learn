# -随机4个byte，转成16进制，不足2位用0补齐
import random

if __name__ == '__main__':
    session_id = "".join([hex(item)[2:] for item in random.randbytes(4)])git
    print(session_id)
    pass
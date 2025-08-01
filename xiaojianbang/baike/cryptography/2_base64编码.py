import base64
import string

base64_tables = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

#base64编码后的结果必须是4的倍数，不足的末尾=补
#base64编码将二进制6位分隔，获取每个二进制对应的十进制即为base64映射表的下标index，拿到具体对应的值


def base64_encode(datas):
    #定义base64字符表

    #输入的数据转换成二进制字符串进行拼接 08b：不足8位的高位以0补齐
    binary_data = ''.join(f'{data:08b}' for data in datas)

    # 补齐到6位的倍数
    padding = len(binary_data) % 6
    if padding != 0:
        binary_data += '0' * (6 - padding)

    # 每6位一组查表,int(binary_data[i:i + 6],2) 将2进制转换为10进制然后去查表
    result_str = ''
    for i in range(0, len(binary_data), 6):
        item = int(binary_data[i:i + 6], 2)
        result_str += base64_tables[item]
    #结果不足4的倍数需要填充=
    if len(result_str) % 4 != 0:
        result_str += '=' * (4 - len(result_str) % 4)
    return result_str


def base64_decode(data_str):
    data_str = data_str.replace('=', '')
    binary_data = ''
    for data in data_str:
        #6个位一位
        item = f'{int(base64_tables.index(data)):06b}'
        binary_data += item

    decoded_bytes = bytearray()

    #舍弃填充的0字符
    i = 0
    while i + 8 <= len(binary_data):
        item = binary_data[i:i + 8]
        decoded_bytes.append(int(item, 2))
        i += 8
    return decoded_bytes


if __name__ == '__main__':
    result_str = base64_encode('中文'.encode())
    print('自定义base64编码后---》', result_str)
    print('自定义base64解码后---》', base64_decode(result_str).decode())

    result_str = base64.b64encode("中文".encode()).decode()
    print('API base64编码后---》',result_str)
    print('API base64解码后---》',base64.b64decode(result_str).decode())



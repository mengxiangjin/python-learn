encoding_table = bytearray("0123456789ABCDEF","UTF-8")
decoding_table = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E',"F"]

# 十六进制编码
# 每个字符4bit，二个字符代表一个字节
def encode(datas):
    byte_array = bytearray(len(datas) * 2)
    for index,data in enumerate(datas):
        byte_array[index * 2] = encoding_table[data >> 4 & 0xf]
        byte_array[index * 2 + 1] = encoding_table[data & 0xf]
    return byte_array.decode()

def decode(datas):
    byte_array = bytearray(len(datas) // 2)
    for index in range(0,len(datas),2):
        high = decoding_table.index(datas[index])
        low = decoding_table.index(datas[index + 1])
        byte_array[index // 2] = (high << 4) | low
    return byte_array.decode()


if __name__ == '__main__':
    params = "中文".encode()
    encoding_result = encode(params)
    print('hex编码---》',encoding_result)
    print('hex解码---》',decode(encoding_result))


#     系统自带函数
    print(params.hex())
    print(bytes.fromhex(params.hex()).decode())

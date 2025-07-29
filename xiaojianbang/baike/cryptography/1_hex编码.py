encoding_table = bytearray("0123456789ABCDEF","UTF-8")
def encode(datas):
    byte_array = bytearray(len(datas) * 2)
    for index,data in enumerate(datas):
        byte_array[index * 2] = encoding_table[data >> 4 & 0xf]
        byte_array[index * 2 + 1] = encoding_table[data & 0xf]
    return byte_array.decode()

def decode(datas):
    byte_array = bytearray(len(datas) // 2)
    for index in range(0,len(datas),2):
        high = encoding_table[int(datas[index])]
        low = encoding_table[int(datas[index + 1])]
        byte_array[index // 2] = (high << 4) | low
    return byte_array


if __name__ == '__main__':
    params = "abc".encode()
    result = encode(params)
    print(result)
    result = decode(result)
    print(result)

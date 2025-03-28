import uuid

if __name__ == '__main__':
    random_uuid = str(uuid.uuid4()).replace('-', '')
    tem_res = f'XW{random_uuid[2]}{random_uuid[12]}{random_uuid[22]}{random_uuid}'.upper()
    print(tem_res)
    pass
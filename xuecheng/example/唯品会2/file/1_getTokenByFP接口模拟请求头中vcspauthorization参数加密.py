import hashlib

data_string ="da19a1b93059ff3609fc1ed2e04b0141vcspKey=4d9e524ad536c03ff203787cf0dfcd29"

# sha1加密
hash_object = hashlib.sha1()
hash_object.update(data_string.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7)

x = "da19a1b93059ff3609fc1ed2e04b0141"+arg7
# sha1加密
hash_object = hashlib.sha1()
hash_object.update(x.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7) 
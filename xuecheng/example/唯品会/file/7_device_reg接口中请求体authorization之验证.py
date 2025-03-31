import hashlib

data_string ="aee4c425dbb2288b80c71347cc37d04bapp_name=achievo_ad&app_version=7.83.3&channel=oziq7dxw:::&device=Pixel 2 XL&device_token=1f3fb32d-9f6a-3cb8-86d2-4c8dc359650b&manufacturer=Google&os_version=30&regPlat=0&regid=null&rom=Dalvik/2.1.0 (Linux; U; Android 11; Pixel 2 XL Build/RP1A.201005.004.A1)&skey=6692c461c3810ab150c9a980d0c275ec&status=1&vipruid=&warehouse=null"

# sha1加密
hash_object = hashlib.sha1()
hash_object.update(data_string.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7)

x = "aee4c425dbb2288b80c71347cc37d04b"+arg7
# sha1加密
hash_object = hashlib.sha1()
hash_object.update(x.encode('utf-8'))
arg7 = hash_object.hexdigest()
print(arg7) #hook出来的：f4f002d40e112a06ecdc04e54d5bf9c92c0477aa  自己计算的：f4f002d40e112a06ecdc04e54d5bf9c92c0477aa
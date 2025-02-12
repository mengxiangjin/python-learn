

import hashlib
md5=hashlib.md5()
md5.update(b'1234567') # fcea920f7412b5da7be0cf42b8c93759
print(md5.hexdigest()) # fcea920f7412b5da7be0cf42b8c93759
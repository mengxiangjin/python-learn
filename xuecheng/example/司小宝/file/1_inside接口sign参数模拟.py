import base64
import hashlib
import hmac
from urllib.parse import quote_plus

if __name__ == '__main__':
    key = "1KMrg0dfufc0wpnXEJacEQX1YEUYA0Ja"

    message = """POST
    1743996219711
    /inside.php"""

    message = message.encode('utf-8')  # 加密内容
    key = key.encode('utf-8')  # 加密的key
    result = hmac.new(key, message, hashlib.sha1).digest()
    print(result)
    _sig = base64.b64encode(result).decode()
    print(_sig)

    result = quote_plus(_sig)
    print(result)

#H2roit4xQZiWIKr5zYXcS%2BFesY4%3D  同hook后的结果一样


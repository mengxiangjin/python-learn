from flask import Flask, request, jsonify
import uuid
import hashlib

app = Flask(__name__)
##密码加密带签名
def get_md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()  # 16进制字符串

# 在进入视图函数执行之前，先做拦截--请求扩展，中间件
@app.before_request
def before():
    print(request.headers)
    ctime = request.headers.get('Ctime')
    sign = request.headers.get('Sign')
    print(ctime, sign)

    if get_md5(ctime) == sign:
        return None  # 正常的app请求，我们不拦截，继续往后走
    else:
        return jsonify({'code': 103, 'msg': "签名错误"})


@app.route('/login', methods=['POST'])
def login():
    # 打印出请求头,从请求头中取出ctime和sign，做个验证签名，如果不正确，我们就不允许这个请求继续访问
    # flask的请求扩展
    print(request.headers)
    # 1 验证签名是否正确
    username = request.form.get('username')
    new_sign = get_md5(username + "jin")
    sign = request.form.get('sign')
    if new_sign == sign:
        password = request.form.get('password')
        # 判断用户名或密码是否正确
        if username == 'admin' and password == get_md5('123456'):
            token = str(uuid.uuid4())
            # 返给前端数据
            return jsonify({'code': 100, 'msg': '登录成功', 'token': token})
        else:
            return jsonify({'code': 101, 'msg': '用户名或密码错误'})
    else:
        return jsonify({'code': 102, 'msg': '签名错误'})


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)

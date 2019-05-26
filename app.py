import time
import hashlib
from flask import Flask, jsonify, request, session

import hdu_crawl
from dao import userDao
from dao.userDao import create_user, User
from setting import ADMIN_PASSWORD


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hui1abUIU,W<>Q{}@^T&^$T()(@$!!_H1FBV3VHG.xcdfghSX045D4FG5H51ug44848416'


@app.route('/api/get_rank')
def get_rank():
    """
    获取排行榜
    """
    return jsonify(status=True, users=userDao.get_rank())


@app.route('/api/add')
def add():
    """
    添加用户
    :return:
    """
    name = request.args.get('name', type=str)
    account = request.args.get('account', type=str)
    motto = request.args.get('motto', type=str)
    if create_user(name, account, motto):
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg='账号已经存在！')


@app.route('/api/remove')
def remove_user():
    """
    删除用户
    """
    is_admin = session.get('is_admin', False)
    if is_admin:
        id = request.args.get('id', type=int)
        user = User()
        user.id = id
        user.remove()
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg='请先登录！')


@app.route('/api/login_admin')
def login_admin():
    """
    管理员登录
    :return:
    """
    pwd = request.args.get('pwd', type=str)

    def validate_token() -> bool:
        # 允许±10s之内误差
        time_token = int(time.time() / 10)
        print('time:' + str(time_token))
        for i in range(-1, 2, 1):
            token = str(time_token + i) + ADMIN_PASSWORD + str(time_token + i)
            m2 = hashlib.sha3_512(token.encode(encoding='utf-8')).hexdigest()
            print('time:' + str(time_token + i))
            print('m2:' + m2)
            if pwd == m2:
                return True
        return False

    if validate_token():
        session['is_admin'] = True
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg='密码错误！')


@app.route('/api/logout_admin')
def logout_admin():
    """
    登出管理员
    """
    session.clear()
    return jsonify(status=True)


@app.route('/api/confirm')
def confirm():
    """
    确认用户
    :return:
    """
    is_admin = session.get('is_admin', False)
    if is_admin:
        id = request.args.get('id', type=int)
        user = User()
        user.id = id
        user.status = user.FETCHING_STATUS
        user.confirm()
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg='请先登录！')


@app.route('/api/get_login_info')
def get_login_info():
    """
    获取登录信息
    :return:
    """
    is_admin = session.get('is_admin', False)
    return jsonify(status=True, is_admin=is_admin)


@app.route('/api/crawl_start')
def crawl_start():
    """
    开始滚版
    :return:
    """
    is_admin = session.get('is_admin', False)
    if is_admin:
        if hdu_crawl.crawl_status() == 'stopped':
            hdu_crawl.crawl_start()
            return jsonify(status=True)
        else:
            return jsonify(status=False, msg='已经在运行！')
    else:
        return jsonify(status=False, msg='请先登录！')


@app.route('/api/crawl_stop')
def crawl_stop():
    """
    停止滚榜
    :return:
    """
    is_admin = session.get('is_admin', False)
    if is_admin:
        if hdu_crawl.crawl_status() != 'stopped':
            hdu_crawl.crawl_stop()
            return jsonify(status=True)
        else:
            return jsonify(status=False, msg='已经停止！')
    else:
        return jsonify(status=False, msg='请先登录！')


@app.route('/api/crawl_status')
def crawl_status():
    """
    爬虫状态
    :return:
    """
    return jsonify(status=True, crawl_status=hdu_crawl.crawl_status())


# hdu_crawl.crawl_start()
if __name__ == '__main__':
    app.run()

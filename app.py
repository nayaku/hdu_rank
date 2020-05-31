import os
import time
import hashlib
from typing import Union, Optional

from flask import Flask, jsonify, request, session
from requests import HTTPError, TooManyRedirects, Timeout

import hdu_crawl
from dao import userDao
from dao.userConfig import UserConfig, save_user_config
from dao.userDao import create_user, User, exist_account, login_validate, exist_uid
import my_setting
import tempfile

my_setting.read_admin_password()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hui1abUIU,W<>Q{}@^T&^$T()(@$!!_H1FBV3VHG.xcdfghSX045D4FG5H51ug44848416'


@app.route('/api/get_rank')
def get_rank():
    """
    获取排行榜
    """
    return jsonify(status=True, users=userDao.get_rank(), notice=UserConfig.notice)


@app.route('/api/login')
def login():
    """
    登录
    :return:
    """
    if 'uid' in request.args:
        uid = request.args.get('uid', type=str)
        pwd = request.args.get('pwd', type=str)
        if exist_uid(uid):
            user = login_validate(uid, pwd)
            if user:
                session['user'] = user
                return jsonify(status=True, user=user)
            else:
                return jsonify(status=False, msg="账号与密码不匹配！")
        else:
            return jsonify(status=False, msg="账号不存在！")
    else:
        user = session.get('user', None)
        if user:
            return jsonify(status=True, user=user)
        else:
            return jsonify(status=False, mgs="请先登录！")


# def validate_account_without_get_request(account: str) -> Union[str, None]:
#     """
#     验证账号是否合法
#     :return: 合法返回None，否则返回原因。
#     """
#     try:
#         if hdu_crawl.exist_hdu_account(account):
#             if not User.exist_account(account):
#                 return None
#             else:
#                 return '账号已经存在！'
#         else:
#             return '输入的账号不正确！'
#     except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
#         return '连接杭电OJ失败！'
#

@app.route('/api/put_user')
def put_user():
    """
    添加或者修改用户
    :return:
    """
    user = User()
    for key in user.__dict__.keys():
        if key in request.args.keys():
            user.__dict__[key] = request.args.get(key)
    if user.uid:
        if not userDao.exist_uid(user.uid):
            return jsonify(status=False, mgs="账号不存在！")
    if user.account:
        if User.exist_account(user.account):
            return jsonify(status=False, mgs="账号已经存在！")
        else:
            try:
                if not hdu_crawl.exist_hdu_account(user.account):
                    return jsonify(status=False, mgs="账号不存在，请确认输入是否正确！")
            except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
                return jsonify(status=False, mgs="连接HDU失败！")

    if user.id:
        current_user: Optional[User, None] = None
        if 'admin' not in session.keys():
            current_user = session.get('user', None)
            if not current_user:
                return jsonify(status=False, mgs="请先登录！")
            else:
                if current_user.id != user.id:
                    return jsonify(status=False, mgs="不允许修改别人账号！")
        user.update()
        if current_user and current_user.id == user.id:
            session['user'] = user
    else:
        user.add()
    return jsonify(status=True)

@app.route('/api/validate_user')
def validate_user():
    filed = request.args.get('field',type=str)
    value = request.args.get('value')
    

# @app.route('/api/validate_user')
# def validate_account():
#     """
#     验证用户是否合法
#     :return:
#     """
#     account = request.args.get('account', type=str)
#     res = validate_account_without_get_request(account)
#     if not res:
#         return jsonify(status=True)
#     else:
#         return jsonify(status=False, msg=res)


@app.route('/api/add')
def add():
    """
    添加用户
    :return:
    """
    name = request.args.get('name', type=str)
    account = request.args.get('account', type=str)
    motto = request.args.get('motto', type=str)
    res = validate_account_without_get_request(account)
    if not res:
        create_user(name, account, motto)
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg=res)


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
            token = str(time_token + i) + my_setting.ADMIN_PASSWORD + str(time_token + i)
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


@app.route('/api/add_notice')
def add_notice():
    """
    添加留言
    :return:
    """
    is_admin = session.get('is_admin', False)
    if is_admin:
        notice = request.args.get('notice', type=str)
        UserConfig.notice = notice
        save_user_config()
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg='请先登录！')


# hdu_crawl.crawl_start()
if __name__ == '__main__':
    app.run()

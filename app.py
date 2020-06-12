import os
from typing import Optional

from flask import Flask, jsonify, request, session, url_for, render_template, redirect
from flask_cors import CORS
from requests import HTTPError, TooManyRedirects, Timeout

import hdu_crawl
from dao import user_dao, admin_dao, server_info
from dao.admin_dao import Admin
from dao.user_dao import User, exist_account, exist_uid

app = Flask(__name__, static_url_path='')
env_dist = os.environ
if 'FLASK_ENV' in env_dist and env_dist['FLASK_ENV'] == 'development':
    app.config['SECRET_KEY'] = 'ui1abUIU,W<>Q{}@^T&^$T()(@$!!_H1FBV3VHG.xcdfghSX045D4FG5H51ug44848416'
else:
    app.config['SECRET_KEY'] = 'hui1abUIU,W<>Q{}@^T&^$T()(@$!!_H1FBV3VHG.xcdfghSX045D4FG5H51ug44848416' + str(
        os.urandom(64))
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return redirect('/index.html')


@app.route('/api/get_rank')
def get_rank():
    """
    获取排行榜
    """
    return jsonify(status=True, users=user_dao.get_rank(), notice=server_info.get_notice(),
                   user=session.get('user', None), admin=session.get('admin', None),
                   crawl_status=hdu_crawl.crawl_status())


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
            user = user_dao.login(uid, pwd)
            if user:
                session['user'] = user.__dict__
                return jsonify(status=True, user=user.__dict__)
            else:
                return jsonify(status=False, msg="账号与密码不匹配！")
        else:
            return jsonify(status=False, msg="账号不存在！")
    else:
        user = session.get('user', None)
        if user:
            return jsonify(status=True, user=user)
        else:
            return jsonify(status=False, msg="请先登录！")


def __validate_user(field: str, value):
    """
    验证字段
    :param field:
    :param value:
    :return:如果成功则返回None，否则返回json。
    """
    if field == 'uid':
        if value is None or len(value) > 16:
            return jsonify(status=False, msg="账号名长度不正确！")
        if user_dao.exist_uid(value):
            return jsonify(status=False, msg="账号已被占用！")
    elif field == 'pwd':
        if value is None or len(value) > 128:
            return jsonify(status=False, msg="密码长度不正确！")
    elif field == 'class_name':
        if len(value) > 24:
            return jsonify(status=False, msg="班级名长度不正确！")
    elif field == 'name':
        if value is None or len(value) > 16:
            return jsonify(status=False, msg="姓名长度不正确！")
    elif field == 'motto':
        if len(value) > 255:
            return jsonify(status=False, msg="格言长度不正确！")
    elif field == 'account':
        if len(value) > 64:
            return jsonify(status=False, msg="杭电账号名过长！")
        if exist_account(value):
            return jsonify(status=False, msg="杭电账号已经被占用！")
        else:
            try:
                if not hdu_crawl.exist_hdu_account(value):
                    return jsonify(status=False, msg="杭电账号不存在，请确认输入是否正确！")
            except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
                return jsonify(status=False, msg="连接HDU失败！")
    elif field == 'status':
        if value:
            if value not in (User.UNCHECKED_STATUS, User.FETCHING_STATUS, User.ACTIVE_STATUS):
                return jsonify(status=False, msg="不正确的状态！")
    return None


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
            if key == 'id':
                user.id = int(user.id)

    if user.id:
        for item in user.__dict__.items():
            if item[1]:
                res = __validate_user(item[0], item[1])
                if res:
                    return res
        admin = session.get('admin', None)
        current_user = session.get('user', None)
        if not (admin or current_user):
            return jsonify(status=False, msg="请先登录！")
        if not admin and current_user['id'] != user.id:
            return jsonify(status=False, msg="没有权限！")
        if user.status and not admin:
            return jsonify(status=False, msg="没有权限！")
        user.update()
        if current_user:
            if user.pwd:
                session.clear()
            else:
                for key in current_user.keys():
                    if user.__dict__[key]:
                        current_user[key] = user.__dict__[key]
                session['user'] = current_user
    else:
        for item in user.__dict__.items():
            res = __validate_user(item[0], item[1])
            if res:
                return res
        user.add()
    return jsonify(status=True)


@app.route('/api/validate_user')
def validate_user():
    """
    验证字段
    :return:
    """
    filed = request.args.get('field', type=str)
    value = request.args.get('value')
    val_res = __validate_user(filed, value)
    if val_res:
        return val_res
    else:
        return jsonify(status=True)


@app.route('/api/logout')
def logout():
    session.clear()
    return jsonify(status=True)


@app.route('/api/remove_user')
def remove_user():
    """
    删除用户
    """
    id = request.args.get('id', type=int)
    user = User()
    user.id = id

    admin = session.get('admin', None)
    current_user = session.get('user', None)
    if not admin:
        if not current_user:
            return jsonify(status=False, msg='请先登录！')
        else:
            if current_user['id'] != user.id:
                return jsonify(status=False, msg='不能删除别人账号！')
    user.remove()
    if not admin and current_user['id'] == user.id:
        session.clear()
    return jsonify(status=True)


@app.route('/api/login_admin')
def login_admin():
    """
    管理员登录
    :return:
    """

    if 'uid' in request.args.keys():
        uid = request.args.get('uid', type=str)
        pwd = request.args.get('pwd', type=str)

        if not admin_dao.exist_uid(uid):
            return jsonify(status=False, msg='账号不存在！')
        admin = admin_dao.login(uid, pwd)
        if not admin:
            return jsonify(status=False, msg='密码错误！')
        session['admin'] = admin.__dict__
        return jsonify(status=True, admin=admin.__dict__)
    else:
        admin = session.get('admin', None)
        if not admin:
            return jsonify(status=False, msg='请先登录！')
        return jsonify(status=True, admin=admin)


@app.route('/api/list_admin')
def list_admin():
    """
    管理员列表
    :return:
    """
    admin: Optional[Admin, None]
    admin = session.get('admin', None)
    if admin:
        if admin['is_super']:
            return jsonify(status=True, admins=admin_dao.get_admin_list())
        else:
            return jsonify(status=False, msg="没有权限！")
    else:
        return jsonify(status=False, msg='请先登录！')


def __validate_admin(field: str, value):
    if field == 'uid':
        if value is None or len(value) > 16:
            return jsonify(status=False, msg="字段不正确！")
        if admin_dao.exist_uid(value):
            return jsonify(status=False, msg="账号名已存在！")
    if field == 'pwd':
        if value is None or len(field) > 128:
            return jsonify(status=False, msg="字段长度不正确！")


@app.route('/api/validate_admin')
def validate_admin():
    admin = session.get('admin', None)
    if admin:
        filed = request.args.get('field', type=str)
        value = request.args.get('value')
        val_res = __validate_admin(filed, value)
        if val_res:
            return val_res
        else:
            return jsonify(status=True)
    else:
        return jsonify(status=False, msg="请先登录！")


@app.route('/api/put_admin')
def put_admin():
    current_admin = session.get('admin', None)
    admin = Admin()
    for key in admin.__dict__.keys():
        if key in request.args.keys():
            admin.__dict__[key] = request.args.get(key)
            if key == 'id':
                admin.id = int(admin.id)

    if current_admin:
        if admin.id:
            # 更新
            if admin.id == current_admin['id'] or current_admin['is_super']:
                if admin.uid:
                    res = __validate_admin('uid', admin.uid)
                    if res:
                        return res
                elif admin.pwd:
                    res = __validate_admin('pwd', admin.pwd)
                    if res:
                        return res
                admin.update()
                if admin.id == current_admin['id']:
                    session.clear()
            else:
                return jsonify(status=False, msg="没有权限！")
        else:
            # 创建
            if not current_admin['is_super']:
                return jsonify(status=False, msg="没有权限！")
            for item in admin.__dict__.items():
                if item[1]:
                    res = __validate_admin(item[0], item[1])
                    if res:
                        return res
            admin.add()
    else:
        return jsonify(status=False, msg="请先登录！")
    return jsonify(status=True)


@app.route('/api/remove_admin')
def remove_admin():
    id = request.args.get('id', type=int)
    admin = session.get('admin', None)
    if not admin:
        return jsonify(status=False, msg="请先登录！")
    if not admin['is_super']:
        return jsonify(status=False, msg="没有权限！")
    if id == admin['id']:
        return jsonify(status=False, msg="请勿删除自己！")
    admin_dao.remove_admin(id)
    return jsonify(status=True)


@app.route('/api/crawl_start')
def crawl_start():
    """
    开始滚版
    :return:
    """
    admin = session.get('admin', None)
    if admin:
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
    admin = session.get('admin', None)
    if admin:
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
    admin = session.get('admin', None)
    if admin:
        notice = request.args.get('notice', type=str)
        server_info.set_notice(notice)
        return jsonify(status=True)
    else:
        return jsonify(status=False, msg='请先登录！')


# hdu_crawl.crawl_start()
if __name__ == '__main__':
    app.run()

from typing import List, Union, Tuple, Optional

import pymysql

from dao.dao import get_connect


class User:
    UNCHECKED_STATUS = 'unchecked'
    FETCHING_STATUS = 'fetching'
    ACTIVE_STATUS = 'active'

    def __init__(self) -> None:
        self.id = None
        self.uid = None
        self.pwd = None
        self.class_name = None
        self.name = None
        self.motto = None
        self.account = None
        self.solved_num = None
        self.status = None
        self.html = None


    # @staticmethod
    # def validate_account_in_hdu(account: str) -> bool:
    #     """
    #     账号是否在杭电
    #     :return:
    #     """
    #     if hdu_crawl.exist_hdu_account(account):
    #         return True
    #     else:
    #         return False
    def update(self) -> bool:
        """
        更新用户
        """
        if not self.id:
            return False
        else:
            parameters = []
            sql_request_string = []
            for filed in self.__dict__.items():
                if filed[1]:
                    sql_request_string.append(str.format("`{0}`=%s", filed[0]))
                    parameters.append(filed[1])
            sql = '''UPDATE users SET ''' + ','.join(sql_request_string) + ''' WHERE id=%s'''
            parameters.append(self.id)
            connect = get_connect()
            with connect.cursor() as cursor:
                cursor.execute(sql, tuple(parameters))
                connect.commit()
            return True

    def confirm(self) -> None:
        """
        确认用户
        """
        sql = '''UPDATE users SET `status`='fetching' WHERE id=%s'''
        connect = get_connect()
        with connect.cursor() as cursor:
            cursor.execute(sql, (self.id,))
            connect.commit()

    def remove(self) -> None:
        """
        删除用户
        """
        sql = '''DELETE FROM users WHERE id=%s'''
        connect = get_connect()
        with connect.cursor() as cursor:
            cursor.execute(sql, (self.id,))
            connect.commit()

    def add(self):
        """
        添加用户到数据库
        :return:
        """

        self.solved_num = 0
        self.status = User.UNCHECKED_STATUS
        sql = '''INSERT INTO users(uid,pwd,class_name,`name`,account,motto,html) VALUES(%s,%s,%s,%s,%s,%s,%s)'''
        connect = get_connect()
        with connect.cursor() as cursor:
            cursor.execute(sql, (self.uid, self.pwd, self.class_name, self.name, self.account, self.motto, self.html))
            connect.commit()
            self.id = cursor.lastrowid


def exist_account(account: str) -> bool:
    """
    判断账号是否已经被占用
    :param account:
    :return: 被占用返回True，否则返回False
    """
    sql = '''SELECT 1 FROM `users` WHERE account = %s LIMIT 1'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, (account,))
        if cursor.fetchone():
            return True
    return False


def get_fetching_list() -> List[User]:
    """
    所有等待获取的用户列表
    :return:
    """
    sql = '''SELECT id,`name`,account,motto,solved_num,`status` FROM `users` WHERE `status`!= 'unchecked' '''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        user_list = []
        for row in rows:
            user = User()
            (user.id, user.name, user.account, user.motto, user.solved_num, user.status) = row
            user_list.append(user)

    return user_list


def get_rank() -> Tuple[tuple]:
    """
    获取排行榜
    :return:
    """
    sql = '''SELECT users.id, users.uid, users.pwd, users.class_name, users.`name`, users.motto,users.account, \
    users.solved_num, users.`status`, users.html FROM users'''
    connect = get_connect()
    with connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


def login(uid: str, pwd: str) -> Optional[User]:
    """
    用户登录
    :param uid:
    :param pwd:
    :return:
    """
    sql = '''SELECT users.id, users.uid, users.class_name, users.`name`, users.motto, users.account, users.solved_num \
    , users.`status`, users.html FROM users WHERE uid=%s AND pwd=%s LIMIT 1'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, (uid, pwd))
        row = cursor.fetchone()
        if row:
            user = User()
            user.id, user.uid, user.class_name, user.name, user.motto, user.account, user.solved_num, user.status, user.html = row
            return user
        else:
            return None


def exist_uid(uid: str) -> bool:
    """
    判断用户名是否存在
    :param uid:
    :return:
    """
    sql = '''SELECT 1 FROM users WHERE uid = %s LIMIT 1'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, (uid,))
        if cursor.fetchone():
            return True
        else:
            return False

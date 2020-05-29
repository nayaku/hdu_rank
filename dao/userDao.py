from typing import List, Union, Tuple

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

    def update(self) -> None:
        """
        更新用户
        """
        if not self.id:
            raise Exception("Need id when update.")
        else:
            parameters = []
            sql_request_string = []
            for filed in self.__dict__.items():
                if filed[1]:
                    sql_request_string.append(str.format("`{0}`=%s", filed[0]))
                    parameters.append(filed[1])
            sql = '''UPDATE users SET '''+','.join(sql_request_string)+''' WHERE id=%s'''
            parameters.append(self.id)
            connect = get_connect()
            with connect.cursor() as cursor:
                cursor.execute(sql, tuple(parameters))
                connect.commit()

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


def exist_user(account: str) -> bool:
    '''
    判断账号是否已经被占用
    :param account:
    :return: 被占用返回True，否则返回False
    '''
    sql = '''SELECT 1 FROM `users` WHERE account = %s LIMIT 1'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, (account,))
        if cursor.fetchone():
            return True
    return False


def create_user(name: str, account: str, motto: str) -> User:
    """
    创建用户
    :param name: 姓名
    :param account: 账号
    :param motto: 格言
    :return: 成功返回User
    """
    user = User()
    user.name = name
    user.account = account
    user.motto = motto
    # sql = '''SELECT 1 FROM `users` WHERE account = %s LIMIT 1'''
    connect = get_connect()
    # with connect.cursor() as cursor:
    #     cursor.execute(sql, (user.account,))
    #     if cursor.fetchone():
    #         return False
    sql = '''INSERT INTO users(`name`,account,motto,solved_num,`status`) VALUES(%s,%s,%s,%s,%s)'''

    with connect.cursor() as cursor:
        cursor.execute(sql, (user.name, user.account, user.motto, user.solved_num, user.status))
        connect.commit()
        user.id = cursor.lastrowid
    return user


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
    sql = '''SELECT users.`name`, users.account, users.motto, users.solved_num, users.`status`, users.id FROM users ORDER BY solved_num DESC '''
    connect = get_connect()
    with connect.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

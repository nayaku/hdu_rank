from typing import Optional, List, Tuple

from dao.dao import get_connect


class Admin:
    def __init__(self):
        self.id = None
        self.uid = None
        self.is_super: Optional[bool] = None
        self.pwd = None

    def add(self):
        """
        添加管理员
        :return:
        """
        sql = '''INSERT INTO admins(uid,is_super,pwd) VALUES(%s, %s, %s)'''
        connect = get_connect()
        with connect.cursor() as cursor:
            cursor.execute(sql, (self.uid, self.is_super, self.pwd))
            connect.commit()
            self.id = cursor.lastrowid

    def update(self):
        """
        更新用户
        """
        parameters = []
        sql_request_string = []
        for filed in self.__dict__.items():
            if filed[1]:
                sql_request_string.append(str.format("`{0}`=%s", filed[0]))
                parameters.append(filed[1])
        sql = '''UPDATE admins SET ''' + ','.join(sql_request_string) + ''' WHERE id=%s'''
        parameters.append(self.id)
        connect = get_connect()
        with connect.cursor() as cursor:
            cursor.execute(sql, tuple(parameters))
            connect.commit()


def login(uid: str, pwd: str) -> Optional[Admin]:
    """
    登录
    :return:
    """
    sql = '''SELECT admins.id, admins.uid, admins.is_super FROM admins WHERE uid=%s AND pwd=%s LIMIT 1'''
    connect = get_connect()

    with connect.cursor() as cursor:
        cursor.execute(sql, (uid, pwd))
        row = cursor.fetchone()
        if row:
            admin = Admin()
            admin.id, admin.uid, admin.is_super = row
            return admin
        else:
            return None


def exist_uid(uid: str) -> bool:
    """
    判断uid是否已经存在
    :param uid:
    :return:
    """
    sql = '''SELECT 1 FROM admins WHERE uid=%s LIMIT 1'''
    connect = get_connect()

    with connect.cursor() as cursor:
        cursor.execute(sql, (uid,))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False


def get_admin_list() -> Tuple[tuple]:
    """
    获取管理员列表
    :return:
    """
    sql = '''SELECT admins.id, admins.uid, admins.is_super FROM admins'''
    connect = get_connect()

    with connect.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows


def remove_admin(id: int):
    """
    删除管理员
    :param id:
    :return:
    """
    sql = '''DELETE FROM admins WHERE id=%s'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, (id,))
        connect.commit()

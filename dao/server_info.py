from dao.dao import get_connect


def get_notice():
    """
    获取公告
    :return:
    """
    sql = '''SELECT notice FROM server_infos LIMIT 1'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, )
        return cursor.fetchone()[0]


def set_notice(notice: str):
    """
    设置公告
    :return:
    """
    sql = '''UPDATE server_infos SET notice=%s WHERE id=1'''
    connect = get_connect()
    with connect.cursor() as cursor:
        cursor.execute(sql, (notice,))
        connect.commit()

from pymysql import Connection, connect

from my_setting import *

_connect: Connection = None


def get_connect() -> Connection:
    global _connect

    if not _connect:
        _connect = connect(host=DB_ADDR, user=DB_USER, passwd=DB_PASSWORD, database=DB_NAME)
    # 掉线重连
    _connect.ping(reconnect=True)
    return _connect

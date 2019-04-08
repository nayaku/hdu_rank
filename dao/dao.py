from pymysql import Connection, connect

from setting import *

_connect: Connection = None


def get_connect() -> Connection:
    global _connect
    if not _connect:
        _connect = connect(DB_ADDR, DB_USER, DB_PASSWORD, DB_NAME)
    return _connect



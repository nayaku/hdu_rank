# 主循环间隔时间(s)
import os
import random
import string

MAIN_LOOP_INTERVAL = 5
# 爬取页面休息时间(s)
CRAWL_SLEEP_TIME = 1
# HDU的网址
HDU_URL = 'http://acm.hdu.edu.cn'
# 数据库地址
DB_ADDR = '127.0.0.1'
# 数据库用户名
DB_USER = 'hr'
# 数据库密码
DB_PASSWORD = 'hr@hr'
# 数据库名称
DB_NAME = 'hdu_rank'
# 管理员密码
ADMIN_PASSWORD = None
print("载入设置")


def read_admin_password() -> None:
    """
    读取管理员密码
    """
    global ADMIN_PASSWORD
    if not os.path.exists('admin.key'):
        ADMIN_PASSWORD = ''.join(random.sample(string.ascii_letters + string.digits + '_!-~`@#$%^&*()+/*<>?.:;[]{}', 8))
        with open('admin.key', 'w') as f:
            f.write(ADMIN_PASSWORD)
            print('管理员密码不存在，已经保存密码到目录下的admin.key文件夹中，密码为：')
            print(ADMIN_PASSWORD)
    else:
        with open('admin.key', 'r') as f:
            ADMIN_PASSWORD = f.read()


# test
# if __name__ == '__main__':
read_admin_password()

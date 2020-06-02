import json
import os
import pickle

'''
用户配置
'''


class _UserConfig:

    def __init__(self):
        # 公告
        self.notice = ""


UserConfig = _UserConfig()


def get_user_config_path():
    """
    获取配置文件的路径
    :return: str
    """
    if os.name == 'nt':
        home = os.path.expanduser('~')
    else:
        home = '/tmp'
    home = os.path.join(home, 'hdu_rank')
    if not os.path.isdir(home):
        os.mkdir(home)
    config_path = os.path.join(home, 'config.dat')
    return config_path


def read_user_config() -> None:
    '''
    读取用户配置
    windows用户默认储存在user目录下，linux则是tmp目录。
    :return:
    '''
    global UserConfig
    config_path = get_user_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'rb') as f:
            UserConfig = pickle.load(f)
            print('读取用户配置完成！ ')
    else:
        print("配置文件不存在！")


def save_user_config() -> None:
    """
    保存用户配置
    """
    config_path = get_user_config_path()
    with open(config_path, 'wb') as f:
        pickle.dump(UserConfig, f)
        print('配置文件写入完成！')


# 程序启动以后自动加载配置
read_user_config()

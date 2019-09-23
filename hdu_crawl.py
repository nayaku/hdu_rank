import re
import threading
import time
import traceback
from threading import Thread
from typing import Optional, Callable, Any, Iterable, Mapping, List, Union

from requests import TooManyRedirects, Timeout, HTTPError

from dao.userDao import get_fetching_list, User
from my_setting import *

import requests


def crawl_page(url: str) -> str:
    """
    爬取页面
    :param url:
    :return:
    """
    time.sleep(CRAWL_SLEEP_TIME)
    # headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    resp = requests.get(url)
    print(f'GET[{resp.status_code}]:{url}')
    resp.raise_for_status()
    return resp.text


def exist_hdu_account(account: str, content: Union[str, None] = None) -> bool:
    """
    判断杭电账号是否正确存在
    :param account:
    :param content: 网页内容，如果未设置则自动爬取
    :return: 存在返回True，否则返回False
    """
    if not content:
        url = HDU_URL + '/userstatus.php?user=' + account
        content = crawl_page(url)
    pattern = re.compile('No such user.', re.S)
    res = re.search(pattern, content)
    return res is None


def crawl_user_info(user: User) -> bool:
    """
    爬取用户题数
    :param user:
    :return 如果变动返回True，否则返回False
    """
    url = HDU_URL + '/userstatus.php?user=' + user.account
    content = crawl_page(url)

    pattern = re.compile('Problems Solved</td><td align=center>(.*?)<', re.S)
    item = re.findall(pattern, content)
    solved_num = int(item[0])
    if solved_num != user.solved_num:
        user.solved_num = solved_num
        user.update()
        return True
    else:
        return False


class CrawlThread(Thread):

    def __init__(self, ) -> None:
        Thread.__init__(self)
        self.__stop_signal = False
        self.status = 'runnable'

    def run(self) -> None:
        self.status = 'running'
        print('爬虫线程启动！')
        while True:
            if self.__stop_signal:
                self.status = 'stopped'
                return
            try:
                crawl_page(HDU_URL)
            except (ConnectionError, HTTPError, Timeout, TooManyRedirects):
                print('连接杭电OJ失败！爬虫线程退出！')
                self.status = 'stopped'
                return

            users = get_fetching_list()
            for user in users:
                try:
                    crawl_user_info(user)
                    if self.__stop_signal:
                        self.status = 'stopped'
                        return
                except Exception as e:
                    traceback.print_exc()

            self.status = 'sleeping'
            time.sleep(MAIN_LOOP_INTERVAL)

    def stop(self):
        self.__stop_signal = True


# 线程池
crawl_pool: List[CrawlThread] = []


def crawl_start() -> None:
    if len(crawl_pool) == 0:
        crawl_pool.append(CrawlThread())
    else:
        crawl_pool[0] = CrawlThread()
    crawl_pool[0].setDaemon(True)
    crawl_pool[0].start()


def crawl_stop() -> None:
    if len(crawl_pool) > 0:
        crawl_pool[0].stop()


def crawl_status() -> str:
    if len(crawl_pool) > 0:
        return crawl_pool[0].status
    else:
        return 'stopped'


if __name__ == '__main__':
    # crawl_page('http://acm.hdu.edu.cn/userstatus.php?user=736248591')
    print (exist_hdu_account("736248591"))

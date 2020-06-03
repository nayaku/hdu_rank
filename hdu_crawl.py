import re
import threading
import time
import traceback
from threading import Thread
from typing import Optional, Callable, Any, Iterable, Mapping, List, Union

from requests import TooManyRedirects, Timeout, HTTPError
from requests.adapters import HTTPAdapter

from dao.user_dao import get_fetching_list, User
from my_setting import *

import requests


def crawl_page(url: str, timeout: int = 8, max_retries: int = 5) -> str:
    """
    爬取页面
    :param url:
    :param max_retries:
    :param timeout:
    :return:
    """
    # headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    # 爬取一次就关闭连接。设置超时和最大尝试次数
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=max_retries))
    s.mount('https://', HTTPAdapter(max_retries=max_retries))
    s.keep_alive = False
    resp = s.get(url, timeout=timeout)
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
        content = crawl_page(url, 3, 1)
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
                    if self.__stop_signal:
                        self.status = 'stopped'
                        return
                    crawl_user_info(user)
                    if self.__stop_signal:
                        self.status = 'stopped'
                        return
                    time.sleep(CRAWL_SLEEP_TIME)
                except Exception as e:
                    traceback.print_exc()

            self.status = 'sleeping'
            for i in range(1, MAIN_LOOP_INTERVAL):
                if self.__stop_signal:
                    self.status = 'stopped'
                    return
                time.sleep(1)

    def stop(self):
        self.__stop_signal = True


# 线程池
crawl_thread: Optional[CrawlThread] = None


def crawl_start() -> None:
    global crawl_thread
    crawl_thread = CrawlThread()
    crawl_thread.setDaemon(True)
    crawl_thread.start()


def crawl_stop() -> None:
    crawl_thread.stop()


def crawl_status() -> str:
    if crawl_thread:
        return crawl_thread.status
    else:
        return 'stopped'

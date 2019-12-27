import time

from requests.adapters import HTTPAdapter


import requests


def crawl_page(url: str, timeout: int = 8, max_retries: int = 5) -> str:
    """
    爬取页面
    :param url:
    :param max_retries:
    :param timeout:
    :return:
    """
    time.sleep(CRAWL_SLEEP_TIME)
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

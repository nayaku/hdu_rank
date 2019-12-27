import json

from time import sleep

import requests

session = requests.Session()
headers = {'X-Requested-With': 'XMLHttpRequest'}


def post(url: str, data=None, files=None) -> dict:
    sleep(0.2)
    url = url
    r = session.post(url, data=data, headers=headers, files=files)
    print(r.url)
    if r.status_code >= 500:
        # 把返回的错误页面写入文件
        with open('respon.html', 'w', encoding='utf8') as error_file:
            error_file.write(r.text)
        raise Exception(r.text)
    if r.text:
        json_result = json.loads(r.text)
        print(json_result)
        return json_result


def login(uid: str, pwd: str) -> None:
    post('User/login', {
        'u': uid,
        'pwd': pwd,
        'method': 'account'})


def logout() -> None:
    post('User/logout')

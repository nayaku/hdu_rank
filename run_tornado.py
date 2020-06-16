#!/usr/bin/python3
import platform
import sys

import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app

port = 5000
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(port)
os_string = platform.system()
print('Running on ' + os_string)
if os_string != "Windows":
    http_server.start(0)
print('Running on http://127.0.0.1:%s/ (Press CTRL+C to quit)' % (port,))
IOLoop.instance().start()

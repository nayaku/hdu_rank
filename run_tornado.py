#!/usr/bin/python3
import platform
import sys

import asyncio

from tornado.options import define

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import app

address = '0.0.0.0'
port = 80
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(port, address)
os_string = platform.system()
print('Running on ' + os_string)
output_string = 'Running on http://%s:%s (Press CTRL+C to quit)' % (address, port)
print(output_string)
if os_string != "Windows":
    http_server.start(0)
IOLoop.instance().start()

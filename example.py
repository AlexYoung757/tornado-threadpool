#coding:utf-8
import time
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from thread_pool import in_thread_pool, in_ioloop, blocking
from tornado.options import define, options

define("port", default=8002, help="run on the given port", type=int)

class TestThreadPool(tornado.web.RequestHandler):
    def get(self):
        self.blocking_method(self.sleep)
        logging.info('end')
        self.write('go')

    @in_thread_pool
    def blocking_method(self,callback):
        logging.info('pass thread_pool')
        callback()

    def sleep(self):
        time.sleep(5)
        logging.info('this func is sleep')

class TestIoloop(tornado.web.RequestHandler):
    def get(self):
        self.blocking_method(self.sleep)
        logging.info('end')
        self.write('go')

    @in_ioloop
    def blocking_method(self,callback):
        logging.info('pass in_ioloop')
        callback()

    def sleep(self):
        time.sleep(5)
        logging.info('this func is sleep')

class TestBlocking(tornado.web.RequestHandler):
    def get(self):
        self.blocking_method(self.sleep)
        logging.info('end')
        self.write('TestBlocking')

    @blocking
    def blocking_method(self,callback):
        logging.info('pass blocking')
        callback()

    def sleep(self):
        time.sleep(5)
        logging.info('this func is sleep')

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/threadpool", TestThreadPool),
            (r"/ioloop",TestIoloop ),
            (r"/blocking", TestBlocking), ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

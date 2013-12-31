#!/usr/bin/env python
# -*- coding: utf-8 -*-
# example of Tornado + REST

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.web import *

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    #@asynchronous
    def get_current_user(self):
        r=self.get_secure_cookie("user")
        print "get_secure_cookie(user)=",r
        return r

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    #@asynchronous
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')

    @asynchronous
    def post(self):
        r=self.get_argument("name")
        print "self.get_argument(name)=",r
        self.set_secure_cookie("user", r)
        self.redirect("/")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
        ]
        settings = {
            #"template_path":'/root/sb',
            #"static_path":'/root/sb',
            #"debug":'/root/sb',
            "cookie_secret": '2137089jkvafkasiufyu129uq239r',
            "login_url": "/login"
        }
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()

#!/usr/bin/python
#coding=utf-8
import tornado.httpserver  
import tornado.ioloop  
import tornado.web  
import tornado.options  
import os.path  
import time
import json

import MySQLdb
import DBUtils.PersistentDB
from DBHelper import mysql

DB = mysql('localhost','dabao','a123456','pk10',3306)

from tornado.options import define, options  
define("port", default=8090, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):  
    def get(self):  
        self.render('login.html')  
    def post(self):  
        user_name = self.get_argument("username");
        password = self.get_argument("password");
        if cmp(user_name, "dabaojian")  == 0 and cmp(password, "123456") == 0:
            self.set_secure_cookie("username", self.get_argument("username"), expires_days=None)
            self.redirect("/")  
        else:
            self.redirect('/login')

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        sql = "select * from pk10_plan_daxiao_3"
        ret = DB.select(sql)
        data_daxiao = []
        self.write("<p>刷新抓取结果，验证稳定，准确</p>")
        self.write("<p>大小</p>")

        for r in ret: 
            st = r['plan']
            self.write("<li>" + st + "</li>")

        self.write("<p>单双</p>")
        sql = "select * from pk10_plan_danshuang_3"

        ret = DB.select(sql)
        for r in ret: 
            st = r['plan']
            self.write("<li>" + st + "</li>")

class QueryPlanHandler(BaseHandler):
    def get(self):
        type = self.get_argument('type')
        cycle = self.get_argument('cycle')
        sql = "select * from pk10_plan_%s_%s order by id desc limit 2" % (type, cycle)
        ret = DB.select(sql)
        if len(ret) == 2:
            current = ret[0]
            prev = ret[1]
            state = "success"
        elif len(ret) == 1:
            current = ret[0]
            prev = "null"
            state = "success"
        else:
            current = "null"
            prev = "null"
            state = "failed"
            
        result = {'state': state, 'current': current, 'prev': prev}
        self.write(json.dumps(result, ensure_ascii=False, encoding='UTF-8'))

class LogoutHandler(BaseHandler):  
    @tornado.web.authenticated
    def post(self):  
        if (self.get_argument("logout", None)):  
            self.clear_cookie("username")  
        self.redirect("/")  

if __name__ == "__main__":  
    tornado.options.parse_command_line()  
    settings = {  
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "login_url": "/login"  
    }  
    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/queryplan', QueryPlanHandler),
        (r'/logout', LogoutHandler)
    ],debug= True,**settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

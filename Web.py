#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Modified

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid
from time import sleep

from tornado.options import define, options

from json import dumps

# filehandler = logging.FileHandler(
#     filename = 'Logs/Web.log',
#     mode = 'a',
#     encoding = None,
#     delay = False
# )
# filehandler.setLevel(logging.INFO)

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/html", HtmlHandler),
            (r"/data", DataHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "GUI/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "GUI/static"),
            xsrf_cookies=True,
            debug=options.debug,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class HtmlHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        HtmlHandler.clients.add(self)

    def on_close(self):
        HtmlHandler.clients.remove(self)

    def on_message(self, message):
        # logging.info("got html message %r", message)
        pass

    @classmethod
    def send_updates(cls, html_file):
        # logging.info("sending html to %d clients", len(cls.clients))
        for clients in cls.clients:
            try:
                clients.write_message(html_file.read())
            except:
                # logging.error("Error sending html", exc_info=True)
                pass

class DataHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        DataHandler.clients.add(self)

    def on_close(self):
        DataHandler.clients.remove(self)

    def on_message(self, message):
        # logging.info("got data message %r", message)
        pass

    @classmethod
    def send_updates(cls, data):
        # logging.info("sending data to %d clients", len(cls.clients))
        for clients in cls.clients:
            try:
                clients.write_message(dumps(data))
            except:
                # logging.error("Error sending data", exc_info=True)
                pass

class CallbackContainer():

    def __init__(self, callback, IOLoop):
        self.i = 0
        self.IOLoop = IOLoop
        if (callable(callback)):
            self.callback = callback
            self.IOLoop.current().add_callback(self.call)
        else:
            raise TypeError("passed variable must be callable")

    def call(self):
        self.callback()
        self.IOLoop.current().add_callback(self.call)
        self.i += 1

i = 0

def update_all(data):
    global i
    data["index"] = i
    if data["State"] == "Options":
        HtmlHandler.send_updates(open("GUI/templates/OptionsManager.html"))
    elif data["State"] == "Game":
        HtmlHandler.send_updates(open("GUI/templates/X01.html"))
    elif data["State"] == "Winner":
        HtmlHandler.send_updates(open("GUI/templates/WinnerManager.html"))

    DataHandler.send_updates(data)
    i +=1

def web_start(callback=None):
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    if (callback != None):
        CallbackContainer(callback, tornado.ioloop.IOLoop)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    def snd():
        sleep(2)
        fl = open("GUI/templates/X01.html")
        HtmlHandler.send_updates(fl)
        # DataHandler.send_updates()
    web_start(snd)

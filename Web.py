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
"""Simplified chat demo for websockets.

Authentication, error handling, etc are left as an exercise for the reader :)
"""

from functools import partial
import time

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

# alldata = [
#     {'body': u'{"State":0,"Data":[["x01","BattleShip"],["Option 1","Option 2","Option 3"],["301","501","701"]]}'},
#     {'body': u'{"State":1,"Data":{"Heading":["Battlefield","Round","Throw"],"PlayerNames":["Scott","Trent","Ryan"],"PlayerScores":["ScottScore","TrentScore","RyanScore"]}}'},
#     {'body': u'{"State":2,"Data":{"Heading":["X01","Round","Throw"],"PlayerNames":["Scott","Trent","Ryan"],"PlayerScores":["ScottScore","TrentScore","RyanScore"]}}'},
#     {'body': u'{"State":3,"Data":["Scott"]}'}
# ]
state = {'body': u'{"State":0,"Data":[["x01","BattleShip"],["Option 1","Option 2","Option 3"],["301","501","701"]]}'},



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "GUI/templates"),
            static_path=os.path.join(os.path.dirname(__file__), "GUI/static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=ChatSocketHandler.cache)

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    global state
    cache = state
    cache_size = 200

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        logging.info("connection opened")
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        logging.info("connection closed")
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending message to %d waiters", len(cls.waiters))
        logging.info("State: %s", str(state))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = {
            "id": str(uuid.uuid4()),
            "body": parsed["body"],
            }
        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)

# def doit():
#     global itera
#     global state
#     global alldata
#     ChatSocketHandler.send_updates(state)
#     time.sleep(3)
#     tornado.ioloop.IOLoop.current().add_callback(partial(doit))
#     itera += 1
#     state = alldata[itera % len(alldata)]
#
# itera = 0

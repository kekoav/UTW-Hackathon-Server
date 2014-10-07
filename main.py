__author__ = 'kekoa'


import os
import time

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from tornado import gen

from game_data import GAME_PLAYS

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hey the server is running but you didn't call the right endpoint. SUCKA.")

class GamesListHandler(tornado.web.RequestHandler):
    def get(self):
        data = {
            'games': [
            {
                "id": 'FFC97706-E3B3-4224-B602-DD7EBF9D32A6',
                "date": "2014-10-03T20:15:00",
                "name": "Utah State @ BYU"
            },
            {
                "id": 'FC8556DB-462A-4C24-AA01-BFB0CFB6566C',
                "date": "2014-10-04T20:15:00",
                "name": "Utah @ UCLA"
            }

        ]}

        self.write(data)

class GameHandler(tornado.web.RequestHandler):
    def get(self, game_id):
        all_game_info = {
            'FFC97706-E3B3-4224-B602-DD7EBF9D32A6': { # USU vs BYU
                'teams': {
                    'home': {
                        'name': "BYU",
                        'color': "#0000ff"
                    },
                    'away': {
                        'name': 'Utah State',
                        'color': '#ffffff',
                    }
                }
            }
        }

        game_info = all_game_info[game_id]

        self.write(game_info)

class StreamHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print "client connected"
        self.write_info("Hello! you are connected to the web socket!")

    def write_error(self, message):

        self.write_message({'type':'error', 'message':message})

    def write_info(self, message):

        self.write_message({'type':'info', 'message':message})

    @gen.engine
    def on_message(self, message):
        message_json = json.loads(message)
        command = message_json.get('command', None)

        if command.lower() == 'start':
            game_id = message_json.get('game_id', None)
            speed = message_json.get('speed', 3)

            if game_id is None or game_id not in GAME_PLAYS:
                self.write_error("Game with id '%s' not found'" % game_id)
                return

            plays = GAME_PLAYS[game_id]
            self.stream_open = True

            index = 0
            while self.stream_open and index < len(plays):
                data = {'type': 'play', 'index':index}
                data.update(plays[index])
                self.write_message(data)
                index += 1
                yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + speed)

        elif command.lower() == 'stop':
            self.stream_open = False
            self.write_info('Game stream stopped')

        else:
            self.write_error("Command '%s' not found" % command)

    def on_close(self):
        # Clean-up
        print "client disconnected"


def main():
    application = tornado.web.Application([
        (r'/stream', StreamHandler),
        (r'/game/([A-Z0-9\-]+)', GameHandler),
        (r'/games', GamesListHandler),
        (r"/", HomeHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
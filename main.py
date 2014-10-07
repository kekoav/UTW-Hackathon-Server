__author__ = 'kekoa'


import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import json

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
                        'color': "blue"
                    },
                    'away': {
                        'name': 'Utah State',
                        'color': 'white',
                    }
                }
            }
        }

        game_info = all_game_info[game_id]

        self.write(game_info)

def main():
    application = tornado.web.Application([
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
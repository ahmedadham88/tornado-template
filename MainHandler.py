from datetime import date
from pymongo import MongoClient
from tornado.options import define, options

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/add", AddHandler),
            (r"/github", tornado.web.RedirectHandler, dict(url="https://github.com/ahmedadham88/")),
            (r"/appName", ApplicationHandler),
            (r"/date", VisitHandler)
        ]

        settings = dict(
            autoescape=None,
        )

        tornado.web.Application.__init__(self, handlers, **settings)

        self.con = MongoClient()
        self.database = self.con["sampleUser"]

class VisitHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'last_visit':  date.today().isoformat() }
        self.write(response)

class ApplicationHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'application_name' : 'Tornado Template'}
        self.write(response)
 
class AddHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><h2 align="center">Add A User</h2>'
                   '<form action="/add" method="POST">'
                   '<label for="name">Name:</label><br/><input type="text" id="name" name="name"><br/>'
                   '<label for="email">Email:</label><br/><input type="email" id="email" name="email"><br/>'
                   '<label for="phone">Phone:</label><br/><input type="tel" id="phone" name="phone"><br/>'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        db=self.application.database

        new_user = {
            "name" : self.get_body_argument("name"),
            "phone" : self.get_body_argument("phone"),
            "email" : self.get_body_argument("email")
        }

        db.users.insert(new_user)

        self.write('<html><body><h2>New User saved with details:</h2> <br/><br/>'
                   '<h4>Name: ' + self.get_body_argument("name") + '<br/> </h4>'
                   '<h4>Email: ' + self.get_body_argument("email") + '<br/> </h4>'
                   '<h4>Phone: ' + self.get_body_argument("phone") + '<br/> </h4></body></html>')

        found = db.users.find()
        self.write("Current Users are: ")
        for c in found:
            self.write("<br/>")
            self.write(c["name"])
            self.write(' - ' + c["phone"])
            self.write(' - ' + c["email"])

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><h1 align="center">Welcome to the Tornado Template</h1>'
                   '<br/><br/><h3>You can navigate to one of the following options:</h3>'
                   '<ul><li><strong>/github</strong>: redirects you to my github account</li>'
                   '<li><strong>/appName</strong>: shows you the application name</li>'
                   '<li><strong>/date</strong>: shows you the current date of visit</li>'
                   '<li><strong>/add</strong>: redirects you to a form for adding details</li>')

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
 
if __name__ == "__main__":
    main()

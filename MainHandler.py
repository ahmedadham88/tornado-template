from datetime import date
from pymongo.connection import Connection

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
 
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
        self.write('<html><body><h2>New User saved with details:</h2> <br/><br/>'
        		   '<h4>Name: ' + self.get_body_argument("name") + '<br/> </h4>'
        		   '<h4>Email: ' + self.get_body_argument("email") + '<br/> </h4>'
        		   '<h4>Phone: ' + self.get_body_argument("phone") + '<br/> </h4></body></html>')

class RetrieveHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'last_visit':  date.today().isoformat() }
        self.write(response)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><h1 align="center">Welcome to the Tornado Template</h1>'
        		   '<br/><br/><h3>You can navigate to one of the following options:</h3>'
        		   '<ul><li><strong>/github</strong>: redirects you to my github account</li>'
        		   '<li><strong>/appName</strong>: shows you the application name</li>'
        		   '<li><strong>/time</strong>: shows you the current time</li>'
        		   '<li><strong>/add</strong>: redirects you to a form for adding details</li>'
        		   '<li><strong>/retrieve/{email}</strong>: retrieves your saved detail by email</li></ul></body></html>')
 
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/retrieve/([\w\+%_& ]+)", RetrieveHandler),
    (r"/add", AddHandler),
    (r"/github", tornado.web.RedirectHandler, dict(url="https://github.com/ahmedadham88/")),
    (r"/appName", ApplicationHandler),
    (r"/time", VisitHandler)
])
 
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

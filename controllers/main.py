import webapp2
from google.appengine.api import users
import os
import logging
import template_engine

from models.anagram import Anagram
from library.helper import Helper
from library.user import UserController

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(self)
        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

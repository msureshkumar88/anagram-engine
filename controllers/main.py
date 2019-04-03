import webapp2
from google.appengine.api import users
import os
import logging
import template_engine

from models.anagram import Anagram
from library.helper import Helper
from library.user import UserController
from models.user import User
from models.anagram import Anagram
from google.appengine.ext import ndb
import itertools
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(self)
        template_values = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user']
        }

        shapes = ['c', 't', 's', ]
        result = itertools.combinations(shapes, 2)
        for each in result:
            logging.info("".join(list(each)))
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(self)
        errors = []
        anagrams = []
        word = self.request.get('word')
        if not Helper.validate_string(word):
            errors.append("Invalid word entered, please enter alphabetical characters only")

        if len(errors) == 0 :
            anagrams_request = ndb.Key('Anagram', Helper.get_word_key(user["user"].email, word))
            anagrams_request = anagrams_request.get()
            anagrams = []
            if anagrams_request:
                anagrams = anagrams_request.anagram
            else:
                errors.append("Anagrams not available for this search")

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'errors': errors,
            'user': user['user'],
            'anagrams': anagrams
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/home.html')
        self.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

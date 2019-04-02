import webapp2
from google.appengine.api import users
import os
import logging
import template_engine

from models.anagram import Anagram
from library.helper import Helper
from library.user import UserController
from anagram import AnagramController


class AnagramRequest(webapp2.RequestHandler):
    def get(self):
        user = UserController.get_user(self)
        #logging.info(user["user"].email)
        logging.info("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.response.headers['Content-Type'] = 'text/html'
        path = self.request.path
        logging.info(Helper.anagrams("sam"))
        if path == "/anagram/save":
            AnagramController.save_get(self)
        elif path == "/anagram/search":
            AnagramController.search_get(self)
        elif path == "/anagram/sub_anagram":
            AnagramController.subanagram_get(self)

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        path = self.request.path

        if path == "/anagram/save":
            AnagramController.save_post(self)
        elif path == "/anagram/search":
            AnagramController.search_post(self)
        elif path == "/anagram/sub_anagram":
            AnagramController.subanagram_post(self)


app = webapp2.WSGIApplication([
    ('/anagram/save', AnagramRequest),
    ('/anagram/search', AnagramRequest),
    ('/anagram/sub_anagram', AnagramRequest)
], debug=True)

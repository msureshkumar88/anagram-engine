import webapp2
from google.appengine.api import users
import os
import logging
import template_engine
from google.appengine.ext import ndb

from models.anagram import Anagram
from library.helper import Helper
from library.user import UserController


class AnagramController:
    @classmethod
    def save_get(self, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        logging.info(user)
        data = {
            'url': user["url"],
            'url_string': user['url_string'],
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/save.html')
        request.response.write(template.render(data))

    @classmethod
    def save_post(self, request):
        errors = []
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)

        word = request.request.get('word')

        if Helper.validate_string(word) == None:
            errors.append("Please enter valid word")
        else:
            Anagram_key = ndb.Key('Anagram', Helper.get_word_key(word))
            Anagram1 = Anagram_key.get()
            if Anagram1:
                errors.append("word already exist")

        if len(errors) == 0:
            anagrams = Helper.anagrams(word)
            anagram_count = len(anagrams)
            letter_count = len(word)
            newAnagram = Anagram(id=Helper.get_word_key(word), word=word, anagram_count=anagram_count,
                                 letter_count=letter_count, anagram=anagrams, user_key=user["user_id"])
            newAnagram.put()

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'errors': errors
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/save.html')
        request.response.write(template.render(data))


app = webapp2.WSGIApplication([
    ('/anagram/save', AnagramController)
], debug=True)

import webapp2
from google.appengine.api import users
import os
import logging
import template_engine
from google.appengine.ext import ndb

from models.anagram import Anagram
from library.helper import Helper
from library.user import UserController
import collections
from models.user import User


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
    def save_post(cls, request):
        errors = []
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)

        word = request.request.get('word')
        Anagram1 = ""
        if Helper.validate_string(word) == None:
            errors.append("Please enter valid word")
        else:
            Anagram_key = ndb.Key('Anagram', Helper.get_word_key(user["user"].email, word))
            Anagram1 = Anagram_key.get()
            # Anagram1.anagram.append("sdsdsd")
            # logging.info(Anagram1.anagram)
            #return
            # if Anagram1:
            #     errors.append("word already exist")

        if len(errors) == 0:
            if Anagram1:
                if word not in Anagram1.anagram:
                    Anagram1.anagram.append(word)
                    Anagram1.anagram_count = Anagram1.anagram_count + 1
                    Anagram1.put()

                    user_key = ndb.Key('User', user["user"].email)
                    user1 = user_key.get()
                    user1.total_anagrams = user1.total_anagrams + 1
                    user1.put()

            else:
                letter_count = len(word)
                newAnagram = Anagram(id=Helper.get_word_key(user["user"].email, word), anagram_count=1,
                                     letter_count=letter_count, anagram=[word], user_key=user["user_id"])
                newAnagram.put()

                user_key = ndb.Key('User', user["user"].email)
                user1 = user_key.get()
                user1.total_words = user1.total_words + 1
                user1.total_anagrams = user1.total_anagrams + 1
                user1.put()

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'errors': errors
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/save.html')
        request.response.write(template.render(data))

    @classmethod
    def search_get(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        errors = []

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'errors': errors
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/search.html')
        request.response.write(template.render(data))

    @classmethod
    def search_post(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        errors = []
        word = request.request.get('word')
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
            'anagrams': anagrams
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/search.html')
        request.response.write(template.render(data))

app = webapp2.WSGIApplication([
    ('/anagram/save', AnagramController)
], debug=True)

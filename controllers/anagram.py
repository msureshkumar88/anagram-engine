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
import itertools
from google.appengine.ext import blobstore

class AnagramController:
    @classmethod
    def save_get(self, request):
        # ndb.delete_multi(
        #     Anagram.query().fetch(keys_only=True)
        # )
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        logging.info(user)
        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user']
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/save.html')
        request.response.write(template.render(data))

    @classmethod
    def save_post(cls, request):
        errors = []
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        success = False
        word = request.request.get('word')
        if Helper.validate_string(word) == None:
            errors.append("Please enter valid word")
        else:
            Helper.saveAnagram(word,user["user"].email)

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'errors': errors,
            'success': True
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
            'user': user['user'],
            'errors': errors
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/search.html')
        request.response.write(template.render(data))

    @classmethod
    def search_post(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        errors = []
        anagrams = []
        word = request.request.get('word')
        if not Helper.validate_string(word):
            errors.append("Invalid word entered, please enter alphabetical characters only")

        if len(errors) == 0 :
            anagrams_request = ndb.Key('Anagram', Helper.get_word_key(user["user"].email, word))
            anagrams_request = anagrams_request.get()

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
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/search.html')
        request.response.write(template.render(data))

    @classmethod
    def subanagram_get(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        errors = []

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'user': user['user'],
            'errors': errors
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/sub_anagram.html')
        request.response.write(template.render(data))

    @classmethod
    def subanagram_post(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        errors = []
        anagrams = []
        word = request.request.get('word')
        logging.info(word)
        sub_anagrams = Helper.getAnagramCombinations(word)
        #logging.info(sub_anagrams)
        # return
        matched_subs = []
        keys = []
        for val in sub_anagrams:
            sub_key = Helper.get_word_key(user["user"].email, val)
            Anagram_key = ndb.Key('Anagram', sub_key)
            Anagram = Anagram_key.get()
            if Anagram and not sub_key in keys:
                matched_subs.extend(Anagram.anagram)
                keys.append(sub_key)
        if not matched_subs:
            errors.append("There are no sub anagrams available for this search")
        logging.info(matched_subs)
        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'errors': errors,
            'user': user['user'],
            'anagrams': matched_subs
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/sub_anagram.html')
        request.response.write(template.render(data))

    @classmethod
    def upload_get(cls, request):
        request.response.headers['Content-Type'] = 'text/html'
        user = UserController.get_user(request)
        errors = []
        upload_url = blobstore.create_upload_url('/upload_text')
        success = request.request.params

        data = {
            'url': user["url"],
            'url_string': user['url_string'],
            'errors': errors,
            'user': user['user'],
            'upload_url': upload_url,
            'success': success
        }
        template = template_engine.JINJA_ENVIRONMENT.get_template('views/anagram/upload.html')
        request.response.write(template.render(data))

    @classmethod
    def upload_post(cls, request):
        pass

app = webapp2.WSGIApplication([
    ('/anagram/save', AnagramController)
], debug=True)

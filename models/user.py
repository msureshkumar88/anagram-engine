from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty()
    total_words = ndb.IntegerProperty()
    total_anagrams = ndb.IntegerProperty()
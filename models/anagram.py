from google.appengine.ext import ndb


class Anagram(ndb.Model):
    user_key = ndb.StringProperty()
    anagram = ndb.StringProperty(repeated=True)
    anagram_count = ndb.IntegerProperty()
    letter_count = ndb.IntegerProperty()

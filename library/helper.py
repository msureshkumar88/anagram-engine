import logging

from models.anagram import Anagram
from models import user
import re
import itertools
from google.appengine.ext import ndb

class Helper:

    @classmethod
    def get_word_key(cls, user_email, word):
        letters = list(word)
        letters = sorted(letters)
        return  user_email +'/' + ''.join(letters)

    @classmethod
    def validate_string(cls, word):
        word = word.strip()
        return re.search('^[a-zA-Z]+$', word)

    @classmethod
    def anagrams(cls, word):
        """ Generate all of the anagrams of a word. """
        anagram_list = []
        if len(word) < 2:
            anagram_list.append(word)
        else:
            for i, letter in enumerate(word):
                if not letter in word[:i]:  # avoid duplicating earlier words
                    for j in Helper.anagrams(word[:i] + word[i + 1:]):
                        anagram_list.append(j + letter)

        return anagram_list

    @classmethod
    def getAnagramCombinations(cls, word):
        anagrams = []
        for i in range(len(word)-1,2, -1):
            combi = ["".join(x) for x in list(itertools.permutations(word, i))]
            anagrams.extend(combi)

        logging.info(itertools.permutations(word, 3))
        return anagrams
        # for each in itertools.permutations(list(word), 3):
        #     logging.info(each)
        # return itertools.permutations(word, len(word)-1)

    @classmethod
    def saveAnagram(cls, word, user_email):
        anagram_key = ndb.Key('Anagram', Helper.get_word_key(user_email, word))
        anagram1 = anagram_key.get()
        word = word.lower()
        if anagram1:
            if word not in anagram1.anagram:
                anagram1.anagram.append(word)
                anagram1.anagram_count = anagram1.anagram_count + 1
                anagram1.put()

                user_key = ndb.Key('User', user_email)
                user1 = user_key.get()
                user1.total_anagrams = user1.total_anagrams + 1
                user1.put()

        else:
            letter_count = len(word)
            newAnagram = Anagram(id=Helper.get_word_key(user_email, word), anagram_count=1,
                                 letter_count=letter_count, anagram=[word], user_key=user_email)
            newAnagram.put()

            user_key = ndb.Key('User', user_email)
            user1 = user_key.get()
            user1.total_words = user1.total_words + 1
            user1.total_anagrams = user1.total_anagrams + 1
            user1.put()
        return




import logging

from models import anagram
import re


class Helper:

    @classmethod
    def get_word_key(cls, word):
        letters = list(word)
        letters = sorted(letters)
        return ''.join(letters)

    @classmethod
    def validate_string(cls, word):
        logging.info(re.search('^[a-zA-Z]+$', word))

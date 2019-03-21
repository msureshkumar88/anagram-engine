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


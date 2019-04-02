import logging

from models import anagram
import re
import itertools

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


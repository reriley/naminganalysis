from collections import Counter
import cmudict
from english_words import get_english_words_set
import os

CURRENT_DIR = os.path.dirname(__file__)
CLICHE_LIST_PATH = os.path.join(CURRENT_DIR, 'cliches')
EXCLUSION_LIST_PATH = os.path.join(CURRENT_DIR, 'exclusions')

with open(CLICHE_LIST_PATH) as f:
    CLICHE_LIST = f.read().splitlines()
with open(EXCLUSION_LIST_PATH) as f:
    EXCLUSION_LIST = f.read().splitlines()
PRONOUNACABLE_PARTS = cmudict.dict().keys()
LOCAL_DICTIONARY = get_english_words_set(['gcide', 'web2'], lower=True)


class WordAnalyzer:

    def __init__(self):
        # self.language_dictionary_api_queries = 0
        pass

    def decompose_phrase(self, phrase: str) -> Counter:
        phrase_part_counter = Counter()
        words = phrase.split(' ')
        for w in words:
            phrase_part_counter.update(self.decompose_word(w))
        return phrase_part_counter

    def decompose_word(self, word: str) -> Counter:
        word_part_counter = Counter()
        word = word.lower()

        word = ''.join([c for c in word if c.isalpha()])

        excluded = self.in_dictionary(word) or word in EXCLUSION_LIST
        included = word in CLICHE_LIST
        if excluded and not included:
            return word_part_counter

        word = word + '_'  # Append a meaningless character to facilitate counting backwards
        word_length = len(word)
        word_part_counter = Counter()
        unevaluated = Counter(range(word_length))
        for i in range(word_length):
            if i not in unevaluated:
                pass
            else:
                for j in range(1, word_length-i):
                    snippet = word[i:-j]  # Count backwards

                    and_condition_set = list()
                    or_condition_set = list()

                    and_condition_set.append(len(snippet) > 1)
                    and_condition_set.append(snippet not in EXCLUSION_LIST)

                    or_condition_set.append(snippet in PRONOUNACABLE_PARTS)
                    or_condition_set.append(self.in_dictionary(snippet))
                    or_condition_set.append(snippet.lower() in CLICHE_LIST)

                    # if all(and_condition_set) and not any(or_condition_set):
                    #     cond4 = False  # Placeholder: Is the string in the dictionary?
                    #     self.language_dictionary_api_queries += 1
                    if all(and_condition_set) and any(or_condition_set):
                        word_part_counter.update([snippet])
                        unevaluated.subtract(range(i, word_length-j))
                        unevaluated._keep_positive()
                        break
        return word_part_counter

    @staticmethod
    def in_dictionary(snippet):
        if snippet == '' or snippet == '_':
            return None
        # Add a stemming function to
        result = snippet in LOCAL_DICTIONARY
        if not result and snippet[-3:] == 'ies':
            result = snippet[:-3] + 'y' in LOCAL_DICTIONARY
        elif not result and snippet[-1] == 's':
            result = snippet[:-1] in LOCAL_DICTIONARY
        return result

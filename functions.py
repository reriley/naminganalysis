from collections import Counter
import cmudict

PRONOUNACABLE_WORDS = cmudict.dict().keys()


class Decomposer:

    def __init__(self):
        self.language_dictionary_api_queries = 0

    def decompose_name(self, name: str) -> Counter:
        name_part_counter = Counter()
        words = name.split(' ')
        for w in words:
            name_part_counter.update(self.decompose_word(w))
        return name_part_counter

    def decompose_word(self, word: str) -> Counter:
        word = word.lower() + '_'  # Append a meaningless character to facilitate counting backwards
        word_length = len(word)
        word_part_counter = Counter()
        unevaluated = Counter(range(word_length))
        for i in range(word_length):
            if i not in unevaluated:
                pass
            else:
                for j in range(word_length-i):
                    nugget = word[i:-j-1]  # Count backwards
                    cond1 = len(nugget) > 1
                    cond2 = nugget.lower() in PRONOUNACABLE_WORDS
                    cond3 = False
                    if cond1 and not cond2:
                        cond3 = False  # Placeholder: Is the string in the dictionary?
                        self.language_dictionary_api_queries += 1
                    if cond1 and (cond2 or cond3):
                        word_part_counter.update([nugget])
                        unevaluated.subtract(range(i, word_length-j-1))
                        unevaluated._keep_positive()
                        break
        return word_part_counter

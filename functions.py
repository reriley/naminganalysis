from collections import Counter
import cmudict

PRONOUNACABLE_WORDS = cmudict.dict().keys()


def decompose_name(name: str) -> Counter:
    part_counter = Counter()
    words = name.split(' ')
    for w in words:
        part_counter.update(decompose_word(w))
    return part_counter


def decompose_word(word: str) -> Counter:
    word = word.lower() + '_'  # Append a meaningless character to facilitate counting backwards
    word_length = len(word)
    part_counter = Counter()
    unevaluated = Counter(range(word_length))
    for i in range(word_length):
        if i not in unevaluated:
            pass
        else:
            for j in range(word_length-i):
                nugget = word[i:-j-1]  # Count backwards
                cond1 = len(nugget) > 1
                cond2 = nugget.lower() in PRONOUNACABLE_WORDS
                cond3 = True  # Placeholder: Is the string in the dictionary?

                if cond1 and (cond2 or cond3):
                    part_counter.update([nugget])
                    unevaluated.subtract(range(i, word_length-j-1))
                    unevaluated._keep_positive()
                    break
    return part_counter

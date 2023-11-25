from collections import Counter
from tqdm import tqdm
import pandas as pd
from analyzer import WordAnalyzer
import numpy as np


class NameSet:

    def __init__(self, names: list):

        if not all(isinstance(name, str) for name in names):
            raise TypeError("The 'names' parameter should be given as a list of strings.")

        self.counter = Counter()
        self._analyser = WordAnalyzer()
        self.names = dict()
        for name in names:
            self.names[name] = Name(name)

        self._is_analyzed = False
        self._is_scored = False

    def analyze(self):
        for k, _ in tqdm(self.names.items()):
            self.names[k].update_stats(self._analyser.decompose_phrase(k))

        self.counter = Counter()
        for _, v in self.names.items():
            self.counter.update(v.counter)
        self._is_analyzed = True

    def score(self):
        for name in tqdm(self):
            name.part_score = Counter({k: name.counter[k] * self.counter[k] for k in name.counter})
        self._is_scored = True

    def get_stats(self):
        if not self._is_analyzed:
            raise RuntimeError('NameSet has not been _is_analyzed. Use the analyze() method.')
        df = pd.DataFrame.from_dict(self.counter, orient='index').reset_index()
        df.rename(columns={'index': 'part', 0: 'count'}, inplace=True)
        df.sort_values(by='count', ascending=False, inplace=True)
        return df

    def get_scores(self):
        df = pd.DataFrame.from_dict(self.scores, orient='index').reset_index()
        df.rename(columns={'index': 'name', 0: 'score'}, inplace=True)
        df.sort_values(by='score', ascending=False, inplace=True)
        return df

    def get_names_with_part(self, snippet: str):
        phrase_list = [k for k, v in self.names.items() if snippet in v.counter]
        return phrase_list

    def _get_all_scores(self, normalized=True):
        if not self._is_scored:
            raise RuntimeError('NameSet has not been _is_scored. Use the score() method.')
        if normalized:
            scores = {name.string: name.norm_score for name in self.names.values()}
        else:
            scores = {name.string: name.score for name in self.names.values()}
        return scores

    def __getitem__(self, name):
        return self.names[name]

    def __setitem__(self, name):
        pass

    def __iter__(self):
        return iter(self.names.values())

    def keys(self):
        return self.names.keys()

    def items(self):
        return self.names.items()

    def values(self):
        return self.names.values()

    scores = property(_get_all_scores)


class Name(object):

    def __init__(self, name: str):
        self.string = name
        self.counter = Counter()
        self.part_score = Counter()

    def update_stats(self, counter: Counter):
        self.counter = Counter()
        self.counter.update(counter)

    def _get_score(self):
        score = np.prod(list(self.part_score.values()))
        return score

    def _get_normalized_score(self):
        score = self._get_score()
        num_parts = len(self.counter)
        if num_parts == 0:
            normalized_score = 0
        else:
            normalized_score = score / num_parts
        return normalized_score

    score = property(_get_score)
    norm_score = property(_get_normalized_score)

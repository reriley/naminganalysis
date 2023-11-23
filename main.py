from functions import decompose_name
from collections import Counter
import pandas as pd

with open('names') as f:
    names = f.read().splitlines()

names_dict = dict()
for n in names:
    names_dict[n] = decompose_name(n)

all_names_counter = Counter()
for _, v in names_dict.items():
    all_names_counter.update(v)

df = pd.DataFrame.from_dict(all_names_counter, orient='index').reset_index()
df.to_csv('results.csv')

pass
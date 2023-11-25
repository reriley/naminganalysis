from words import NameSet

with open('names') as f:
    names = f.read().splitlines()

name_set = NameSet(names)
name_set.analyze()
name_set.score()
stats = name_set.get_stats()
scores = name_set.get_scores()
stats.to_csv('stats.csv')
scores.to_csv('scores.csv')
pass
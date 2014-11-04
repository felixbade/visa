import json

from app import scores
import config

team_scores = scores.calculate_scores_from_list()

scores = {}

for team in team_scores:
    score, players = team_scores[team]
    scores.update({team: score})
    print ('%s: %d%% (%d pelaajaa)' % (team, score, players))

f = open(config.results_file, 'w')
json.dump(scores, f)
f.close()

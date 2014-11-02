import json

from app import questions
from config import logfilename

def load_requests():
    with open(logfilename, 'r') as logfile:
        text = logfile.read()
        for line in text.split('\n'):
            if not line:
                continue
            yield json.loads(line)

def is_question(question):
    index = questions.get_index_by_question_text(question)
    # first question is what team you are in
    return index is not None and index > 0

def is_team_choice(question):
    index = questions.get_index_by_question_text(question)
    # first question is what team you are in
    return index is not None and index == 0

def get_correct_answer(question):
    index = questions.get_index_by_question_text(question)
    answers = questions.get_question_and_answers_by_number(
            index)['answers']
    # first answer is correct, other answers are false
    return answers[0]

def calculate_scores_from_list():
    players = {}
    for request in load_requests():
        if request['type'] != 'response':
            continue
        session = request.get('session', {})
        player_id = session.get('id', None)
        team = None

        answers = session.get('answers', {})
        score = 0
        answer_count = 0
        for key in answers:
            if is_question(key):
                answer_count += 1
                if answers[key] == get_correct_answer(key):
                    score += 1
            elif is_team_choice(key):
                team = answers[key]

        players.update({player_id: (score, team)})
    
    # this has to be done in two phases because
    # 1) players can change their answers
    # 2) there can be multiple players per team
    team_scores = {}
    for player in players:
        score, team = players[player]
        score_this_far = 0
        players_this_far = 0
        if team in team_scores:
            score_this_far, players_this_far = team_scores[team]
        new_score = score_this_far + score
        new_players = players_this_far + 1
        team_scores.update({team: (new_score, new_players)})

    for team in team_scores:
        score, players = team_scores[team]
        score /= float(players + 1)
        print(team, score)

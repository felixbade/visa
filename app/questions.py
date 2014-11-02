import yaml

from config import questions_file

with open(questions_file) as f:
    question_list = yaml.safe_load(f)

def get_question_and_answers_by_answered_questions(answered):
    for question in question_list:
        if question['question'] not in answered:
            return question
    return None

def is_such_question(question_text):
    for question_and_answer in question_list:
        if question_and_answer['question'] == question_text:
            return True
    return False

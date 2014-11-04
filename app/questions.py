import yaml

from config import questions_file

with open(questions_file) as f:
    question_list = yaml.safe_load(f)

def get_number_of_questions():
    return len(question_list)

def get_question_and_answers_by_number(number):
    if number >= 0 and number < len(question_list):
        return question_list[number]
    return None

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

def get_index_by_question_text(question_text):
    for i in range(len(question_list)):
        if question_list[i]['question'] == question_text:
            return i
    return None


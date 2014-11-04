import random
import json

from flask import render_template, session, request

from app import app
import config
from app import request_logger
from app import questions

@app.route('/', methods=['GET', 'POST'])
def q():
    possible_questions = list(request.form.keys())
    if len(possible_questions) == 1:
        question = possible_questions[0]
        if questions.is_such_question(question):
            session['answers'].update({question: request.form[question]})
            session['qnumber'] += 1
    
    question_and_answers = questions.get_question_and_answers_by_number(session['qnumber'])

    if question_and_answers is None:
        return render_template('ready.html')

    question = question_and_answers.get('question')
    answers = question_and_answers.get('answers', [])
    selected = None
    description = question_and_answers.get('description')

    # shuffle answers if not stated otherwise
    if question_and_answers.get('shuffle', True):
        random.shuffle(answers)
    if question in session['answers']:
        selected = session['answers'][question]
    
    return render_template('question.html', question=question, answers=answers, selected=selected, description=description)

@app.route('/uudestaan')
def again():
    if session['qnumber'] < questions.get_number_of_questions():
        session['qnumber'] = 0
    return q()

@app.route('/vastaukset')
def vastaukset():
    answer_list = []
    for qnumber in range(1, questions.get_number_of_questions()-1):
        question_and_answers = questions.get_question_and_answers_by_number(qnumber)

        question = question_and_answers.get('question')
        correct_answer = question_and_answers.get('answers')[0]
        answer_list.append({'question': question, 'answer': correct_answer})
    return render_template('answers.html', answers=answer_list)
    
@app.route('/id')
def id():
    return str(session['id'])

@app.route('/tulokset')
def tulokset():
    with open(config.results_file) as results:
        scores = json.load(results)

    teams = [
            {'name': 'Matematiikka', 'value': '0', 'color': '#177fa5'},
            {'name': 'Fysiikka', 'value': '0', 'color': '#db405d'},
            {'name': 'Kemia', 'value': '0', 'color': '#e9bb43'},
            {'name': 'Biologia', 'value': '0', 'color': '#57a93b'}
            ]

    for i in range(len(teams)):
        teams[i]['value'] = str(scores[teams[i]['name']])

    return render_template('scores.html', teams=teams)

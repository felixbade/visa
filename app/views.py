import time
import json
import base64

from flask import render_template, session, request

from app import app
import config
from app import request_logger
from app import questions

@app.route('/', methods=['GET', 'POST'])
def q():
    # NOTE: this will break if questions are answered in wrong order
    # TODO: make sure that is is not possible
    possible_questions = list(request.form.keys())
    if len(possible_questions) == 1:
        question = possible_questions[0]
        if questions.is_such_question(question):
            session['answers'].update({question: request.form[question]})
            session['qnumber'] += 1
    
    question_and_answers = questions.get_question_and_answers_by_number(session['qnumber'])

    if question_and_answers is None:
        return render_template('ready.html')

    question = question_and_answers['question']
    answers = question_and_answers['answers']
    if question in session['answers']:
        selected = session['answers'][question]

    return render_template('question.html', question=question, answers=answers, selected=selected)

@app.route('/uudestaan')
def again():
    session['qnumber'] = 0
    return q()

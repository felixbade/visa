import time
import json

from flask import session, request

from app import app
import config

logfile = open(config.logfilename, 'a')

def log(dictionary):
    logfile.write(json.dumps(dictionary) + '\n')
    logfile.flush()

id_counter = 0
def get_next_id():
    global id_counter
    id_counter += 1
    return id_counter

@app.before_request
def before():
    # TODO: this really should not be here, but where?
    session.permanent = True
    if not 'id' in session or type(session['id']) is not int:
        session['id'] = get_next_id()
    if not 'answers' in session or type(session['answers']) is not dict:
        session['answers'] = {}
    if not 'qnumber' in session or type(session['qnumber']) is not int:
        session['qnumber'] = 0
    
    request_ = {
            'type': 'request',
            'timestamp': time.time(),
            'ip': request.remote_addr,
            'session': dict(session),
            'headers': dict(request.headers),
            'form': dict(request.form)
    }
    log(request_)

@app.after_request
def after(response):
    response_ = {
            'type': 'response',
            'timestamp': time.time(),
            'session': dict(session),
            'headers': dict(response.headers)
    }
    log(response_)
    return response

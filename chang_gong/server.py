#!/usr/bin/env python
#coding: utf-8

import os
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

import json
import base64

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)

clients=[]
user_no = 1
ui_current_state = {'power':'', 'button':''}

def call_current_state():
    return ui_current_state

@app.before_request
def before_request():
    global user_no
    if 'session' in session and 'user-id' in session:
        pass
    else:
        session['session'] = os.urandom(24)
        session['username'] = 'user'+str(user_no)
        user_no += 1

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/mynamespace')
def connect():
    emit("response", {'data': 'Connected', 'username': session['username']})
    clients.append(request.sid)

@socketio.on('disconnect', namespace='/mynamespace')
def disconnect():
    session.clear()
    clients.remove(request.sid)
    print ("Disconnected")

@socketio.on("request", namespace='/mynamespace')
def web_request(message):
    if message['data'] == 'pet' :
        r_stat.user_select = 'pet'
        return
    
    if message['data'] == 'can' :
        r_stat.user_select = 'can'
        return
    
    if message['data'] == 'start' :
        r_stat.startRVM()
        return

    if message['data'] == 'end' :
        if r_stat.user_select == '' and r_stat.reset_selection == 0:
            r_stat.terminationRVM()
        else :
            r_stat.reset_selection = 1
        return

    if message['data'] == 'force_continue' :
        r_stat.force_continue = message['arg'] 
        return

    print(message)
    print(session)
    print(clients)
    emit("response", {'data': message['data'], 'username': session['username']}, broadcast=True)

def socketStart() :
    print('start')
    app.app_context()
    socketio.run(app,host='0.0.0.0', port=5000)

def getClass(newClass) :
    global r_stat
    r_stat = newClass

def sendMesg(string) :
    print('send:' + string)
    socketio.emit("response", {'head': 'msg_ready','data': string},namespace='/mynamespace',room= clients[-1])

def sendCount() :
    obj = {'can': r_stat.recycling_number['can'],'pet': r_stat.recycling_number['pet'] }
    socketio.emit("response", {'head': 'count_ready','data': obj},namespace='/mynamespace',room= clients[-1])

def endReport() :
    print('aaa')
    obj = {'head' : 'end' ,'can': r_stat.recycling_number['can'],'pet': r_stat.recycling_number['pet'] }
    socketio.emit("response", obj,namespace='/mynamespace',room= clients[-1])

'''
def sendCamera(url) :
    obj = {'head':'img_ready', 'data':url}
    socketio.emit("response", obj,namespace='/mynamespace',room= clients[-1])
'''

def sendCamera(url) :
    with open('.'+url, 'rb') as img:
        b64 = base64.b64encode(img.read()).decode('utf-8')
    obj = {'head':'img_ready', 'data':b64}
    socketio.emit("response", obj,namespace='/mynamespace',room= clients[-1])

def error_report(s) :
    obj = {'head':'error', 'data':s}
    socketio.emit("response", obj,namespace='/mynamespace',room= clients[-1])

def setButton(string) :
    obj = {'head':'button', 'data':string}
    socketio.emit("response", obj,namespace='/mynamespace',room= clients[-1])

def trigger(data) :
    obj = {'head':'trigger', 'data':data}
    socketio.emit("response", obj,namespace='/mynamespace',room= clients[-1])

    

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000)
    print('aaaaas')
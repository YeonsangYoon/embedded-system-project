from flask import Flask, request
import os
import sys
import subprocess
import time
import random

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/requestd', methods = ['POST'])
def start_discrimination():
    

    # YOLO 실행하는 내용 추가하세요..... 

    q = random.randint(1,10)
    if q <= 2:
        return 'return'
    elif q > 2 and q <= 8:
        return 'pet'
    elif q > 8 and q <= 10:
        return 'can'

    

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', threaded=False, debug=False, port=5000)